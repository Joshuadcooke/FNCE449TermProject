# FNCE449TermProject
These code files aim to evaluate the performance of a sector rotation strategy by analyzing returns of the strategy against the S&P 500 for two periods: pre and post COVID. By looking at performance over these periods, we can explore how effective this strategy is under different economic conditions and how sector performance may have shifted in response to unprecedented events. The sector rotation strategy implemented involves looking at the returns of 5 chosen securities from a given month and then purchasing the top performers and then unwinding the position and reallocating at the end of the following month. This approach is intended to capture gains in high-performing sectors while minimizing exposure to underperforming areas.

There are 3 Python files in this repository:

FNCE 449 Term Project CSV Download.py:
    This Python file downloads the data I used in the following Python files. It is not neccesary to run this code as I have the data sitting in another repository and it will automatically be pulled when running the next two Python files. I only included it to show how I       accessed the CSV files. This data is located at: https://github.com/Joshuadcooke/TermProjectData

FNCE 449 Term Project Pre Covid Code.py:
    This code file is testing my sector rotation strategy against the cumulative returns of the S&P 500 from 2016-01-01 to 2018-01-01 (pre-COVID). Using data in the other repository: https://github.com/Joshuadcooke/TermProjectData
    The outputs from running this code file are:
      "Average Monthly Returns Pre-Covid (2016-2018)" for my chosen stocks of AAPL, JPM, TSLA, XOM, and META.
      Ending Cumulative Return of Portfolio, Ending Cumulative Return of S&P 500, and the Difference in Cumulative Return (Portfolio - S&P 500).
      Figure 2 shows a graph of the Cumulative Portfolio Return vs S&P 500. The date is on the x-axis and the cumultaive return is on the y-axis.
      Figure 1 shows the monthly trade log, this identifies which stocks are purchased at the end of each month based off of the returns throughout that month. With the exception of the first month, the previous trades are closed before the stocks are selected.

FNCE 449 Term Project Post Covid Code.py:
    This code file is testing my sector rotation strategy against the cumulative returns of the S&P 500 from 2022-11-01 to 2024-11-01 (post-COVID). Using data in the other repository: https://github.com/Joshuadcooke/TermProjectData
    The outputs from running this code file are:
      "Average Monthly Returns Pre-Covid (2022-2024)" for my chosen stocks of AAPL, JPM, TSLA, XOM, and META.
      Ending Cumulative Return of Portfolio, Ending Cumulative Return of S&P 500, and the Difference in Cumulative Return (Portfolio - S&P 500).
      Figure 2 shows a graph of the Cumulative Portfolio Return vs S&P 500. The date is on the x-axis and the cumultaive return is on the y-axis.
      Figure 1 shows the monthly trade log, this identifies which stocks are purchased at the end of each month based off of the returns throughout that month. With the exception of the first month, the previous trades are closed before the stocks are selected.
