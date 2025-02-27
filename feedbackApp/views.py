from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, View
from django.utils.timezone import now
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Meal, Feedback, MealImport
from .forms import RegisterForm, LoginForm, FeedbackForm, MealImportForm

# 📌 Ana Sayfa
class HomeView(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meals"] = Meal.objects.filter(date=now().date())
        return context
    
# 📌 Kullanıcı Giriş Sayfası
class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        messages.error(request, "Kullanıcı adı veya şifre hatalı!")
        return render(request, self.template_name, {"form": form})

class AdminLoginView(View):
    template_name = "authentication/admin_login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:  # Yalnızca admin kullanıcıları giriş yapabilir
            login(request, user)
            return redirect("admin-dashboard")
        
        messages.error(request, "Geçersiz kullanıcı adı veya şifre!")
        return render(request, self.template_name)
# 📌 Kullanıcı Kayıt Sayfası
class RegisterView(View):
    template_name = "register.html"

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        return render(request, self.template_name, {"form": form})

# 📌 Şifre Sıfırlama Sayfası
class PasswordResetView(TemplateView):
    template_name = "password_reset.html"

# 📌 Günlük Yemek Listesi
class MealListView(LoginRequiredMixin, ListView):
    template_name = "meal_list.html"
    model = Meal
    context_object_name = "meals"

    def get_queryset(self):
        return Meal.objects.filter(city=self.request.user.profile.city, date=now().date())

# 📌 Yemek Detay Sayfası
class MealDetailView(LoginRequiredMixin, DetailView):
    template_name = "meal_detail.html"
    model = Meal
    context_object_name = "meal"

# 📌 Geri Bildirim Formu
class FeedbackFormView(LoginRequiredMixin, CreateView):
    template_name = "feedback_form.html"
    model = Feedback
    form_class = FeedbackForm
    success_url = reverse_lazy("feedback-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# 📌 Kullanıcının Geri Bildirimleri
class FeedbackListView(LoginRequiredMixin, ListView):
    template_name = "feedback_list.html"
    model = Feedback
    context_object_name = "feedbacks"

    def get_queryset(self):
        return Feedback.objects.filter(user=self.request.user)

# 📌 Yönetici Paneli
class AdminDashboardView(UserPassesTestMixin, TemplateView):
    template_name = "admin_dashboard.html"

    def test_func(self):
        return self.request.user.profile.user_type == "manager"

# 📌 Geri Bildirim Yönetimi (Yöneticiler İçin)
class FeedbackManagementView(UserPassesTestMixin, ListView):
    template_name = "feedback_management.html"
    model = Feedback
    context_object_name = "feedbacks"

    def test_func(self):
        return self.request.user.profile.user_type == "manager"

    def get_queryset(self):
        return Feedback.objects.filter(is_approved=False)

# 📌 Excel Dosyası ile Yemek Yükleme
class MealUploadView(UserPassesTestMixin, CreateView):
    template_name = "meal_upload.html"
    model = MealImport
    form_class = MealImportForm
    success_url = reverse_lazy("admin-dashboard")

    def test_func(self):
        return self.request.user.profile.user_type == "manager"

# 📌 Haftalık/Aylık Raporlar (Yöneticiler İçin)
class ReportsView(UserPassesTestMixin, TemplateView):
    template_name = "reports.html"

    def test_func(self):
        return self.request.user.profile.user_type == "manager"


class LogoutViewCustom(View):
    def get(self, request):
        logout(request)
        return redirect("home") 


class ApproveFeedbackView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.profile.user_type == "manager"

    def get(self, request, pk):
        feedback = get_object_or_404(Feedback, pk=pk)
        feedback.is_approved = True
        feedback.save()
        return redirect("feedback-management")