# Babson PT Clinic

## The Scenario

I chose scenario D, the Babson PT Clinic: a physical therapy clinic run by Babson alumni that books on a paper calendar and keeps paper charts. It wants to book patients without double-booking a therapist, see what each treatment earns, and find patients it has lost touch with.

## The ERD

```mermaid
erDiagram
    THERAPISTS ||--o{ APPOINTMENTS : "sees"
    PATIENTS ||--o{ APPOINTMENTS : "books"
    PATIENTS ||--o{ REFERRALS : "is referred by"
    APPOINTMENTS ||--o{ APPOINTMENT_TREATMENTS : "includes"
    TREATMENTS ||--o{ APPOINTMENT_TREATMENTS : "is given at"

    THERAPISTS {
        int therapist_id PK
        varchar first_name
        varchar last_name
        varchar credential "DPT or PTA"
        varchar email UK
        date hire_date
    }
    PATIENTS {
        int patient_id PK
        varchar first_name
        varchar last_name
        date date_of_birth
        varchar phone
        varchar email
        varchar insurance_member_number UK "null if self-pay"
    }
    REFERRALS {
        int referral_id PK
        int patient_id FK
        varchar physician_name
        date referral_date
        varchar reason
    }
    TREATMENTS {
        int treatment_id PK
        varchar name UK
        int standard_minutes
        decimal price
        decimal cost
    }
    APPOINTMENTS {
        int appointment_id PK
        int patient_id FK
        int therapist_id FK
        timestamp starts_at
        int length_minutes "30, 45 or 60"
        varchar status "booked, completed or no-show"
    }
    APPOINTMENT_TREATMENTS {
        int appointment_id PK, FK
        int treatment_id PK, FK
        decimal price_charged
        int minutes
    }
```

## What One Row Means


- `therapists`: One row of `therapists` is one physical therapist who works at the clinic.
- `patients`: One row of `patients` is one person who receives care at the clinic.
- `referrals`: One row of `referrals` is one physician sending one patient to the clinic on one date.
- `treatments`: One row of `treatments` is one type of procedure the clinic uses to treat its patients' conditions.
- `appointments`: One row of `appointments` is one scheduled time with a specific therapist to see one patient.
- `appointment_treatments`: One row of `appointment_treatments` is one treatment given during one scheduled appointment.

## Design Choices

**Keys.** I used a separate ID for each table (`patient_id`, `therapist_id`, etc.) instead of using names or insurance numbers. This makes more sense because two patients could have the same name and date of birth, and self-pay patients don't necessarily have an insurance number.

**Optional relationships.** Not every patient has a referral, and not every treatment is necessarily used. For example, Dry Needling and Aquatic Therapy have no appointments associated with them. In the ERD, I used a circle to represent these optional relationships, meaning that there can be zero or more.

**Rules the tables can't hold.** There are some rules that cannot be checked directly through the table structure. For example, the total treatment time during an appointment cannot be longer than the appointment itself. Also, a therapist cannot have two appointments that overlap, such as one appointment from 9:00 to 10:00 and another starting at 9:30. Since these rules involve comparing information across multiple rows, I used queries to check them instead. Question 7 in `questions.py` identifies the appointments where the treatment time exceeds the appointment length.

**Something I changed from the agent.** The agent originally generated appointment data that was not very realistic, with too many appointments on Mondays and almost none on Wednesdays. I noticed this when looking at the chart in `build.py`, so I asked for the data to be adjusted to make the weekly distribution look more like a real clinic. The change is included in the commit "db: add build.py and fix make_data.py because the weekdays were wrong".