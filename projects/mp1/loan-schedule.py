# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of option, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *This tool is designed for someone buying an apartment who needs to finance the remaining $400,000 after making a 20% down payment. It helps them compare a 30-year mortgage at 7.03% interest with a 15-year mortgage at 6.42% to decide which option best fits their budget and saves them the most money in the long run.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    1. Start with the loan amount ($400,000), the interest rates (7.03% for 30 years and 6.42% for 15 years), and the loan terms.
    2. Calculate the monthly interest rate and the total number of payments for each option.
    3. Calculate how much my friend would have to pay each month for each mortgage.
    4. Use a loop to go through each month and calculate how much goes toward interest, how much goes toward the loan itself, and how much she still owes.
    5. Keep track of the total interest paid for each loan and repeat the process for both options.
    6. Compare the results to see which option has lower monthly payments and which one saves more money in the long run.

    **What does your loop carry from one step to the next, the way a running total carries its sum?**

    The loop keeps track of how much my friend still owes after each monthly payment. It updates the balance every month until the loan is paid off.

    **Which check will you use in section 6, and which two numbers should agree?**

    I will check that the total amount of principal paid equals the original $400,000 loan amount. These two numbers should be the same.

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your option from the Mini Project 1 page. If you chose D, your own option, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    loan_amount = 400000
    annual_rates = {30: 0.0703, 15: 0.0642}
    return annual_rates, loan_amount


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(annual_rates, loan_amount):
    r = annual_rates[30] / 12
    n = 30 * 12
    payment = round(loan_amount * r / (1 - (1 + r) ** -n), 2)
    print(payment)
    return


@app.cell
def _(annual_rates, loan_amount):
    def make_schedule(term):
        r = annual_rates[term] / 12
        n = term * 12
        payment = round(loan_amount * r / (1 - (1 + r) ** -n), 2)
        balance = loan_amount
        rows = []
        for month in range(1, n + 1):
            interest = round(balance * r, 2)
            if month == n:
                principal = balance
                pay = round(principal + interest, 2)
            else:
                pay = payment
                principal = round(payment - interest, 2)
            balance = round(balance - principal, 2)
            rows.append((month, pay, interest, principal, balance))
        return rows

    return (make_schedule,)


@app.function
def print_schedule(rows):
    print(f"{'Month':>5} {'Payment':>10} {'Interest':>10} {'Principal':>10} {'Balance':>12}")
    for month, pay, interest, principal, balance in rows:
        print(f"{month:>5} {pay:>10,.2f} {interest:>10,.2f} {principal:>10,.2f} {balance:>12,.2f}")


@app.cell
def _(make_schedule):
    schedule_30 = make_schedule(30)
    print_schedule(schedule_30)
    return (schedule_30,)


@app.cell
def _(make_schedule):
    schedule_15 = make_schedule(15)
    print_schedule(schedule_15)
    return (schedule_15,)


@app.function
def total_interest(rows):
    total = 0
    for row in rows:
        total = total + row[2]
    return round(total, 2)


@app.cell
def _(schedule_15, schedule_30):
    interest_30 = total_interest(schedule_30)
    interest_15 = total_interest(schedule_15)
    payment_30 = schedule_30[0][1]
    payment_15 = schedule_15[0][1]

    print(f"{'Loan':>8} {'Monthly payment':>16} {'Total interest':>16}")
    print(f"{'30-year':>8} {payment_30:>16,.2f} {interest_30:>16,.2f}")
    print(f"{'15-year':>8} {payment_15:>16,.2f} {interest_15:>16,.2f}")
    print()
    print(f"The 15-year loan costs ${payment_15 - payment_30:,.2f} more each month, "
          f"but saves ${interest_30 - interest_15:,.2f} in interest over the life of the loan.")
    return interest_15, interest_30


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(loan_amount, schedule_15, schedule_30):
    def total_principal(rows):
        total = 0
        for row in rows:
            total = total + row[3]
        return round(total, 2)

    principal_30 = total_principal(schedule_30)
    principal_15 = total_principal(schedule_15)
    print(f"30-year: principal paid = {principal_30:,.2f}, loan = {loan_amount:,.2f}, match: {principal_30 == loan_amount}")
    print(f"15-year: principal paid = {principal_15:,.2f}, loan = {loan_amount:,.2f}, match: {principal_15 == loan_amount}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I added up all the principal payments for both loans and compared them with the original $400,000 loan amount. Both totals matched $400,000, which shows that the calculations were correct and the loans were fully paid off. This is a way to check my results without just looking at the final balance.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell
def _(annual_rates, loan_amount):
    def payoff_with_extra(term, extra):
        r = annual_rates[term] / 12
        n = term * 12
        payment = round(loan_amount * r / (1 - (1 + r) ** -n), 2)
        balance = loan_amount
        months = 0
        total = 0
        while balance > 0:
            months = months + 1
            interest = round(balance * r, 2)
            principal = round(payment + extra - interest, 2)
            if principal > balance:
                principal = balance
            balance = round(balance - principal, 2)
            total = total + interest
        return months, round(total, 2)

    return (payoff_with_extra,)


@app.cell
def _(interest_15, interest_30, payoff_with_extra):
    extra_payment = 200
    months_30, extra_interest_30 = payoff_with_extra(30, extra_payment)
    months_15, extra_interest_15 = payoff_with_extra(15, extra_payment)

    print(f"30-year: paid off in {months_30} months instead of 360, "
          f"saving {360 - months_30} months and ${interest_30 - extra_interest_30:,.2f} in interest.")
    print(f"15-year: paid off in {months_15} months instead of 180, "
          f"saving {180 - months_15} months and ${interest_15 - extra_interest_15:,.2f} in interest.")
    return


if __name__ == "__main__":
    app.run()
