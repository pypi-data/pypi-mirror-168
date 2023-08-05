from django.db.models.manager import BaseManager
from guardian_queryset.queryset import GuardianQuerySet, ForeignKeyGuardienQuerSet
from django.db import models

class GuardianManager(BaseManager.from_queryset(GuardianQuerySet), models.Manager):
    pass

class ForeignKeyGuardianManager(BaseManager.from_queryset(ForeignKeyGuardienQuerSet), models.Manager):
    pass


