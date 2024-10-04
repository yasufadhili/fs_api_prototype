from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

import shortuuid
from django_countries.fields import CountryField
from autoslug import AutoSlugField

from leagues.models import League


class Club(models.Model):
    id = models.CharField(_(u'id'),
                          primary_key=True,
                          max_length=255,
                          default=shortuuid.ShortUUID().random(4),
                          help_text=u'Club ID',
                          db_index=True)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)
    full_name = models.CharField(max_length=155)
    short_name = models.CharField(max_length=55)
    logo = models.URLField(blank=True, null=True)
    year_established = models.SmallIntegerField(blank=True, null=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, **kwargs):
        self.slug = slugify(self.name)
        super().save()