# serializers.py
from rest_framework import serializers
from .models import CustomUser, GaitParameter, HistoryRecord, IssueAndSuggestion

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_id', 'username', 'date_of_birth', 'gender', 'role', 'notes', 'is_active', 'deactivated_at']

class GaitParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = GaitParameter
        fields = ['gait_parameter_id', 'measurement_time', 'video_name', 'json_name', 'user_name',
                  'average_step_time', 'average_stride_length', 'movement_speed', 'stance', 
                  'health_value', 'each_of_step_length', 'y_values', 'left_y_value']

class HistoryRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryRecord
        fields = ['record_id', 'user', 'gait_parameter', 'issue_id', 'record_time']

class IssueAndSuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueAndSuggestion
        fields = ['issue_id', 'issue_name', 'record', 'suggestion']
