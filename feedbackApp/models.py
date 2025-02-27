from django.db import models
from django.contrib.auth.models import User

# 📌 Şehir Modeli
class City(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Şehir isimleri benzersiz olmalı

    class Meta:
        ordering = ['name']  # Şehirleri alfabetik sırayla getir

    def __str__(self):
        return self.name

# 📌 Kullanıcı Profili Modeli
class UserProfile(models.Model):
    USER_TYPES = (('student', 'Öğrenci'), ('manager', 'Yönetici'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"

# 📌 Yemek Kategorisi Modeli
class MealCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

# 📌 Yemek Modeli
class Meal(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(MealCategory, on_delete=models.CASCADE, related_name="meals")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="meals")
    date = models.DateField()

    class Meta:
        ordering = ['-date']  # En güncel yemekleri önce göster

    def __str__(self):
        return f"{self.name} - {self.city.name} ({self.date})"

# 📌 Geri Bildirim Modeli
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedbacks")
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="feedbacks")
    comment = models.TextField()
    rating = models.IntegerField(choices=[(1, 'Kötü'), (2, 'Orta'), (3, 'İyi'), (4, 'Çok İyi'), (5, 'Mükemmel')])
    sentiment = models.CharField(max_length=10, default='Nötr')  # Gemini API duygu analizi sonucu
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)  # Yöneticinin yorumları onaylamasını sağlayabiliriz

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} -> {self.meal.name} ({self.rating})"

# 📌 Excel Yükleme Modeli
class MealImport(models.Model):
    file_path = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Excel Yükleme - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
