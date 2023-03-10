from django.conf import settings
from django.db import models
from django.utils import timezone


class Note(models.Model):
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Created at'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name='Created by'
    )
    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
