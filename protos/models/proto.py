from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gismodels


class ProtoQuerySet(gismodels.QuerySet):
    def delete(self):
        self.update(deleted_at=datetime.utcnow())


class ProtoActiveManager(gismodels.Manager):
    def active(self):
        return self.model.objects.filter(deleted_at__isnull=True)

    def get_queryset(self):
        return ProtoQuerySet(self.model, using=self._db)


class Proto(gismodels.Model):
    name = gismodels.CharField(max_length=128, null=False, blank=False)
    desc = gismodels.TextField(null=True, blank=True)

    created_by = gismodels.ForeignKey(User, null=True, blank=True, related_name='+')
    created_at = gismodels.DateTimeField(auto_now_add=True, blank=True, null=True)

    updated_by = gismodels.ForeignKey(User, null=True, blank=True, related_name='+')
    updated_at = gismodels.DateTimeField(auto_now=True, blank=True, null=True)

    deleted_by = gismodels.ForeignKey(User, null=True, blank=True, related_name='+')
    deleted_at = gismodels.DateTimeField(blank=True, null=True)

    objects = ProtoActiveManager()

    class Meta:
        abstract = True


class GeoProto(Proto, gismodels.Model):
    point = gismodels.PointField(srid=4326)

    class Meta:
        abstract = True
