
from django.contrib import admin
from .models import Patient, Doctor, Specialty, User


# Gestion des utilisateurs
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'is_active',
        'is_staff',
    )

    search_fields = ('username', 'first_name', 'last_name', 'email')

    list_filter = ('is_active', 'is_staff')

    ordering = ('username',)


# Gestion des médecins
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'license_number',
        'phone',
        'created_at',
    )

    search_fields = (
        'username',
        'first_name',
        'last_name',
        'license_number',
        'phone',
    )

    list_filter = ('created_at', 'is_active')

    ordering = ('-created_at',)


# Gestion des patients
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'national_id',
        'phone',
        'birth_date',
        'created_at',
    )

    search_fields = (
        'username',
        'first_name',
        'last_name',
        'national_id',
        'phone',
    )

    list_filter = ('birth_date', 'created_at')

    ordering = ('-created_at',)


# Gestion des spécialités
@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

    search_fields = ('name',)

    ordering = ('name',)
