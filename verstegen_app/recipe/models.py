
from django.db import models
from django.urls import reverse

import uuid

from costing.models import Costing 
from ingredients.models import Ingredients

STATUS = ((0, 'Draft'), (1 , 'Published'), (2, 'Archived'), (3, 'Deleted'), (4, 'Revised'), (5, 'Under Review'))


class Recipe(models.Model):
    """
        Main Recipe model
    """

    recipe_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(max_length=100)
    author = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True) 
    ingredients = models.ForeignKey(Ingredients, blank=True, null=True, on_delete=models.SET_NULL)
    method = models.TextField(max_length=1000)
    category = models.ForeignKey('Recipe_Category', null=True, blank=True, on_delete=models.SET_NULL)
    portion_weight = models.FloatField()
    prep_time = models.DurationField()
    cook_time = models.DurationField()
    other_items = models.TextField(max_length=1000, blank=True, null=True)
    costing = models.ForeignKey(Costing, null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(blank=True, null=True)
    image_url = models.URLField(max_length=1024, blank=True, null=True)
    published = models.IntegerField(choices=STATUS,default=False)
    meta_description = models.TextField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['-date_created']
        verbose_name_plural = 'Recipes'
        verbose_name = 'Recipe'

    def __str__(self):
        return self.name
    
    def get_authgr(self):
        return self.author
    
    def get_absolute_url(self):
        return reverse('recipe_detail', args=[self.id])


class Recipe_Category(models.Model):
    """
        Verstegen Recipe Categories
    """

    name = models.TextField(max_length=50)
    friendly_name = models.TextField(max_length=50, null=True, blank=True)
    image = models.ImageField(blank=True, null=True)
    image_url = models.URLField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_friendly(self):
        return self.friendly_name
    
    def get_absolute_url(self):
        return reverse('recipe_category_detail', args=[self.id])
    
    class Meta:
        verbose_name_plural = 'Recipe Category'
        verbose_name = 'Recipe Category'
        ordering = ['-name']