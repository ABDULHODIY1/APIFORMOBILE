from rest_framework import serializers
from .models import (UserProfile, ExternalAuth, Goal, UserGoal,
                     Workout, WorkoutLesson, Notification, Insight,
                     UserNotification, UserStatistic, Food, Payment,
                     Post, UserActivityLog, Exercise, MealPlan, 
                     UserProgress, HealthTips,User)

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import SomeModel
from rest_framework import serializers
from .models import UserActivityLog, PasswordResetRequest

class UserActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivityLog
        fields = '__all__'

class PasswordResetRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResetRequest
        fields = '__all__'

class SomeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SomeModel
        fields = '__all__'

# Registrations va boshqa API-lar

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # yoki kerakli maydonlar ro'yxatini ko'rsating

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField()

class UserActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivityLog
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        user_profile = UserProfile.objects.create(user=user, **validated_data)
        return user_profile

class ExternalAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalAuth
        fields = '__all__'

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'

class UserGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGoal
        fields = '__all__'

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = '__all__'

class WorkoutLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutLesson
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'text', 'type', 'created_at', 'updated_at']

class InsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insight
        fields = '__all__'

class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotification
        fields = ['id', 'user', 'notification']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class UserStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatistic
        fields = ['id', 'user', 'date', 'steps', 'calories_burned', 'exercise_duration']

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

class MealPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPlan
        fields = '__all__'

class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = '__all__'

class HealthTipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthTips
        fields = '__all__'
