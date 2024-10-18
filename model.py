import json
from rules import latest_financial_index, iscr_flag, total_revenue_5cr_flag, borrowing_to_revenue_flag

def analyze_financials(data):
    if 'financials' not in data or not isinstance(data['financials'], list):
        return {"error": "'financials' key is missing or invalid"}
    
    financial_index = latest_financial_index(data)
    
    results = {
        "ISCR_FLAG": iscr_flag(data, financial_index),
        "TOTAL_REVENUE_5CR_FLAG": total_revenue_5cr_flag(data, financial_index),
        "BORROWING_TO_REVENUE_FLAG": borrowing_to_revenue_flag(data, financial_index),
    }
    
    return results

if __name__ == "__main__":
    with open('data.json', 'r') as f:
        data = json.load(f)

    analysis_results = analyze_financials(data)
    print(json.dumps(analysis_results, indent=4))
