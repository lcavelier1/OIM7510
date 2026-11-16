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
    # Babson PT Clinic: Building the Database

    This notebook deletes `database.duckdb` and builds it again from the CSV files in `data/` every time it runs. The CSV files come from `make_data.py`.
    """)
    return


@app.cell
def _(duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"
    data = mo.notebook_dir() / "data"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return ask, data, database


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Tables

    One `CREATE TABLE` per table in the ERD. The keys and rules each table can hold are declared here:

    - `credential` must be DPT or PTA, `length_minutes` must be 30, 45 or 60, and `status` must be booked, completed or no-show.
    - A therapist can't have two appointments that start at the same time: `UNIQUE (therapist_id, starts_at)`.
    - Prices are above zero and costs are never negative.
    - Each appointment needs exactly one patient and one therapist: both are `NOT NULL` foreign keys.
    """)
    return


@app.cell
def _():
    create_tables = """
    CREATE TABLE therapists (
        therapist_id INTEGER PRIMARY KEY,
        first_name VARCHAR NOT NULL,
        last_name VARCHAR NOT NULL,
        credential VARCHAR NOT NULL CHECK (credential IN ('DPT', 'PTA')),
        hire_date DATE NOT NULL,
        email VARCHAR NOT NULL UNIQUE
    );

    CREATE TABLE patients (
        patient_id INTEGER PRIMARY KEY,
        first_name VARCHAR NOT NULL,
        last_name VARCHAR NOT NULL,
        date_of_birth DATE NOT NULL,
        phone VARCHAR,
        email VARCHAR,
        insurance_member_number VARCHAR UNIQUE  -- empty for self-pay patients
    );

    CREATE TABLE referrals (
        referral_id INTEGER PRIMARY KEY,
        patient_id INTEGER NOT NULL REFERENCES patients (patient_id),
        physician_name VARCHAR NOT NULL,
        referral_date DATE NOT NULL,
        reason VARCHAR
    );

    CREATE TABLE treatments (
        treatment_id INTEGER PRIMARY KEY,
        name VARCHAR NOT NULL UNIQUE,
        standard_minutes INTEGER NOT NULL CHECK (standard_minutes > 0),
        price DECIMAL(8, 2) NOT NULL CHECK (price > 0),
        cost DECIMAL(8, 2) NOT NULL CHECK (cost >= 0)
    );

    CREATE TABLE appointments (
        appointment_id INTEGER PRIMARY KEY,
        patient_id INTEGER NOT NULL REFERENCES patients (patient_id),
        therapist_id INTEGER NOT NULL REFERENCES therapists (therapist_id),
        starts_at TIMESTAMP NOT NULL,
        length_minutes INTEGER NOT NULL CHECK (length_minutes IN (30, 45, 60)),
        status VARCHAR NOT NULL DEFAULT 'booked' CHECK (status IN ('booked', 'completed', 'no-show')),
        UNIQUE (therapist_id, starts_at)
    );

    CREATE TABLE appointment_treatments (
        appointment_id INTEGER NOT NULL REFERENCES appointments (appointment_id),
        treatment_id INTEGER NOT NULL REFERENCES treatments (treatment_id),
        price_charged DECIMAL(8, 2) NOT NULL CHECK (price_charged > 0),
        minutes INTEGER NOT NULL CHECK (minutes > 0),
        PRIMARY KEY (appointment_id, treatment_id)
    );
    """
    return (create_tables,)


@app.cell
def _(create_tables, create_view, data, database, duckdb):
    # Build from nothing: delete the old file, then create and fill every table.
    database.unlink(missing_ok=True)
    with duckdb.connect(database) as _con:
        _con.sql(create_tables)
        for _table in ["therapists", "patients", "referrals", "treatments", "appointments", "appointment_treatments"]:
            _con.sql(f"INSERT INTO {_table} BY NAME SELECT * FROM read_csv('{data / _table}.csv')")
        _con.sql(create_view)
    built = True
    return (built,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Data

    `make_data.py` writes the six CSV files: 12 months of history up to **13 November 2026** (`as_of`), plus four weeks of booked appointments after it.

    It also leaves some rows with nothing attached: about a third of patients have no referral, patients 289 to 300 were referred but never booked, and two treatments (Dry Needling and Aquatic Therapy) were never given.

    **The two deliberate breaks for question 7:** appointments **1004** and **1007** are 30-minute appointments whose treatments add up to more than 30 minutes. The tables accept them, because no column rule can add up minutes across rows.
    """)
    return


@app.cell
def _(ask, built):
    built
    ask("""
        SELECT appointment_id, length_minutes, treatment_minutes
        FROM appointment_summary
        WHERE appointment_id IN (1004, 1007)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A Look at the Data
    """)
    return


@app.cell
def _(alt, ask, built):
    built
    by_weekday = ask("""
        SELECT dayname(starts_at) AS weekday, isodow(starts_at) AS day_number, COUNT(*) AS appointments
        FROM appointments
        GROUP BY weekday, day_number
        ORDER BY day_number
    """)
    alt.Chart(by_weekday).mark_bar().encode(
        x=alt.X("weekday:N", sort=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], title="Day of the week"),
        y=alt.Y("appointments:Q", title="Appointments"),
    ).properties(title="Appointments by day of the week")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This looks like a real clinic: Monday to Thursday are busy and similar, and Friday is much lower because people avoid booking right before the weekend. The first version had far too many Mondays and almost no Wednesdays, so I changed make_data.py.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Row Counts
    """)
    return


@app.cell
def _(ask, built):
    built
    ask("""
        SELECT 'therapists' AS table_name, COUNT(*) AS row_count FROM therapists
        UNION ALL SELECT 'patients', COUNT(*) FROM patients
        UNION ALL SELECT 'referrals', COUNT(*) FROM referrals
        UNION ALL SELECT 'treatments', COUNT(*) FROM treatments
        UNION ALL SELECT 'appointments', COUNT(*) FROM appointments
        UNION ALL SELECT 'appointment_treatments', COUNT(*) FROM appointment_treatments
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A Row It Refuses

    Appointment 1 already has a therapist and a start time. Here I try to book a second appointment for the same therapist at the very same minute. The `UNIQUE (therapist_id, starts_at)` rule should refuse it.
    """)
    return


@app.cell
def _(built, database, duckdb):
    built
    try:
        with duckdb.connect(database) as _con:
            _first = _con.execute("SELECT therapist_id, starts_at FROM appointments WHERE appointment_id = 1").fetchone()
            _con.execute(
                "INSERT INTO appointments VALUES (99999, 5, ?, ?, 30, 'booked')",
                [_first[0], _first[1]],
            )
        refused = "The database accepted the row (this should not happen)."
    except Exception as error:
        refused = f"Refused: {error}"
    refused
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Answers You Already Knew

    Three questions whose answers I knew before asking, because `make_data.py` made them that way.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **1. How many therapists are there?** Expected: 7.
    """)
    return


@app.cell
def _(ask, built):
    built
    ask("SELECT COUNT(*) AS therapists FROM therapists")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **2. How many treatments were never given?** Expected: 2 (Dry Needling and Aquatic Therapy).
    """)
    return


@app.cell
def _(ask, built):
    built
    ask("""
        SELECT t.name
        FROM treatments AS t
        LEFT JOIN appointment_treatments AS g ON g.treatment_id = t.treatment_id
        WHERE g.treatment_id IS NULL
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **3. Are there any booked appointments on or before `as_of`, or completed ones after it?** Expected: 0.
    """)
    return


@app.cell
def _(ask, built):
    built
    ask("""
        SELECT COUNT(*) AS wrong_status
        FROM appointments
        WHERE (status = 'booked' AND starts_at::DATE <= DATE '2026-11-13')
           OR (status <> 'booked' AND starts_at::DATE > DATE '2026-11-13')
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A View

    The clinic manager asks the same thing every week: what did each appointment bring in, and how many treatment minutes did it use? The view `appointment_summary` answers it with one row per appointment. The build cell above creates it, and Part B uses it.
    """)
    return


@app.cell
def _():
    create_view = """
    CREATE VIEW appointment_summary AS
    SELECT
        a.appointment_id,
        a.patient_id,
        a.therapist_id,
        a.starts_at,
        a.length_minutes,
        a.status,
        COALESCE(SUM(g.price_charged), 0) AS revenue,
        COALESCE(SUM(t.cost), 0) AS cost,
        COALESCE(SUM(g.minutes), 0) AS treatment_minutes
    FROM appointments AS a
    LEFT JOIN appointment_treatments AS g ON g.appointment_id = a.appointment_id
    LEFT JOIN treatments AS t ON t.treatment_id = g.treatment_id
    GROUP BY a.appointment_id, a.patient_id, a.therapist_id, a.starts_at, a.length_minutes, a.status
    """
    return (create_view,)


if __name__ == "__main__":
    app.run()
