from collections import defaultdict
from core.models.transaction import Transaction

def calculate_debts(from_date=None, to_date=None):
    expected = defaultdict(float)
    paid = defaultdict(float)
    transactions_data = []

    txs = Transaction.objects.all()
    if from_date:
        txs = txs.filter(date__gte=from_date)
    if to_date:
        txs = txs.filter(date__lt=to_date)  # строго меньше следующего месяца

    for tx in txs:
        amount = float(tx.amount)
        participants = tx.participants.all()
        share = round(amount / participants.count(), 2)

        transactions_data.append({
            'date': tx.date,
            'amount': amount,
            'paid_by': tx.paid_by.username,
            'participants': [p.username for p in participants],
            'share': share,
            'description': tx.description
        })

        for user in participants:
            expected[user.username] += share
        paid[tx.paid_by.username] += amount

    balances = {user: round(paid[user] - expected[user], 2) for user in set(expected) | set(paid)}

    debts = []
    debtors = {u: b for u, b in balances.items() if b < -0.01}
    creditors = {u: b for u, b in balances.items() if b > 0.01}

    for debtor, debt_amount in debtors.items():
        for creditor, credit_amount in list(creditors.items()):
            if debt_amount == 0:
                break

            transfer = min(-debt_amount, credit_amount)
            if transfer > 0:
                debts.append({
                    'from': debtor,
                    'to': creditor,
                    'amount': round(transfer, 2)
                })

                debtors[debtor] += transfer
                creditors[creditor] -= transfer
                debt_amount += transfer

    return {
        'debts': debts,
        'details': transactions_data,
        'balances': balances,
    }
