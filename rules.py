class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3
    WHITE = 4

def latest_financial_index(data: dict):
    for index, financial in enumerate(data.get("financials", [])):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0

def total_revenue(data: dict, financial_index: int):
    try:
        financial = data['financials'][financial_index]
        return financial['pnl']['lineItems'].get('net_revenue', 0)
    except (IndexError, KeyError):
        return 0

def total_borrowing(data: dict, financial_index: int):
    try:
        financial = data['financials'][financial_index]
        long_term_borrowings = financial['bs']['liabilities'].get('long_term_borrowings', 0)
        short_term_borrowings = financial['bs']['liabilities'].get('short_term_borrowings', 0)
        return long_term_borrowings + short_term_borrowings
    except (IndexError, KeyError):
        return 0

def iscr(data: dict, financial_index: int):
    try:
        financial = data['financials'][financial_index]
        interest = financial['pnl']['lineItems'].get('interest', 0) + 1
        profit_before_interest_and_tax = financial['pnl']['lineItems'].get('profit_before_interest_and_tax', 0) + 1
        return profit_before_interest_and_tax / interest
    except (IndexError, KeyError):
        return 0

def iscr_flag(data: dict, financial_index: int):
    iscr_value = iscr(data, financial_index)
    return FLAGS.GREEN if iscr_value >= 2 else FLAGS.RED

def total_revenue_5cr_flag(data: dict, financial_index: int):
    revenue = total_revenue(data, financial_index)
    return FLAGS.GREEN if revenue >= 50000000 else FLAGS.RED

def borrowing_to_revenue_flag(data: dict, financial_index: int):
    revenue = total_revenue(data, financial_index)
    borrowings = total_borrowing(data, financial_index)
    ratio = borrowings / (revenue or 1)
    return FLAGS.GREEN if ratio <= 0.25 else FLAGS.AMBER
