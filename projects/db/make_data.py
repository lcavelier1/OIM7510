"""Make fake data for the Babson PT Clinic and save it as CSV files in data/.

Run it from the repository folder with:  uv run python projects/db/make_data.py
"""

import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path

random.seed(7510)  # same "random" data every run

AS_OF = date(2026, 11, 13)  # the last day of history; later appointments are only booked
FIRST_DAY = AS_OF - timedelta(days=365)  # 12 months of history
LAST_BOOKING_DAY = AS_OF + timedelta(days=28)  # bookings for the next four weeks

DATA = Path(__file__).parent / "data"
DATA.mkdir(exist_ok=True)


def save(name, rows):
    """Write a list of dicts to data/<name>.csv."""
    with open(DATA / f"{name}.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"{name}: {len(rows)} rows")


FIRST_NAMES = [
    "Ana", "Ben", "Carla", "David", "Elena", "Frank", "Grace", "Hector", "Isabel", "James",
    "Karen", "Luis", "Maria", "Nathan", "Olivia", "Pedro", "Quinn", "Rosa", "Sam", "Tara",
    "Umar", "Valeria", "Will", "Ximena", "Yusuf", "Zoe", "Liam", "Emma", "Noah", "Mia",
]
LAST_NAMES = [
    "Smith", "Garcia", "Johnson", "Lee", "Brown", "Martinez", "Davis", "Lopez", "Wilson", "Clark",
    "Nguyen", "Patel", "Kim", "Rossi", "Murphy", "Cohen", "Silva", "Walsh", "Chen", "Reyes",
]

# ---------- therapists ----------
therapists = [
    {"therapist_id": 1, "first_name": "Laura", "last_name": "Mejia", "credential": "DPT", "hire_date": "2019-03-04"},
    {"therapist_id": 2, "first_name": "Kevin", "last_name": "O'Brien", "credential": "DPT", "hire_date": "2020-08-17"},
    {"therapist_id": 3, "first_name": "Priya", "last_name": "Shah", "credential": "DPT", "hire_date": "2021-01-11"},
    {"therapist_id": 4, "first_name": "Marcus", "last_name": "Hill", "credential": "PTA", "hire_date": "2022-06-06"},
    {"therapist_id": 5, "first_name": "Sofia", "last_name": "Ramos", "credential": "PTA", "hire_date": "2023-02-13"},
    {"therapist_id": 6, "first_name": "Daniel", "last_name": "Park", "credential": "DPT", "hire_date": "2024-09-03"},
    {"therapist_id": 7, "first_name": "Hannah", "last_name": "Weiss", "credential": "PTA", "hire_date": "2025-04-21"},
]
for t in therapists:
    t["email"] = f"{t['first_name'].lower()}.{t['last_name'].lower().replace(chr(39), '')}@babsonpt.com"

# Each therapist has a slightly different no-show rate, so question 2 has something to find.
NO_SHOW_RATE = {1: 0.06, 2: 0.08, 3: 0.07, 4: 0.12, 5: 0.10, 6: 0.09, 7: 0.15}

# ---------- treatments ----------
treatments = [
    {"treatment_id": 1, "name": "Initial Evaluation", "standard_minutes": 45, "price": 180.00, "cost": 60.00},
    {"treatment_id": 2, "name": "Therapeutic Exercise", "standard_minutes": 15, "price": 55.00, "cost": 15.00},
    {"treatment_id": 3, "name": "Manual Therapy", "standard_minutes": 15, "price": 65.00, "cost": 20.00},
    {"treatment_id": 4, "name": "Neuromuscular Re-education", "standard_minutes": 15, "price": 60.00, "cost": 18.00},
    {"treatment_id": 5, "name": "Gait Training", "standard_minutes": 15, "price": 50.00, "cost": 14.00},
    {"treatment_id": 6, "name": "Ultrasound", "standard_minutes": 10, "price": 35.00, "cost": 8.00},
    {"treatment_id": 7, "name": "Electrical Stimulation", "standard_minutes": 15, "price": 40.00, "cost": 10.00},
    {"treatment_id": 8, "name": "Kinesio Taping", "standard_minutes": 10, "price": 30.00, "cost": 12.00},
    {"treatment_id": 9, "name": "Dry Needling", "standard_minutes": 20, "price": 90.00, "cost": 25.00},  # never given
    {"treatment_id": 10, "name": "Aquatic Therapy", "standard_minutes": 30, "price": 85.00, "cost": 40.00},  # never given
]
GIVEN_TREATMENTS = [2, 3, 4, 5, 6, 7, 8]  # follow-up visits use these; 1 is only for the first visit

# ---------- patients ----------
patients = []
member_number = 100000
for patient_id in range(1, 301):
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    birth = date(1945, 1, 1) + timedelta(days=random.randint(0, 365 * 60))
    if random.random() < 0.2:
        insurance = ""  # self-pay: no member number
    else:
        member_number = member_number + random.randint(1, 50)
        insurance = f"MBR{member_number}"
    patients.append({
        "patient_id": patient_id,
        "first_name": first,
        "last_name": last,
        "date_of_birth": birth.isoformat(),
        "phone": f"781-{random.randint(200, 999)}-{random.randint(1000, 9999)}",
        "email": f"{first.lower()}.{last.lower()}{patient_id}@example.com",
        "insurance_member_number": insurance,
    })

# Two patients share a name and a birthday with another patient (the scenario says this happens).
for copy_id, original_id in [(150, 40), (275, 212)]:
    patients[copy_id - 1]["first_name"] = patients[original_id - 1]["first_name"]
    patients[copy_id - 1]["last_name"] = patients[original_id - 1]["last_name"]
    patients[copy_id - 1]["date_of_birth"] = patients[original_id - 1]["date_of_birth"]

# ---------- referrals ----------
PHYSICIANS = ["Dr. Allen", "Dr. Brooks", "Dr. Carter", "Dr. Diaz", "Dr. Evans", "Dr. Fischer", "Dr. Gomez"]
REASONS = ["Low back pain", "Knee replacement rehab", "Rotator cuff tear", "Ankle sprain",
           "Neck pain", "ACL reconstruction", "Hip replacement rehab", "Tennis elbow"]

# Patients 289-300 are referred but never book an appointment (question 5).
NO_APPOINTMENT_PATIENTS = list(range(289, 301))

referrals = []
referral_id = 1
for p in patients:
    if p["patient_id"] in NO_APPOINTMENT_PATIENTS:
        how_many = 1
    else:
        how_many = random.choices([0, 1, 2, 3], weights=[30, 50, 15, 5])[0]
    for _ in range(how_many):
        referral_day = FIRST_DAY + timedelta(days=random.randint(0, 350))
        referrals.append({
            "referral_id": referral_id,
            "patient_id": p["patient_id"],
            "physician_name": random.choice(PHYSICIANS),
            "referral_date": referral_day.isoformat(),
            "reason": random.choice(REASONS),
        })
        referral_id = referral_id + 1

# ---------- appointments ----------
# Every patient with appointments gets one course of care: a first visit, then
# one or two visits a week with the same therapist.

taken = {}  # (therapist_id, day) -> list of (start, end) already booked


def is_free(therapist_id, start, length):
    """True if the therapist has nothing overlapping start..start+length."""
    end = start + timedelta(minutes=length)
    for other_start, other_end in taken.get((therapist_id, start.date()), []):
        if start < other_end and other_start < end:
            return False
    return True


def book(therapist_id, day, length):
    """Find a free half-hour start between 8:00 and 17:00 on that day, or return None."""
    starts = []
    for half_hours in range(0, 19):  # 8:00, 8:30, ... 17:00
        starts.append(datetime(day.year, day.month, day.day, 8, 0) + timedelta(minutes=30 * half_hours))
    random.shuffle(starts)
    for start in starts:
        if is_free(therapist_id, start, length):
            taken.setdefault((therapist_id, day), []).append((start, start + timedelta(minutes=length)))
            return start
    return None


appointments = []
appointment_id = 1
for p in patients:
    if p["patient_id"] in NO_APPOINTMENT_PATIENTS:
        continue
    therapist_id = random.choice([1, 1, 2, 2, 3, 3, 4, 5, 6, 7])
    visits = random.randint(6, 18)
    day = FIRST_DAY + timedelta(days=random.randint(0, 380))
    for visit in range(visits):
        while day.weekday() >= 5:  # move weekend days to Monday
            day = day + timedelta(days=1)
        if day > LAST_BOOKING_DAY:
            break
        if visit == 0:
            length = 60  # the first visit is the evaluation
        else:
            length = random.choice([30, 45, 45, 60])
        start = book(therapist_id, day, length)
        if start is not None:
            if day > AS_OF:
                status = "booked"
            else:
                rate = NO_SHOW_RATE[therapist_id]
                if day.weekday() == 0:  # Mondays have more no-shows
                    rate = rate + 0.05
                if random.random() < rate:
                    status = "no-show"
                else:
                    status = "completed"
            appointments.append({
                "appointment_id": appointment_id,
                "patient_id": p["patient_id"],
                "therapist_id": therapist_id,
                "starts_at": start.isoformat(sep=" "),
                "length_minutes": length,
                "status": status,
                "is_first_visit": visit == 0,
            })
            appointment_id = appointment_id + 1
        day = day + timedelta(days=random.choice([3, 4, 7, 7]))

# ---------- treatments given at each completed appointment ----------
price_of = {t["treatment_id"]: t["price"] for t in treatments}
minutes_of = {t["treatment_id"]: t["standard_minutes"] for t in treatments}

appointment_treatments = []
for a in appointments:
    if a["status"] != "completed":
        continue
    remaining = a["length_minutes"]
    chosen = []
    if a["is_first_visit"]:
        chosen.append(1)
        remaining = remaining - minutes_of[1]
    options = GIVEN_TREATMENTS.copy()
    random.shuffle(options)
    for treatment_id in options:
        if len(chosen) >= 4 or remaining < minutes_of[treatment_id]:
            continue
        chosen.append(treatment_id)
        remaining = remaining - minutes_of[treatment_id]
    for treatment_id in chosen:
        price = price_of[treatment_id]
        if random.random() < 0.1:  # sometimes a 15% discount that day
            price = round(price * 0.85, 2)
        appointment_treatments.append({
            "appointment_id": a["appointment_id"],
            "treatment_id": treatment_id,
            "price_charged": price,
            "minutes": minutes_of[treatment_id],
        })

# The two deliberate breaks for question 7: add 20 minutes to one treatment in
# two completed appointments, so their treatments take longer than the appointment.
BROKEN = []
for a in appointments:
    if a["status"] == "completed" and a["length_minutes"] == 30 and len(BROKEN) < 2 and a["appointment_id"] > 1000:
        BROKEN.append(a["appointment_id"])
for row in appointment_treatments:
    if row["appointment_id"] in BROKEN:
        row["minutes"] = row["minutes"] + 20
        BROKEN.remove(row["appointment_id"])  # only one treatment per appointment
        print(f"Broke the minutes rule on purpose in appointment {row['appointment_id']}")

for a in appointments:
    del a["is_first_visit"]  # helper column, not part of the table

save("therapists", therapists)
save("patients", patients)
save("referrals", referrals)
save("treatments", treatments)
save("appointments", appointments)
save("appointment_treatments", appointment_treatments)
