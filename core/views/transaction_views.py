from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Sum
from core.forms import TransactionForm
from core.models.transaction import Transaction
from core.models.category import Category
from core.enums.category_type import CategoryType
import datetime

@login_required
def transaction_list(request):
    all_transactions = Transaction.objects.all().order_by('-date')
    categories = Category.objects.all()
    users = User.objects.all()

    # поточна дата
    today = datetime.date.today()
    current_month = today.month
    current_year = today.year

    # фільтрація
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category_id = request.GET.get('category')
    paid_by = request.GET.get('paid_by')

    if not start_date and not end_date:
        all_transactions = all_transactions.filter(date__year=current_year, date__month=current_month)

    if start_date:
        all_transactions = all_transactions.filter(date__gte=start_date)
    if end_date:
        all_transactions = all_transactions.filter(date__lte=end_date)
    if category_id:
        all_transactions = all_transactions.filter(category_id=category_id)
    if paid_by:
        all_transactions = all_transactions.filter(paid_by_id=paid_by)

    # розділення по типу
    incomes = all_transactions.filter(category__type=CategoryType.INCOME)
    expenses = all_transactions.filter(category__type=CategoryType.EXPENSE)

    # підсумки
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    context = {
        'incomes': incomes,
        'expenses': expenses,
        'categories': categories,
        'users': users,
        'start_date': start_date,
        'end_date': end_date,
        'selected_category': int(category_id) if category_id else None,
        'selected_paid_by': int(paid_by) if paid_by else None,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
    }
    return render(request, 'transactions/list.html', context)

@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transactions/create.html', {'form': form})

# Редагування для адміністратора
@login_required
@user_passes_test(lambda u: u.is_staff)
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'transactions/update.html', {'form': form, 'transaction': transaction})


# Видалення транзакцій доступні лише для адміністратора
@login_required
@user_passes_test(lambda u: u.is_staff)
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')

    return render(request, 'transactions/confirm_delete.html', {'transaction': transaction})
