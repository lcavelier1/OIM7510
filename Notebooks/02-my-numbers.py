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
    # How much did I spend on groceries from April to August?
    """)
    return


@app.cell
def _():
    spending = [250.50, 198.25, "n/a", 225.00, 240.50]
    months = ["April", "May", "June", "July","August"]
    return (spending,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each number in `spending` is the amount I spent on groceries in the month at the same position in `months`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    TypeError: Python cannot add a number to the text "n/a".

    Rule: a month whose value is text is left out of the total.
    """)
    return


@app.cell
def _(spending):
    clean = []
    for amount in spending:
        if type(amount) != str:
            clean.append(amount)
    clean
    return (clean,)


@app.cell
def _(clean):
    print(f"Over the {len(clean)} months with data, groceries cost ${sum(clean):.2f}, or ${sum(clean) / len(clean):.2f} a month.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    How I know these numbers are right: I added the same numbers by hand, 250.50 + 198.25 + 225.00 + 240.50 = 914.25, and I ran a second calculation with a loop in the next cell.
    """)
    return


@app.cell
def _(clean):
    running = 0
    for value in clean:
        running = running + value
    running
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I changed April in `spending` from 210.50 to 250.50. The clean list, the sentence and the check loop updated by themselves.
    """)
    return


if __name__ == "__main__":
    app.run()
