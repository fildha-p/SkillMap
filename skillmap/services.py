from .models import Question, AssessmentAttempt, UserRole, UserSkillLevel

LEVEL_THRESHOLDS = {
    1: 40,
    2: 55,
    3: 70,
    4: 85,
    5: 95
}


def calculate_level(score_percentage):
    achieved_level = 0
    for level, threshold in LEVEL_THRESHOLDS.items():
        if score_percentage >= threshold:
            achieved_level = level
    return achieved_level


def update_role_readiness(user, skill):
    roles = skill.roles.all()

    for role in roles:
        user_role = UserRole.objects.filter(user=user, role=role).first()
        if not user_role:
            continue

        skills = role.skills.all()

        total_levels = 0
        total_possible = 0

        for s in skills:
            total_possible += s.total_levels
            user_skill = UserSkillLevel.objects.filter(user=user, skill=s).first()
            if user_skill:
                total_levels += user_skill.level

        readiness_percentage = (
            (total_levels / total_possible) * 100
            if total_possible > 0 else 0
        )

        user_role.readiness_score = round(readiness_percentage, 2)

        if readiness_percentage < 40:
            user_role.category = "Beginner"
        elif readiness_percentage < 70:
            user_role.category = "Intermediate"
        else:
            user_role.category = "Advanced"

        user_role.save()


# ===============================
# EVALUATE ASSESSMENT (FIXED)
# ===============================

def evaluate_assessment(user, skill, level, submitted_answers):

    questions = skill.questions.filter(difficulty_level=level)

    correct_count = 0
    wrong_answers = []

    for question in questions:

        selected_key = submitted_answers.get(str(question.id))
        correct_key = question.correct_option

        # Map option key → actual answer text
        option_map = {
            "A": question.option_a,
            "B": question.option_b,
            "C": question.option_c,
            "D": question.option_d,
        }

        selected_text = option_map.get(selected_key, "Not Answered")
        correct_text = option_map.get(correct_key)

        if selected_key == correct_key:
            correct_count += 1
        else:
            wrong_answers.append({
                "question": question.text,
                "selected": selected_text,
                "correct": correct_text
            })

    total_questions = questions.count()

    score = round((correct_count / total_questions) * 100) if total_questions > 0 else 0

    # Use skill's pass percentage instead of hardcoded 60
    passed = score >= skill.pass_percentage

    time_taken = int(submitted_answers.get('time_taken', 0))

    # Create attempt
    attempt = AssessmentAttempt.objects.create(
        user=user,
        skill=skill,
        level_achieved=level,
        score=score,
        correct_count=correct_count,
        total_questions=total_questions,
        passed=passed,
        time_taken=time_taken,
        wrong_answers=wrong_answers
    )

    # Update user skill level if passed
    if passed:
        user_skill, created = UserSkillLevel.objects.get_or_create(
            user=user,
            skill=skill,
        )

        if level > user_skill.level:
            user_skill.level = level
            user_skill.save()

    # Update role readiness automatically
    update_role_readiness(user, skill)

    return attempt