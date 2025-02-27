from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserRegistrationView, UserLoginView, TodayMealsView, MealViewSet, 
    FeedbackViewSet, ManageFeedbackView
)

router = DefaultRouter()
router.register(r'register', UserRegistrationView, basename='register')
router.register(r'login', UserLoginView, basename='login')
router.register(r'today-meals', TodayMealsView, basename='today-meals')
router.register(r'meals', MealViewSet, basename='meals')
router.register(r'feedbacks', FeedbackViewSet, basename='feedbacks')
router.register(r'manage-feedbacks', ManageFeedbackView, basename='manage-feedbacks')

urlpatterns = [
    # 📌 Kullanıcı Kimlik Doğrulama
    
    path('', include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

 
]
