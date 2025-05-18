from django.db import models
from django.contrib.auth.models import User
from core.models.category import Category

class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    participants = models.ManyToManyField(User, related_name='involved_in')
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.category.name} – {self.amount} грн'
    class Meta:
        app_label = 'core'
        ordering = ['-date']
