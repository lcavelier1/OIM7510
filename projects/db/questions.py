import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import altair as alt

    return alt, duckdb, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Babson PT Clinic: Questions and Verification

    Eight business questions answered with the database that `build.py` makes. Run `build.py` first so that `database.duckdb` exists.
    """)
    return


@app.cell
def _():
    as_of = "2026-11-13"
    return (as_of,)


@app.cell
def _(duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `as_of` is **13 November 2026**. "Last month" means the last full calendar month before it, so **October 2026**.

    ## 1. How many appointments did each therapist complete last month, and how much revenue did they bring in?
    """)
    return


@app.cell
def _(as_of, ask):
    q1 = ask(f"""
        SELECT th.first_name || ' ' || th.last_name AS therapist,
               COUNT(DISTINCT a.appointment_id) AS completed_appointments,
               COALESCE(SUM(g.price_charged), 0) AS revenue
        FROM therapists AS th
        LEFT JOIN appointments AS a
               ON a.therapist_id = th.therapist_id
              AND a.status = 'completed'
              AND a.starts_at >= date_trunc('month', DATE '{as_of}') - INTERVAL 1 MONTH
              AND a.starts_at < date_trunc('month', DATE '{as_of}')
        LEFT JOIN appointment_treatments AS g ON g.appointment_id = a.appointment_id
        GROUP BY therapist
        ORDER BY revenue DESC
    """)
    q1
    return (q1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In October 2026 the seven therapists completed **237** appointments worth **$35,308**; Priya Shah led with 58 appointments and $8,510.75, and Daniel Park had the fewest with 14 and $2,082.

    ## 2. What is the no-show rate per therapist and per day of the week?

    Rate = no-shows ÷ (completed + no-shows). Booked appointments are left out because they haven't happened yet.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT th.first_name || ' ' || th.last_name AS therapist,
               COUNT(*) FILTER (WHERE a.status = 'no-show') AS no_shows,
               COUNT(*) FILTER (WHERE a.status IN ('completed', 'no-show')) AS completed_or_no_show,
               ROUND(100.0 * COUNT(*) FILTER (WHERE a.status = 'no-show')
                     / COUNT(*) FILTER (WHERE a.status IN ('completed', 'no-show')), 1) AS no_show_pct
        FROM therapists AS th
        JOIN appointments AS a ON a.therapist_id = th.therapist_id
        GROUP BY therapist
        ORDER BY no_show_pct DESC
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT dayname(starts_at) AS weekday,
               COUNT(*) FILTER (WHERE status = 'no-show') AS no_shows,
               COUNT(*) FILTER (WHERE status IN ('completed', 'no-show')) AS completed_or_no_show,
               ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'no-show')
                     / COUNT(*) FILTER (WHERE status IN ('completed', 'no-show')), 1) AS no_show_pct
        FROM appointments
        GROUP BY weekday, isodow(starts_at)
        ORDER BY isodow(starts_at)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Marcus Hill has the highest no-show rate at **14.9%** (52 of 349) and Laura Mejia the lowest at **5.9%** (37 of 631); by day, Monday is worst at **12.1%** and Friday best at **6.4%**.

    ## 3. Which patients have we lost touch with?

    Patients whose last completed appointment was more than 90 days before `as_of` and who have nothing booked, with their phone numbers for outreach.
    """)
    return


@app.cell
def _(as_of, ask):
    q3 = ask(f"""
        SELECT p.patient_id, p.first_name, p.last_name, p.phone,
               MAX(a.starts_at)::DATE AS last_completed
        FROM patients AS p
        JOIN appointments AS a ON a.patient_id = p.patient_id AND a.status = 'completed'
        WHERE NOT EXISTS (
            SELECT 1 FROM appointments AS b
            WHERE b.patient_id = p.patient_id AND b.status = 'booked'
        )
        GROUP BY p.patient_id, p.first_name, p.last_name, p.phone
        HAVING MAX(a.starts_at)::DATE < DATE '{as_of}' - INTERVAL 90 DAY
        ORDER BY last_completed
    """)
    q3
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **153** patients last came in before 15 August 2026 and have nothing booked; the longest gone is Hector Martinez (patient 233), last seen on 10 December 2025.

    ## 4. What does each treatment earn: revenue, cost and margin?

    Includes the treatments that were never given. Cost is the treatment's internal cost times the number of times it was given.
    """)
    return


@app.cell
def _(ask):
    q4 = ask("""
        SELECT t.name AS treatment,
               COUNT(g.appointment_id) AS times_given,
               COALESCE(SUM(g.price_charged), 0) AS revenue,
               COUNT(g.appointment_id) * t.cost AS cost,
               COALESCE(SUM(g.price_charged), 0) - COUNT(g.appointment_id) * t.cost AS margin
        FROM treatments AS t
        LEFT JOIN appointment_treatments AS g ON g.treatment_id = t.treatment_id
        GROUP BY t.name, t.cost
        ORDER BY margin DESC
    """)
    q4
    return (q4,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Manual Therapy earns the most, with **$71,110** of revenue and a **$48,870** margin over 1,112 uses; Dry Needling and Aquatic Therapy were never given, so they show $0.

    ## 5. Which referred patients never had an appointment?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT p.patient_id, p.first_name, p.last_name, p.phone,
               COUNT(*) AS referrals
        FROM patients AS p
        JOIN referrals AS r ON r.patient_id = p.patient_id
        WHERE NOT EXISTS (
            SELECT 1 FROM appointments AS a WHERE a.patient_id = p.patient_id
        )
        GROUP BY p.patient_id, p.first_name, p.last_name, p.phone
        ORDER BY p.patient_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **12** patients (IDs 289 to 300) were referred by a physician but never booked a single appointment.

    ## 6. For each patient, how many referrals and how many appointments?

    Each count is made in its own subquery first and then joined to patients, so referrals and appointments don't multiply each other.
    """)
    return


@app.cell
def _(ask):
    q6 = ask("""
        WITH referral_counts AS (
            SELECT patient_id, COUNT(*) AS referral_count
            FROM referrals
            GROUP BY patient_id
        ),
        appointment_counts AS (
            SELECT patient_id, COUNT(*) AS appointment_count
            FROM appointments
            GROUP BY patient_id
        )
        SELECT p.patient_id, p.first_name, p.last_name,
               COALESCE(rc.referral_count, 0) AS referral_count,
               COALESCE(ac.appointment_count, 0) AS appointment_count
        FROM patients AS p
        LEFT JOIN referral_counts AS rc ON rc.patient_id = p.patient_id
        LEFT JOIN appointment_counts AS ac ON ac.patient_id = p.patient_id
        ORDER BY p.patient_id
    """)
    q6
    return (q6,)


@app.cell
def _(q6):
    # Each count checked against counting it alone: the totals must equal the table row counts.
    {
        "referrals in q6": q6["referral_count"].sum(),
        "appointments in q6": q6["appointment_count"].sum(),
        "patients in q6": q6.height,
    }
    return


@app.cell
def _(ask):
    ask("""
        SELECT (SELECT COUNT(*) FROM referrals) AS referrals_alone,
               (SELECT COUNT(*) FROM appointments) AS appointments_alone,
               (SELECT COUNT(*) FROM patients) AS patients_alone
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The table has one row for each of the **300** patients; its referral counts add up to **293** and its appointment counts to **3,236**, the same as counting each table alone.

    ## 7. Which completed appointments break the minutes rule?

    The rule: the treatments given at an appointment take no more minutes than the appointment's length. This uses the view `appointment_summary` from `build.py`.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT appointment_id, patient_id, therapist_id, starts_at,
               length_minutes, treatment_minutes
        FROM appointment_summary
        WHERE status = 'completed'
          AND treatment_minutes > length_minutes
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Exactly **2** completed appointments break the rule, **1004** (50 minutes of treatment in 30) and **1007** (45 in 30): the two I broke on purpose in Part A.

    ## 8. My own question

    <!-- TODO Laura: your question in plain words -->
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## How I Know These Numbers Are Right

    **Check 1: question 1 against the view.** Question 1 joins three tables. Here the same month is counted straight from the view `appointment_summary`, without the therapists table. Both should give 237 appointments and $35,308.
    """)
    return


@app.cell
def _(as_of, ask, q1):
    by_view = ask(f"""
        SELECT COUNT(*) AS completed_appointments, SUM(revenue) AS revenue
        FROM appointment_summary
        WHERE status = 'completed'
          AND starts_at >= date_trunc('month', DATE '{as_of}') - INTERVAL 1 MONTH
          AND starts_at < date_trunc('month', DATE '{as_of}')
    """)
    {
        "q1 appointments": q1["completed_appointments"].sum(),
        "view appointments": by_view["completed_appointments"][0],
        "q1 revenue": q1["revenue"].sum(),
        "view revenue": by_view["revenue"][0],
    }
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Check 2: question 4's total against every treatment row.** The revenue of all treatments in question 4 should equal the sum of every `price_charged` in `appointment_treatments`.
    """)
    return


@app.cell
def _(ask, q4):
    all_rows = ask("SELECT SUM(price_charged) AS revenue FROM appointment_treatments")
    {
        "q4 total revenue": q4["revenue"].sum(),
        "all treatment rows": all_rows["revenue"][0],
    }
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Check 3: question 6** is checked right under it: its totals match the row counts of `referrals` (293) and `appointments` (3,236) from `build.py`.

    ## Working With the Agent

    <!-- TODO Laura -->

    ## Reading It Back

    **My prediction (before running the joins):** joining `patients`, `referrals` and `appointments` without grouping will give about **4,200 rows**. It has to be more than the 3,236 appointments, because a patient with 2 or 3 referrals gets each of their appointments repeated once per referral, but most patients have 0 or 1 referral, so only some appointments repeat. The 12 referred patients with no appointments still add 1 row each, because a LEFT JOIN keeps every patient.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Going Further

    <!-- TODO Laura -->

    ## Time Spent

    <!-- TODO Laura -->
    """)
    return


if __name__ == "__main__":
    app.run()
    