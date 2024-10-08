from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Machine(models.Model):
    machine_name = models.CharField(max_length=255, unique=True)
    tool_capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])  # Ensures tool capacity is positive
    tool_offset = models.FloatField(validators=[MinValueValidator(0.0)])  # Ensures no negative offsets
    feedrate = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10000)])  # Feedrate has a reasonable max limit
    tool_in_use = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])  # Range limit for tool_in_use

    created_at = models.DateTimeField(auto_now_add=True)  # Tracks when machine was created
    updated_at = models.DateTimeField(auto_now=True)  # Tracks last update time

    def __str__(self):
        return self.machine_name


class Axis(models.Model):
    class AxisType(models.TextChoices):
        X = 'X', _('X Axis')
        Y = 'Y', _('Y Axis')
        Z = 'Z', _('Z Axis')
        A = 'A', _('A Axis')
        C = 'C', _('C Axis')

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='axes')
    axis_name = models.CharField(max_length=1, choices=AxisType.choices)  # Only allow predefined axis types
    max_acceleration = models.FloatField(validators=[MinValueValidator(0.0)])  # Acceleration must be non-negative
    max_velocity = models.FloatField(validators=[MinValueValidator(0.0)])  # Velocity must be non-negative

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_axis_name_display()} - {self.machine.machine_name}"  # Get human-readable axis name


class FieldUpdate(models.Model):
    ENTITY_CHOICES = [
        ('machine', 'Machine'),
        ('axis', 'Axis'),
    ]
    entity_type = models.CharField(max_length=255, choices=ENTITY_CHOICES)
    entity_id = models.PositiveIntegerField()
    field_name = models.CharField(max_length=255)
    field_value = models.FloatField()
    update_time = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['entity_type', 'entity_id', 'field_name']),
        ]
        ordering = ['-update_time']

    def __str__(self):
        return f"Update on {self.entity_type} {self.entity_id}: {self.field_name} = {self.field_value}"
