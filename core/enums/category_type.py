from django.db import models

class CategoryType(models.TextChoices):
    INCOME = 'INCOME', 'Доход'
    EXPENSE = 'EXPENSE', 'Расход'
