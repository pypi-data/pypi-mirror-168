from django.db import models
from jsonfield import JSONField

class MigrationCheckpoint(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now=True)
    migrations = JSONField(default={})