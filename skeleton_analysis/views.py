# views.py
from rest_framework import viewsets
from .models import CustomUser, GaitParameter, HistoryRecord, IssueAndSuggestion
from .serializers import CustomUserSerializer, GaitParameterSerializer, HistoryRecordSerializer, IssueAndSuggestionSerializer

# 用戶 ViewSet
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

# 步態參數 ViewSet
class GaitParameterViewSet(viewsets.ModelViewSet):
    queryset = GaitParameter.objects.all()
    serializer_class = GaitParameterSerializer

# 歷史紀錄 ViewSet
class HistoryRecordViewSet(viewsets.ModelViewSet):
    queryset = HistoryRecord.objects.all()
    serializer_class = HistoryRecordSerializer

# 問題與建議 ViewSet
class IssueAndSuggestionViewSet(viewsets.ModelViewSet):
    queryset = IssueAndSuggestion.objects.all()
    serializer_class = IssueAndSuggestionSerializer
