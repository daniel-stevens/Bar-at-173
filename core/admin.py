# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User, Drink, Session, Consumption

# Customize the User admin to include the avatar field
class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

class UserProfileAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'avatar_thumb')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': ('avatar',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('username', 'email', 'password1', 'password2', 'avatar')}),
    )
    readonly_fields = []
    # Custom method to display a thumbnail of avatar in list display
    def avatar_thumb(self, obj):
        if obj.avatar:
            return f'<img src="{obj.avatar.url}" alt="avatar" style="height:50px;width:50px;border-radius:50%;" />'
        return ""
    avatar_thumb.allow_tags = True
    avatar_thumb.short_description = "Avatar"

admin.site.register(User, UserProfileAdmin)
admin.site.register(Drink)
admin.site.register(Session)
admin.site.register(Consumption)
