import uuid
from django.db import models
from django.utils import timezone


class User(models.Model):
	id = models.UUIDField(primary_key=True, unique=True, editable=False, max_length=21, default=uuid.uuid4, auto_created=True)
	f_name = models.CharField(max_length=255, null=True, blank=True, unique=False)
	l_name = models.CharField(max_length=255, null=True, blank=True, unique=False)
	created_at = models.DateTimeField(default=timezone.now, null=False, blank=False, unique=False)
	class Meta:
		app_label = "API"

