from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from .models import Programme, Faculty, ApplicationUser, Application, CustomUser, ApplicationIssue

# Group modelini admin paneldan olib tashlaymiz
admin.site.unregister(Group)

# Custom User admin paneli
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'birthdate', 'middle_name', 'phone_number']
    search_fields = ['username', 'email']
    list_filter = ['username']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'middle_name', 'email', 'birthdate', 'phone_number')
        }),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'birthdate', 'middle_name', 'phone_number'),
        }),
    )

# ApplicationUser admin paneli
class ApplicationUserAdmin(admin.ModelAdmin):
    list_display = ['user_link', 'get_application_info', 'timestamp']
    search_fields = ['user__username', 'application__passport_serial']
    list_filter = ['timestamp']

    def user_link(self, obj):
        if obj.application:
            app_label = obj.application._meta.app_label
            model_name = obj.application._meta.model_name
            url = f"/admin/{app_label}/{model_name}/{obj.application.id}/change/"
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return obj.user.username

    user_link.short_description = "User (Click for Application)"

    def get_application_info(self, obj):
        if obj.application:
            app_label = obj.application._meta.app_label
            model_name = obj.application._meta.model_name
            return format_html(
                '<a href="/admin/{}/{}/{}/change/">{} (Status: {})</a>',
                app_label,
                model_name,
                obj.application.id,
                obj.application.passport_serial,
                obj.application.status
            )
        return 'No Application'

    get_application_info.short_description = 'Application Info'

    def delete_model(self, request, obj):
        if obj.application:
            obj.application.delete()
        super().delete_model(request, obj)

# Application admin paneli (shart, chunki bo'lmasa 404 bo'ladi!)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['passport_serial', 'status', 'timestamp']
    search_fields = ['passport_serial']

# Barcha model adminlarini ro'yxatdan o'tkazamiz
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ApplicationUser, ApplicationUserAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(ApplicationIssue)
admin.site.register(Programme)
admin.site.register(Faculty)
