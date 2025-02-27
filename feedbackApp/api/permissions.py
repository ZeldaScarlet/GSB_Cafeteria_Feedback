from rest_framework.permissions import BasePermission

# 📌 Yalnızca Yöneticiler İçin
class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.user_type == 'manager'

# 📌 Yalnızca Kullanıcının Kendi Yorumlarını Düzenlemesine İzin Ver
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:  # Okuma izinleri herkese açık
            return True
        return obj.user == request.user  # Kullanıcı sadece kendi yorumunu düzenleyebilir
