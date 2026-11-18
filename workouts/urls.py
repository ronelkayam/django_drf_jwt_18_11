from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView,WorkoutListCreateView,AuditLogView

urlpatterns = [
    #JWT נתיבי אימות (צמיד VIP(
    path('register/', RegisterView.as_view(),name='auth_register'),
    path('login', TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),name='token_refresh'),

    #app url, save by JWT
    path('workouts/', WorkoutListCreateView.as_view(),name='workouts_list_created'),
    path('logs/', AuditLogView.as_view(),name='mongo_audit_log'),

]