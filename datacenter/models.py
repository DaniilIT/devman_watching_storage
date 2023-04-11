from django.db import models
from datetime import timedelta
from django.utils import timezone

class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )

    def get_duration(self):
        time_end = timezone.localtime(self.leaved_at) if self.leaved_at else timezone.now()
        time_entered_at = timezone.localtime(self.entered_at)
        duration = time_end - time_entered_at
        return duration.total_seconds()

    @staticmethod
    def format_duration(duration):
        return f'{duration // 3600 :02.0f}:{(duration % 3600) // 60 :02.0f}'

    def is_long(self, minutes=60):
        return self.get_duration() > (minutes * 60)
      