# TV Show Catalog ERD

```mermaid
erDiagram
    SHOWS ||--o{ CREDITS : "has"
    PEOPLE ||--o{ CREDITS : "has"
    SHOWS ||--o{ SHOW_GENRES : "has"

    SHOWS {
        int show_id PK
        varchar title
        int year
        varchar type
        int episodes
        double rating
        int votes
    }
    PEOPLE {
        int people_id PK
        varchar name
        int birth_year
    }
    CREDITS {
        int show_id PK, FK
        int people_id PK, FK
        varchar role PK
    }
    SHOW_GENRES {
        int show_id PK, FK
        varchar genre PK
    }
```

## Assumptions

- A show can have more than one genre and many people involved, so I made different tables for each.
- Two shows can have the same name, so each one has an id.