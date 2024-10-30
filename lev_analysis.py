import pandas as pd
import datetime as dt

pd.set_option('display.max_columns', 50)
pd.set_option('display.width', 2000)

#Data
data = pd.read_csv('SPY_data.csv', index_col='Date')
data.index = pd.to_datetime(data.index, utc=True)
data = data.drop(['Capital Gains'], axis=1)
data = data.resample(rule='YE').last()
data['returns'] = data['Close'].pct_change()
data = data.dropna()


results = []

for start in range(len(data.index)):

    #Parameters
    starting_equity = 2000              #Amount of starting money
    r = 0.05                            #yearly interest rate
    n = 1                               #periods in year for interest
    maintinance_requirement = 0.30      #margin maintinance %

    #Margin Info
    margin_interest = (1 + r) ** (1/n) - 1
    margin_call = False
    margin_call_date = None

    #Regular Account
    regular_equity = [starting_equity]

    #Leveraged Account
    leveraged_equity = [starting_equity]
    margin_loan = [starting_equity]


    for i in range(start, len(data.index)):
        stock_return = float(1 + data['returns'].iloc[i])

        regular_equity.append(regular_equity[-1] * stock_return)

        #Leveraged
        leveraged_total = leveraged_equity[-1] + margin_loan[-1]
        new_leveraged_total = leveraged_total * stock_return

        loan_interest = margin_loan[-1] * margin_interest
        new_leveraged_equity = new_leveraged_total - margin_loan[-1] - loan_interest

        if new_leveraged_equity > leveraged_equity[-1]:
            margin_loan.append(new_leveraged_equity)
        else:
            margin_loan.append(margin_loan[-1])

        if new_leveraged_equity < new_leveraged_total * maintinance_requirement:
            margin_call = True
            margin_call_date = data.index[i].strftime('%Y-%m-%d')
            break

        leveraged_equity.append(new_leveraged_equity)


    results.append({
        'Start_Date': data.index[start],
        'Regular_Final': regular_equity[-1],
        'Leveraged_Final': leveraged_equity[-1],
        'Regular_Return': ((regular_equity[-1] - starting_equity) / starting_equity) * 100,
        'Leveraged_Return': ((leveraged_equity[-1] - starting_equity) / starting_equity) * 100,
        'Margin_Call': margin_call,
        'Margin_Call_Date': margin_call_date
    })


results_df = pd.DataFrame(results)
results_df['Start_Date'] = results_df['Start_Date'].dt.strftime('%Y-%m-%d')

print(round(results_df, 2))





