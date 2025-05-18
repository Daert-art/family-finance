from django.urls import path

from core.views import debt_views
from core.views.debt_views import debt_result
from core.views.transaction_views import transaction_list, transaction_create

urlpatterns = [
    path('', transaction_list, name='transaction_list'),
    path('add/', transaction_create, name='transaction_create'),
    path('debts/', debt_result, name='debt_result'),
    path('debts/details/', debt_views.debt_details, name='debt_details'),
]
