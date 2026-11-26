from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone


class Appointment(models.Model):
    reason = models.TextField()
    prescription = models.FileField(
        blank=True,
        upload_to='prescriptions/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
    )

    class Status(models.TextChoices):
        PENDING = 'pending', "En attente"
        CONFIRMED = 'confirmed', "Confirmé"
        CANCELLED = 'cancelled', "Annulé"

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    duration_minutes = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    appointment_date = models.DateTimeField()
    doctor = models.ForeignKey(
        'AccountApp.Doctor',
        on_delete=models.CASCADE,
        related_name='appointments',
    )
    patient = models.ForeignKey(
        'AccountApp.Patient',
        on_delete=models.CASCADE,
        related_name='appointments',
    )

    def clean(self):
        super().clean()
        if self.appointment_date is None:
            return

        if self._state.adding:
            date_changed = True
        else:
            previous_date = type(self).objects.filter(pk=self.pk).values_list(
                'appointment_date',
                flat=True,
            ).first()
            date_changed = previous_date != self.appointment_date

        if date_changed and self.appointment_date <= timezone.now():
            raise ValidationError({
                'appointment_date': "La date du rendez-vous doit être dans le futur."
            })

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.appointment_date:%Y-%m-%d %H:%M}"

    class Meta:
        ordering = ['-appointment_date']
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_appointment_per_doctor',
                violation_error_message="Un rendez-vous existe déjà pour ce médecin à cette date et heure.",
            ),
        ]