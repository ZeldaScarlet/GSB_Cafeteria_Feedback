import django_filters
from feedbackApp.models import Meal, Feedback

# 📌 Yemek Filtreleme (Şehir, Kategori, Tarih)
class MealFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__name", lookup_expr='iexact')
    city = django_filters.CharFilter(field_name="city__name", lookup_expr='iexact')
    date = django_filters.DateFilter(field_name="date")

    class Meta:
        model = Meal
        fields = ['category', 'city', 'date']

# 📌 Geri Bildirim Filtreleme (Duygu, Puan, Onay Durumu)
class FeedbackFilter(django_filters.FilterSet):
    sentiment = django_filters.CharFilter(field_name="sentiment", lookup_expr='iexact')
    rating = django_filters.NumberFilter(field_name="rating")
    is_approved = django_filters.BooleanFilter(field_name="is_approved")

    class Meta:
        model = Feedback
        fields = ['sentiment', 'rating', 'is_approved']
