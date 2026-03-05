# from django.contrib import admin
# from .models import Role, Skill, Question, AssessmentAttempt, UserSkillLevel, UserRole


# @admin.register(Role)
# class RoleAdmin(admin.ModelAdmin):
#     list_display = ('name',)


# @admin.register(Skill)
# class SkillAdmin(admin.ModelAdmin):
#     list_display = ('name', 'display_roles', 'pass_percentage', 'total_levels')
#     list_filter = ('roles',)

#     def display_roles(self, obj):
#         return ", ".join(role.name for role in obj.roles.all())

#     display_roles.short_description = 'Roles'

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ('skill', 'difficulty_level', 'text')
#     list_filter = ('skill', 'difficulty_level')


# @admin.register(AssessmentAttempt)
# class AssessmentAttemptAdmin(admin.ModelAdmin):
#     list_display = ('user', 'skill', 'score', 'level_achieved', 'passed', 'attempted_at')
#     list_filter = ('skill', 'passed')


# @admin.register(UserSkillLevel)
# class UserSkillLevelAdmin(admin.ModelAdmin):
#     list_display = ('user', 'skill', 'level', 'updated_at') 

# admin.site.register(UserRole)

from django.contrib import admin
from .models import Role, Skill, Question, AssessmentAttempt, UserSkillLevel, UserRole


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_roles', 'pass_percentage', 'total_levels')
    list_filter = ('roles',)

    def display_roles(self, obj):
        return ", ".join(role.name for role in obj.roles.all())

    display_roles.short_description = 'Roles'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('skill', 'difficulty_level', 'text')
    list_filter = ('skill', 'difficulty_level')


@admin.register(AssessmentAttempt)
class AssessmentAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'score', 'level_achieved', 'passed', 'attempted_at')
    list_filter = ('skill', 'passed')


@admin.register(UserSkillLevel)
class UserSkillLevelAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'level', 'updated_at')


admin.site.register(UserRole)