import pandas as pd
import json

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib import urlopen


def get_jsonparsed_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

#Returns tuple of (debt_score, debt, cash, debt/cash ratio)
def get_debt(ticker):
    try:

        balance_sheet_url = "https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/" + ticker


        balance_sheet = get_jsonparsed_data(balance_sheet_url)['financials']
        pd_balance = pd.DataFrame.from_dict(balance_sheet)[['date','Long-term debt', 'Cash and short-term investments']]
        debt = pd_balance.iloc[0,1]
        cash = pd_balance.iloc[0,2]
        ratio = float(debt)/float(cash)
        #Determining Size of Debt
        if(ratio<=0.1):
            return (3, debt, cash, ratio)
        if(0.1<ratio<=2):
            return (2, debt, cash, ratio)
        if(2<ratio<=4):
            return (1, debt, cash, ratio)
        if(4<ratio):
            return (0, debt, cash, ratio)
    except:
        return 1

#Returns tuple of (revenue score, profit score)
def get_revenue_profit(ticker):
    q_financials_url = ("https://financialmodelingprep.com/api/v3/financials/income-statement/" + ticker + "?period=quarter")
    q_financials = get_jsonparsed_data(q_financials_url)['financials']
    pd_quarterly = pd.DataFrame.from_dict(q_financials)[['date', 'Revenue', 'EPS Diluted']]
    revenue_growth = []
    revs = pd_quarterly['Revenue']
    q_eps_growth = []
    q_eps = pd_quarterly['EPS Diluted']
    for i in range(len(revs)):
        try:
            x1 = (((float(revs[i]) - float(revs[i + 4])) / float(revs[i + 4])) * 100)
            x2 = (((float(revs[i]) - float(revs[i + 4])) / float(revs[i + 4])) * 100)
            revenue_growth.append(round(x1, 2))
            q_eps_growth.append(round(x2, 2))
        except:
            revenue_growth.append('-')
            q_eps_growth.append('—')
    pd_quarterly.insert(2, "Revenue Growth (%)", revenue_growth, True)
    pd_quarterly.insert(4, "EPS Growth (%)", q_eps_growth, True)
    pd_quarterly.set_index('date')
    print(pd_quarterly)
    last_ten_rev = pd_quarterly.iloc[0:10,2]
    last_four_rev = pd_quarterly.iloc[0:4, 2]
    last_two_rev = pd_quarterly.iloc[0:2, 2]
    last_ten_eps = pd_quarterly.iloc[0:10, 4]
    last_four_eps = pd_quarterly.iloc[0:4, 4]
    last_two_eps = pd_quarterly.iloc[0:2, 4]
    def count_negative(list):
        count = 0
        for i in list:
            if (i<0):
                count = count + 1
        return count
    if (count_negative(last_ten_rev)>=8):
        rev_result = 0
    elif(count_negative(last_four_rev)>=3):
        rev_result = 1
    elif(count_negative(last_two_rev)==2):
        rev_result = 2
    else:
        rev_result = 3
    if (count_negative(last_ten_eps)>=8):
        eps_result = 0
    elif(count_negative(last_four_eps)>=3):
        eps_result = 1
    elif(count_negative(last_two_eps)==2):
        eps_result = 2
    else:
        eps_result = 3
    return(rev_result, eps_result)



def get_profit(ticker):
    return (True)

def get_altman(ticker):
    return (True)

def yearly_range(ticker):
    return (True)
