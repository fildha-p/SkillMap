from django.shortcuts import render, get_object_or_404, redirect
from .models import Skill, UserRole, UserSkillLevel, AssessmentAttempt, Role
from .services import evaluate_assessment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# -------------------------------
# Skill Category Helper
# -------------------------------
def get_skill_category(level, total_levels):
    if total_levels == 0:
        return "Beginner"

    percentage = (level / total_levels) * 100

    if percentage < 40:
        return "Beginner"
    elif percentage < 70:
        return "Intermediate"
    else:
        return "Advanced"


# ===============================
# TAKE ASSESSMENT
# ===============================
@login_required
def take_assessment(request, skill_id, level):
    skill = get_object_or_404(Skill, id=skill_id)

    user_skill, _ = UserSkillLevel.objects.get_or_create(
        user=request.user,
        skill=skill,
        defaults={'level': 0}
    )

    if level > user_skill.level + 1:
        current_role_id = request.GET.get("role")
        if current_role_id:
            return redirect(f'/skillmap/dashboard/?role={current_role_id}')
        return redirect('dashboard')
        # return redirect('dashboard')

    if level > skill.total_levels:
        current_role_id = request.GET.get("role")
        if current_role_id:
            return redirect(f'/skillmap/dashboard/?role={current_role_id}')
        return redirect('dashboard')
        # return redirect('dashboard')

    questions = skill.questions.filter(difficulty_level=level)

    if request.method == 'POST':
        
        current_role_id = request.GET.get("role")

        attempt = evaluate_assessment(
        user=request.user,
        skill=skill,
        level=level,
        submitted_answers=request.POST
    )

        wrong_count = attempt.total_questions - attempt.correct_count

        return render(request, 'skillmap/assessment.html', {
        'skill': skill,
        'level': level,
        'questions': questions,
        'result': attempt,
        'wrong_count': wrong_count,
        'current_role_id': current_role_id,
    })
    return render(request, 'skillmap/assessment.html', {
    'skill': skill,
    'level': level,
    'questions': questions,
    'current_role_id': request.GET.get("role"),
})


# ===============================
# DASHBOARD (Dynamic Readiness)
# ===============================
@login_required
def dashboard(request):
    user = request.user
    selected_roles = UserRole.objects.filter(user=user).select_related('role')

    # Add Role
    if request.method == "POST":
        
        role_id = request.POST.get("role_id")
        if role_id:
            
            role = get_object_or_404(Role, id=role_id)
            UserRole.objects.get_or_create(user=user, role=role)
            return redirect(f"{request.path}?role={role.id}")

    role_id = request.GET.get("role")

    # Auto-select first role if none selected
    if not role_id and selected_roles.exists():
        role_id = selected_roles.order_by('selected_at').first().role.id

    active_role = None
    role_readiness = None
    skill_progress = []
    weakest_skill = None
    strongest_skill = None
    role_status = None
    attempts = []

    if role_id:
        user_role = get_object_or_404(UserRole, user=user, role_id=role_id)
        active_role = user_role.role
        skills = active_role.skills.all()

        attempts = AssessmentAttempt.objects.filter(
            user=user,
            skill__in=skills
        ).select_related('skill').order_by('-attempted_at')

        user_skills = UserSkillLevel.objects.filter(
            user=user,
            skill__in=skills
        )

        user_skill_dict = {us.skill_id: us.level for us in user_skills}

        lowest_ratio = 101
        highest_ratio = -1
        total_ratio = 0
        count = 0

        for skill in skills:
            current_level = user_skill_dict.get(skill.id, 0)
            total_levels = skill.total_levels

            ratio = (current_level / total_levels) * 100 if total_levels > 0 else 0

            total_ratio += ratio
            count += 1

            if ratio < lowest_ratio:
                lowest_ratio = ratio
                weakest_skill = skill.name

            if ratio > highest_ratio:
                highest_ratio = ratio
                strongest_skill = skill.name

            skill_progress.append({
                "skill": skill,
                "current_level": current_level,
                "next_level": current_level + 1 if current_level < total_levels else None,
                "total_levels": total_levels,
                "category": get_skill_category(current_level, total_levels)
            })

        # Dynamic Readiness Calculation
        role_percentage = round(total_ratio / count, 2) if count > 0 else 0

        if role_percentage < 40:
            category = "Beginner"
            role_status = "Not Ready"
        elif role_percentage < 70:
            category = "Intermediate"
            role_status = "Developing"
        elif role_percentage < 90:
            category = "Advanced"
            role_status = "Almost Ready"
        else:
            category = "Advanced"
            role_status = "Interview Ready"

        role_readiness = {
            "percentage": role_percentage,
            "label": category
        }

    all_roles = Role.objects.exclude(
        id__in=selected_roles.values_list("role_id", flat=True)
    )

    return render(request, "skillmap/dashboard.html", {
        "selected_roles": selected_roles,
        "all_roles": all_roles,
        "active_role": active_role,
        "role_readiness": role_readiness,
        "skill_progress": skill_progress,
        "weakest_skill": weakest_skill,
        "strongest_skill": strongest_skill,
        "role_status": role_status,
        "attempts": attempts,
    })

# ===============================
# RESET SKILL (Now Simple)
# ===============================
@login_required
def reset_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)

    UserSkillLevel.objects.filter(
        user=request.user,
        skill=skill
    ).update(level=0)

    AssessmentAttempt.objects.filter(
        user=request.user,
        skill=skill
    ).delete()

    current_role_id = request.GET.get("role")
    if current_role_id:
        return redirect(f'/skillmap/dashboard/?role={current_role_id}')
    return redirect('dashboard')


# ===============================
# REGISTER
# ===============================
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(request, "skillmap/register.html", {
        'form': form
    })


def home(request):
    return render(request, "skillmap/home.html")


@login_required
def assessment_result(request, attempt_id):
    attempt = get_object_or_404(
        AssessmentAttempt,
        id=attempt_id,
        user=request.user
    )

    current_role_id = request.GET.get("role")

    return render(request, "skillmap/result.html", {
        'attempt': attempt,
        'current_role_id': current_role_id,
    })

@login_required
def assessment_history(request):
    attempts = AssessmentAttempt.objects.filter(
        user=request.user
    ).select_related('skill').order_by('-attempted_at')

    return render(request, 'skillmap/history.html', {
        'attempts': attempts
    })


@login_required
def delete_role(request, role_id):
    UserRole.objects.filter(
        user=request.user,
        role_id=role_id
    ).delete()

    return redirect("dashboard")