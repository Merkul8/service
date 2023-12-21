from django.db import models
from django.urls import reverse

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('item', kwargs={'pk': self.pk})
    
    
