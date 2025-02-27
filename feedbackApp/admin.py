from django.contrib import admin
from .models import City, UserProfile, MealCategory, Meal, Feedback, MealImport

# 📌 Şehir Modeli Admin Paneli
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # ID ve Şehir adı gösterilecek
    search_fields = ('name',)  # Şehir adına göre arama yapılabilecek
    ordering = ('name',)

# 📌 Kullanıcı Profili Admin Paneli
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'city')  # Kullanıcı, Türü ve Şehri göster
    list_filter = ('user_type', 'city')  # Kullanıcı türüne ve şehre göre filtreleme
    search_fields = ('user__username', 'city__name')  # Kullanıcı adına ve şehir adına göre arama

# 📌 Yemek Kategorisi Admin Paneli
@admin.register(MealCategory)
class MealCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # ID ve Kategori adı göster
    search_fields = ('name',)  # Kategori adına göre arama

# 📌 Yemek Modeli Admin Paneli
@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'city', 'date')  # ID, Yemek Adı, Kategori, Şehir, Tarih
    list_filter = ('category', 'city', 'date')  # Kategori, Şehir ve Tarihe göre filtreleme
    search_fields = ('name', 'city__name', 'category__name')  # Yemek, şehir ve kategori adına göre arama
    ordering = ('-date',)  # En güncel yemekler en üstte görünecek

# 📌 Geri Bildirim Modeli Admin Paneli
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'meal', 'rating', 'sentiment', 'is_approved', 'created_at')
    list_filter = ('sentiment', 'is_approved', 'rating')  # Duygu analizi, onay durumu ve puana göre filtreleme
    search_fields = ('user__username', 'meal__name', 'comment')  # Kullanıcı adı, yemek adı ve yorum içeriğine göre arama
    ordering = ('-created_at',)  # En güncel yorumlar en üstte görünecek
    list_editable = ('is_approved',)  # Admin panelinden geri bildirimleri hızlıca onaylamak için

# 📌 Excel Yükleme Modeli Admin Paneli
@admin.register(MealImport)
class MealImportAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_path', 'uploaded_at')  # ID, Dosya Yolu ve Yükleme Tarihi
    ordering = ('-uploaded_at',)  # En son yüklenen dosyalar en üstte görünecek
