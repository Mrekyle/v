from django.db import models
from django.urls import reverse

from costing.models import Costing

class Ingredients(models.Model):
    """
        Ingredient database for recipe creation
    """

    vegetable = models.ForeignKey('Vegetable', blank=True, null=True, on_delete=models.SET_NULL)
    fruit = models.ForeignKey('Fruit', blank=True, null=True, on_delete=models.SET_NULL)
    protein = models.ForeignKey('Protein', blank=True, null=True, on_delete=models.SET_NULL)
    verstegen_product = models.ForeignKey('Products', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'Ingredients'
        verbose_name = 'Ingredient'
        ordering = ['-vegetable', '-fruit', '-protein', '-verstegen_product']

class Products(models.Model):
    """
        Verstegen Main Products
    """

    name = models.TextField(max_length=100)
    category = models.ForeignKey('Product_Category', null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    weight = models.FloatField()
    allergen = models.ForeignKey('Allergens', blank=True, null=True, on_delete=models.SET_NULL)
    product_link = models.URLField(max_length=1024, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    image_url = models.URLField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products_detail', args=[self.id])

    class Meta:
        verbose_name_plural = 'Products'
        verbose_name = 'Product'
        ordering = ['-name']

class Product_Category(models.Model):
    """
        Verstegen Product Categories
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
        return reverse('product_category_detail', args=[self.id])
    
    class Meta:
        verbose_name_plural = 'Product Category'
        verbose_name = 'Product Category'
        ordering = ['-name']


class Vegetable(models.Model):
    """
        Vegetables
    """

    name = models.CharField(max_length=100)
    weight = models.FloatField()
    cost = models.ForeignKey(Costing, blank=True, null=True, on_delete=models.SET_NULL)
    allergen = models.ForeignKey('Allergens', blank=True, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(blank=True, null=True)
    image_url = models.URLField(max_length=1024, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('vegetable_detail', args=[self.id])
    
    class Meta:
        verbose_name_plural = 'Vegetables'
        verbose_name = 'Vegetable'
        ordering = ['-name']

class Fruit(models.Model):
    """
        Fruit
    """

    name = models.CharField(max_length=100)
    weight = models.FloatField()
    cost = models.ForeignKey(Costing, blank=True, null=True, on_delete=models.SET_NULL)
    allergen = models.ForeignKey('Allergens', blank=True, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(blank=True, null=True)
    image_url = models.URLField(max_length=1024, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('fruit_detail', args=[self.id])
    
    class Meta:
        verbose_name_plural = 'Fruits'
        verbose_name = 'Fruit'
        ordering = ['-name']

class Protein(models.Model):
    """
        Protein
    """

    name = models.CharField(max_length=100)
    weight = models.FloatField()
    cost = models.ForeignKey(Costing, blank=True, null=True, on_delete=models.SET_NULL)
    allergen = models.ForeignKey('Allergens', blank=True, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(blank=True, null=True)
    image_url = models.URLField(max_length=1024, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('protein_detail', args=[self.id])
    
    class Meta:
        verbose_name_plural = 'Proteins'
        verbose_name = 'Protein'
        ordering = ['-name']


class Allergens(models.Model):
    """
        Food Allergens
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
        return reverse('allergens_detail', args=[self.id])
    
    class Meta:
        verbose_name_plural = 'Allergens'
        verbose_name = 'Allergen'
        ordering = ['-name']

