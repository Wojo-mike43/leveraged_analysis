# leveraged_analysis

This project analyzes the difference between regular and leveraged investments in the S&P 500 index through its proxy $SPY. The script utilized `pandas` to model both a regular and leveraged investment account, and takes into consideration factors such as interest on margin loans, margin maintinance requirements, and potential margin calls. Additionally, it backtests from every possible starting date to assess how the starting date impacts returns.

**Assumptions:**

There are several assumption for the model:
- Equity earned in the account can be borrowed against, essentially maintaining 2x leverage throught the simulation.
- Any decline in account equity results in the same margin loan being held, meaning that as equity declines the margin loan stays the same.
- The strategy being tested is a simply buy and hold strategy. There is no selling to reduce the likleyhood of a margin call.

**How it Works:**


Inputs:
- Data for the simulation is read in from a CSV file. This file contains data starting in 1993 and goes until Oct 1st of 2024.
- Parameters such as the starting equity, yearly interest rate on margin loans, and maintinance requirements can be adjusted in the script.


Calculations:
- Returns for a regular account are calculated using $SPY yearly returns.
- Leveraged Account is modeled wtih an initial loan equal to the starting equity. As the equity increases, additional funds are borrowed to maintain 2x leverage. The account includes:
  - Margin Interest: Compounded monthly, based on the specified yearly interest rate.
  - Maintenance Requirement: If the equity falls below the maintenance threshold, a margin call is triggered, and the date is recorded.

 
**Output:**
- The output is a `pandas` dataframe showing the theoretical value of each account based on the starting date for each simulation.
