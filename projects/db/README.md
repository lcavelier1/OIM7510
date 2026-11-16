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

<!-- TODO Laura: fill in after the first commit -->
