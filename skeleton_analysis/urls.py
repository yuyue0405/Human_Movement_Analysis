# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, GaitParameterViewSet, HistoryRecordViewSet, IssueAndSuggestionViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='customuser')
router.register(r'gaitparameters', GaitParameterViewSet, basename='gaitparameter')
router.register(r'historyrecords', HistoryRecordViewSet, basename='historyrecord')
router.register(r'issuesuggestions', IssueAndSuggestionViewSet, basename='issueandsuggestion')

urlpatterns = [
    path('api/', include(router.urls)),  # 所有API路徑都通過這個路由器
]
