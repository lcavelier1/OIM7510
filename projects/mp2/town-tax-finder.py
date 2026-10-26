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


@app.cell
def _():
    county = "Middlesex"
    budget_dollars = 700000
    tax_limit_dollars = 8000
    fiscal_year = 2026
    return budget_dollars, county, fiscal_year, tax_limit_dollars


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work
    """)
    return


@app.cell
def _():
    import requests

    return (requests,)


@app.cell
def _(county, requests):
    def get_towns(county):
        towns_url = "https://oim.zhili.dev/ma/towns"
        first_page = requests.get(
            towns_url,
            params={"county": county, "per_page": 100, "page": 1},
            timeout=10,
        ).json()
        towns = first_page["items"]
        pages = first_page["pagination"]["pages"]
        for page_number in range(2, pages + 1):
            next_page = requests.get(
                towns_url,
                params={"county": county, "per_page": 100, "page": page_number},
                timeout=10,
            ).json()
            towns = towns + next_page["items"]
        return towns

    county_towns = get_towns(county)
    len(county_towns), county_towns[0]["name"]
    return (county_towns,)


@app.cell
def _(fiscal_year, requests):
    def get_year(dor_code, fiscal_year):
        history = requests.get(
            f"https://oim.zhili.dev/ma/towns/{dor_code}/history",
            timeout=10,
        ).json()
        for year in history["years"]:
            if year["fiscal_year"] == fiscal_year:
                return year
        return None

    get_year("317", fiscal_year)
    return (get_year,)


@app.cell
def _(county_towns, fiscal_year, get_year):
    town_records = []
    for _town in county_towns:
        _year = get_year(_town["dor_code"], fiscal_year)
        if _year is not None:
            town_records.append(
                {
                    "name": _town["name"],
                    "dor_code": _town["dor_code"],
                    "average_value_dollars": _year["average_single_family_value_dollars"],
                    "tax_rate": _year["residential_rate_per_thousand"],
                    "average_bill_dollars": _year["average_single_family_bill_dollars"],
                }
            )

    len(town_records), town_records[0]
    return (town_records,)


@app.cell
def _(budget_dollars, tax_limit_dollars, town_records):
    passing_towns = []
    for _record in town_records:
        _value = _record["average_value_dollars"]
        _bill = _record["average_bill_dollars"]
        if _value is not None and _bill is not None:
            if _value <= budget_dollars and _bill < tax_limit_dollars:
                passing_towns.append(_record)

    def get_bill(record):
        return record["average_bill_dollars"]

    sorted_towns = sorted(passing_towns, key=get_bill)
    len(sorted_towns), sorted_towns
    return (sorted_towns,)


@app.cell
def _(county, fiscal_year, mo, town_records):
    import csv

    data_folder = mo.notebook_dir() / "data"
    data_folder.mkdir(exist_ok=True)
    records_csv = data_folder / f"{county.lower()}-{fiscal_year}.csv"

    with open(records_csv, "w", newline="", encoding="utf-8") as _file:
        _writer = csv.DictWriter(_file, fieldnames=list(town_records[0].keys()))
        _writer.writeheader()
        _writer.writerows(town_records)

    records_csv.name
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer
    """)
    return


@app.cell
def _(sorted_towns):
    print(f"{'Town':<16}{'Avg home value':>16}{'Tax rate':>10}{'Avg bill':>10}")
    for _record in sorted_towns:
        _value_text = f"${_record['average_value_dollars']:,}"
        _bill_text = f"${_record['average_bill_dollars']:,}"
        print(f"{_record['name']:<16}{_value_text:>16}{_record['tax_rate']:>10.2f}{_bill_text:>10}")
    return


@app.cell
def _(budget_dollars, county, fiscal_year, sorted_towns, tax_limit_dollars):
    if sorted_towns:
        cheapest_town = sorted_towns[0]
        answer_sentence = (
            f"In {county} County, {len(sorted_towns)} towns have an average single-family home "
            f"of ${budget_dollars:,} or less and an average tax bill under ${tax_limit_dollars:,} "
            f"in fiscal year {fiscal_year}. The lowest bill is in {cheapest_town['name']}, "
            f"at ${cheapest_town['average_bill_dollars']:,} a year on an average home of "
            f"${cheapest_town['average_value_dollars']:,}."
        )
    else:
        answer_sentence = (
            f"No town in {county} County has an average home of ${budget_dollars:,} or less "
            f"and an average bill under ${tax_limit_dollars:,} in fiscal year {fiscal_year}."
        )
    print(answer_sentence)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right
    """)
    return


@app.cell
def _(county, county_towns, requests, sorted_towns):
    check_reply = requests.get(
        "https://oim.zhili.dev/ma/towns",
        params={"county": county, "per_page": 1},
        timeout=10,
    ).json()
    api_total = check_reply["pagination"]["total"]
    print(f"Towns I collected: {len(county_towns)}   Towns the API reports: {api_total}   Match: {len(county_towns) == api_total}")
    print()
    print(f"{'Town':<16}{'API bill':>10}{'Value x rate / 1000':>22}{'Difference':>12}")
    for _record in sorted_towns:
        _computed_bill = _record["average_value_dollars"] * _record["tax_rate"] / 1000
        _difference = abs(_computed_bill - _record["average_bill_dollars"])
        print(f"{_record['name']:<16}{_record['average_bill_dollars']:>10,}{_computed_bill:>22,.2f}{_difference:>12,.2f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I checked that I got all 54 towns by comparing my results with the API total. I also checked that the tax bills I calculated were almost the same as the API’s bills, with a difference of less than 50 cents.
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
    The agent’s code worked the first time. I checked that the number of towns matched the API and that the tax bills matched my calculations. I also tested Wellesley separately and got the same numbers as in notebook 04.
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
