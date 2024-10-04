from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

import shortuuid
from django_countries.fields import CountryField
from autoslug import AutoSlugField


CONTINENTS = (
    ('AF', 'Africa'),
    ('AN', 'Antarctica'),
    ('AS', 'Asia'),
    ('EU', 'Europe'),
    ('NA', 'North America'),
    ('SA', 'South America'),
    ('OC', 'Oceania'),
)


class League(models.Model):
    id = models.CharField(_(u'id'),
                          primary_key=True,
                          max_length=255,
                          default=shortuuid.ShortUUID().random(4),
                          help_text=u'League ID',
                          db_index=True)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)
    short_name = models.CharField(max_length=255)
    logo = models.URLField(blank=True, null=True)
    country = CountryField()
    continent = models.CharField(max_length=2, choices=CONTINENTS, default='AF')
    description = models.TextField(blank=True, null=True)
    year_established = models.SmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('league-detail', args=[str(self.slug)])
    
    def get_update_url(self):
        return reverse('league-update', args=[str(self.slug)])
    
    def get_delete_url(self):
        return reverse('league-delete', args=[str(self.slug)])
    
    def get_create_url(self):
        return reverse('league-create')
    
    def get_list_url(self):
        return reverse('league-list')
    
    def get_country_name(self):
        return self.country.name
    
    def get_country_code(self):
        return self.country.alpha_2