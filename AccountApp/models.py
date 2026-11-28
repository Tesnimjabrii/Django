from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError


class User(AbstractUser):
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"


class Specialty(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "specialty"
        verbose_name_plural = "specialties"

    def __str__(self):
        return self.name


class Doctor(User):
    license_number = models.CharField(
        max_length=6,
        unique=True,
        validators=[MinLengthValidator(6)],
    )
    phone = models.CharField(
        max_length=8,
        validators=[RegexValidator(r'^\d{8}$')],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Médecin"
        verbose_name_plural = "Médecins"
    specialties = models.ManyToManyField(Specialty, related_name='doctors')


def validate_past_date(value):
    if value >= timezone.localdate():
        raise ValidationError("La date de naissance doit être antérieure à aujourd'hui.")

# Compatibilité avec l'ancienne migration
validate_birth_date = validate_past_date

class Patient(User):
    national_id = models.CharField(
        max_length=8,
        unique=True,
        validators=[RegexValidator(r'^\d{8}$')],
    )
    phone = models.CharField(
        max_length=8,
        validators=[RegexValidator(r'^\d{8}$')],
    )
    birth_date = models.DateField(validators=[validate_past_date])
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
    updated_at = models.DateTimeField(auto_now=True)