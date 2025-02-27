from rest_framework import serializers
from feedbackApp.models import City, UserProfile, MealCategory, Meal, Feedback, MealImport
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# 📌 Kullanıcı Serializer (User Modeli için)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# 📌 Şehir Serializer (City Modeli için)
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

# 📌 Kullanıcı Profili Serializer (UserProfile Modeli için)
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'user_type', 'city']

# 📌 Yemek Kategorisi Serializer (MealCategory Modeli için)
class MealCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MealCategory
        fields = '__all__'

# 📌 Yemek Serializer (Meal Modeli için)
class MealSerializer(serializers.ModelSerializer):
    category = MealCategorySerializer(read_only=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = Meal
        fields = ['id', 'name', 'category', 'city', 'date']

# 📌 Yemek Oluşturma Serializer (Kategori ve Şehir ID’sini Alır)
class MealCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['name', 'category', 'city', 'date']

# 📌 Geri Bildirim Serializer (Feedback Modeli için)
class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    meal = MealSerializer(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'meal', 'comment', 'rating', 'sentiment', 'is_approved', 'created_at']

# 📌 Geri Bildirim Oluşturma Serializer (Yemek ID'si Alır)
class FeedbackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'meal', 'comment', 'rating']
        
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user  # Kullanıcı otomatik atanıyor
        return super().create(validated_data)    

# 📌 Excel Yükleme Serializer (MealImport Modeli için)
class MealImportSerializer(serializers.ModelSerializer):
    uploaded_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = MealImport
        fields = ['id', 'file_path', 'uploaded_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password": "Şifreler eşleşmiyor!"})
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError({"error": "Kullanıcı adı veya şifre yanlış!"})
        return {"user": user}

        
        