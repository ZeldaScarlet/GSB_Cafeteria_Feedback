from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    HomeView, LoginView, RegisterView, PasswordResetView, LogoutViewCustom,
    MealListView, MealDetailView, FeedbackFormView, FeedbackListView,
    AdminDashboardView, FeedbackManagementView, MealUploadView, ReportsView, ApproveFeedbackView,
AdminLoginView
)

urlpatterns = [
    # 📌 Genel Sayfalar
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutViewCustom.as_view(), name="logout"),
    path("password-reset/", PasswordResetView.as_view(), name="password-reset"),

    # 📌 Yemek Sayfaları
    path("meals/", MealListView.as_view(), name="meal-list"),
    path("meals/<int:pk>/", MealDetailView.as_view(), name="meal-detail"),

    # 📌 Geri Bildirim Sayfaları
    path("feedback/", FeedbackFormView.as_view(), name="feedback-form"),
    path("feedback/list/", FeedbackListView.as_view(), name="feedback-list"),

    # 📌 Yönetici Paneli
    path("admin/dashboard/", AdminDashboardView.as_view(), name="admin-dashboard"),
    path("admin/feedbacks/", FeedbackManagementView.as_view(), name="feedback-management"),
    path("admin/feedbacks/<int:pk>/approve/", ApproveFeedbackView.as_view(), name="approve-feedback"),  # 📌 Yeni Eklendi!
    path("admin/meal-upload/", MealUploadView.as_view(), name="meal-upload"),
    path("admin/reports/", ReportsView.as_view(), name="reports"),
    path('admin-login/', AdminLoginView.as_view(), name='admin-login'),
]
