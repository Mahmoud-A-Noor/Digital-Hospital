from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    list_filter = ["is_staff"]
    fieldsets = [
        ("Email Related Info", {"fields": ["email", "password"]}),
        (
            "Personal Info",
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "date_of_birth",
                    "gender",
                    "address",
                    "phone_number"
                ],
            },
        ),
        (
            "Additional Info",
            {
                "fields": [
                    "username",
                    "user_type",
                    "img"
                ],
            },
        )
    ]
    add_fieldsets = [
        (
            None,
            {
                "fields": [
                    "email",
                    "first_name",
                    "last_name",
                    "date_of_birth",
                    "gender",
                    "user_type",
                    "phone_number",
                    "password1",
                    "password2",
                ]
            },
        ),
    ]


admin.site.register(CustomUser, CustomUserAdmin)
