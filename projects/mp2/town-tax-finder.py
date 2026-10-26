import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Town Tax Finder
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This tool helps a couple find towns in Middlesex County where they can afford a $700,000 home and pay less than $8,000 a year in property taxes. It shows the best options, starting with the lowest tax bill.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Steps

    1. I will get all the towns in Middlesex County, using 100 towns per page.
    2. I will check that I got all the towns by comparing the total with the API’s pagination.
    3. I will get the 2026 tax data for each town using its dor_code.
    4. I will keep the towns with an average home value of $700,000 or less and taxes under $8,000.
    5. I will sort them from the lowest to the highest tax bill.
    6. I will print the results in a table with a short summary.

    Functions

    * get_towns(county): Gets all the towns in a county.
    * get_year(dor_code, fiscal_year): Gets a town’s tax data for a specific year.

    Addresses

    * https://oim.zhili.dev/ma/towns?county=...
    * https://oim.zhili.dev/ma/towns/{dor_code}/history

    How I will check my results:
    I will make sure the number of towns matches the API’s total. I will also check that the average home value multiplied by the tax rate and divided by 1,000 is close to the average tax bill.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I used AI to review and correct my plan in section 2 before writing any code.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Reading It Back
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Going Further
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Time Spent
    """)
    return


if __name__ == "__main__":
    app.run()
