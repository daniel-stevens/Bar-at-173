# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.html import format_html

from .models import User, Drink, Session, Consumption


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


@admin.register(User)
class UserProfileAdmin(DjangoUserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = User

    # -------- list view --------
    list_display = (
        "username", "email", "first_name", "last_name",
        "is_staff", "avatar_thumb",
    )
    list_filter = ("is_staff", "is_superuser", "is_active")

    # -------- detail (change) view --------
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "avatar")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser",
                                    "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # -------- add-user form --------
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "avatar"),
        }),
    )

    # no read-only extras, so leave readonly_fields empty
    readonly_fields = ()

    # helper: thumbnail in list_display
    def avatar_thumb(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:50%;" />',
                obj.avatar.url,
            )
        return "—"
    avatar_thumb.short_description = "Avatar"


# --------------------------------------------------------------------
#  Register the remaining models with vanilla admins
# --------------------------------------------------------------------
admin.site.register(Drink)
admin.site.register(Session)
admin.site.register(Consumption)
