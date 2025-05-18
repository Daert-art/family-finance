from django.db import models
from django.contrib.auth.models import User
from core.enums.category_type import CategoryType

class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=7, choices=CategoryType.choices)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.get_type_display()})'
    class Meta:
        app_label = 'core'
