from django.db import models
from django.urls import reverse

class Costing(models.Model):
    """
        Recipe costing 
    """

    cost_per_portion = models.DecimalField(max_digits=6, decimal_places=2)
    recipe_cost = models.DecimalField(max_digits=6, decimal_places=2)
    ingredient_cost = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.cost_per_portion
    
    def get_absolute_url(self):
        return reverse('costing_detail', args=[self.id])
    
    class Meta:
        verbose_name_plural = 'Costing'
        verbose_name = 'Costing'
        ordering = ['-cost_per_portion']