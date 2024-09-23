from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (User,
                     UserGoal,
                     UserProfile,
                     UserNotification,
                     UserStatistic,
                     ExternalAuth,
                     Workout,
                     WorkoutLesson,
                     Notification,
                     Insight,
                     Goal,
                     Payment,
                     Post)

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(ExternalAuth)
admin.site.register(UserGoal)
admin.site.register(Workout)
admin.site.register(WorkoutLesson)
admin.site.register(Notification)
admin.site.register(Insight)
admin.site.register(UserNotification)
admin.site.register(Goal)
admin.site.register(Payment)
admin.site.register(User, UserAdmin)
admin.site.register(UserStatistic)

# Postlar
admin.site.register(Post)