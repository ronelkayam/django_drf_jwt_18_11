from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Workout

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,min_length = 4)

    class Meta:
        model = User
        fields = ['username','email','password']

    def create(self, validated_data):
        #יוצר לי משתמש וסיסמא מוצפנת בלי טקסט גלוי
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'])
        return user

class WorkoutSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Workout
        fields = ['id','username','exercise_name','weight_kg','reps','sets','created_at']
        read_only_fields = ['id','username','created_at']


    def validate_weight(self, value):
        if value < 0:
            raise serializers.ValidationError('Weight must be greater than 0')
        return value

    def validate_reps(self, value):
        if value <= 0:
            raise serializers.ValidationError('Reps must be greater than 0')
        return value
