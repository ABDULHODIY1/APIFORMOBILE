from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
import stripe


class UserGroups(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey('auth.Group', on_delete=models.CASCADE)


class UserUserPermissions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    permission = models.ForeignKey('auth.Permission', on_delete=models.CASCADE)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='custom_user',
    )

    def __str__(self):
        return self.email


class UserActivityLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity} ({self.timestamp})"


class PasswordResetRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.token}"


class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


# Stripe API key configuration
stripe.api_key = settings.STRIPE_SECRET_KEY


class Payment(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    stripe_charge_id = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)

    def __str__(self):
        return self.user_profile.user.username


class ExternalAuth(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    another_auth = models.CharField(max_length=100)
    another_auth_id = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Goal(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserGoal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.goal.name}"


class Workout(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    level = models.CharField(max_length=50)
    duration = models.IntegerField()  # duration in minutes
    video_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class WorkoutLesson(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField()  # duration in minutes
    video_url = models.URLField()

    def __str__(self):
        return self.name


class Notification(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Insight(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.FloatField()
    workout_duration = models.IntegerField()
    calories_burned = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class UserNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.notification.title}"


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserStatistic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    steps = models.IntegerField(default=0)
    calories_burned = models.FloatField(default=0)
    exercise_duration = models.IntegerField(default=0)  # Minutes

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class Food(models.Model):
    name = models.CharField(max_length=100)
    calories = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    carbs = models.FloatField()

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    calories_burned = models.IntegerField(help_text="Calories burned")
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class MealPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    total_calories = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.FloatField()
    calories_burned = models.IntegerField()
    workout_duration = models.IntegerField(help_text="Workout duration in minutes")

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class HealthTips(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=100, choices=(
        ('nutrition', 'Nutrition'),
        ('exercise', 'Exercise'),
        ('mental_health', 'Mental Health'),
    ))

    def __str__(self):
        return self.title


class SomeModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
