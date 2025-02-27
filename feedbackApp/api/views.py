from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login
from rest_framework.decorators import action
from django.utils.timezone import now
from feedbackApp.models import Meal, Feedback
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    MealSerializer, MealCreateSerializer, FeedbackSerializer, FeedbackCreateSerializer
)
from .filters import MealFilter, FeedbackFilter
from .permissions import IsAdminUser, IsOwnerOrReadOnly
from .utils import analyze_sentiment
from rest_framework_simplejwt.tokens import RefreshToken

# 📌 Kullanıcı Kayıt API'si
class UserRegistrationView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 📌 Kullanıcı Giriş API'si
class UserLoginView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 📌 Günlük Yemekleri Listeleme API'si
class TodayMealsView(viewsets.ReadOnlyModelViewSet):
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = MealFilter
    queryset = Meal.objects.all()

    def get_queryset(self):
        user_city = self.request.user.profile.city
        return Meal.objects.filter(city=user_city, date=now().date())

# 📌 Yemek Ekleme API'si (Sadece Yöneticiler İçin)
class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Meal.objects.all()

# 📌 Kullanıcı Geri Bildirim API'si
class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = FeedbackFilter

    def get_queryset(self):
        return Feedback.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        comment = self.request.data.get("comment")
        sentiment = analyze_sentiment(comment)
        serializer.save(user=self.request.user, sentiment=sentiment)

# 📌 Geri Bildirim Yönetim API'si (Sadece Yöneticiler)
class ManageFeedbackView(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Feedback.objects.filter(is_approved=False)

    @action(detail=True, methods=['patch'])
    def approve(self, request, pk=None):
        feedback = self.get_object()
        feedback.is_approved = True
        feedback.save()
        return Response({"status": "Geri bildirim onaylandı!"}, status=status.HTTP_200_OK)
