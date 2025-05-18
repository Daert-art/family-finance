from django.shortcuts import render
from core.services.debt_calculator import calculate_debts
from datetime import date

def debt_result(request):
    month = int(request.GET.get('month', date.today().month))
    year = int(request.GET.get('year', date.today().year))

    from_date = date(year, month, 1)
    to_date = date(year + (month // 12), (month % 12) + 1, 1)

    result = calculate_debts(from_date, to_date)
    result['selected_month'] = month
    result['selected_year'] = year
    result['months'] = range(1, 13)

    return render(request, 'debts/result.html', result)


def debt_details(request):
    month = int(request.GET.get('month', date.today().month))
    year = int(request.GET.get('year', date.today().year))

    from_date = date(year, month, 1)
    to_date = date(year + (month // 12), (month % 12) + 1, 1)

    result = calculate_debts(from_date, to_date)
    result['selected_month'] = month
    result['selected_year'] = year

    return render(request, 'debts/details.html', result)
