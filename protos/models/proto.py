from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.contrib.gis.db import models as geomodels


class ProtoQuerySet(QuerySet):
    def delete(self):
        self.update(deleted_at=datetime.utcnow())


class ProtoActiveManager(models.Manager):
    def active(self):
        return self.model.objects.filter(deleted_at__isnull=True)

    def get_queryset(self):
        return ProtoQuerySet(self.model, using=self._db)


class Proto(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    desc = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(User, null=True, blank=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    updated_by = models.ForeignKey(User, null=True, blank=True, related_name='+')
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    deleted_by = models.ForeignKey(User, null=True, blank=True, related_name='+')
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = ProtoActiveManager()

    class Meta:
        abstract = True


class GeoProto(Proto, geomodels.Model):
    point = geomodels.PointField(srid=4326)

    class Meta:
        abstract = True
