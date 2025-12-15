# ERD for HCAD Alumni Voting System (clean mermaid syntax)

```mermaid
erDiagram
    ELECTION ||--o{ POSITION : has
    ELECTION ||--o{ NOMINATION : includes
    ELECTION ||--o{ ELECTION_REMINDER : schedules

    POSITION ||--o{ CANDIDATE : offers
    POSITION ||--o{ NOMINATION : requested_for
    POSITION ||--o{ VOTE : receives

    VOTER ||--o{ NOMINATION : submits
    VOTER ||--o{ VOTE : casts
    CANDIDATE ||--o{ VOTE : chosen_in

    NOMINATION ||--|| CANDIDATE : promoted_to

    VOTER ||--o{ NOTIFICATION : receives
    USER ||--|| ADMIN_SESSION : owns

    ELECTION {
      int id
      string name
      string description
      datetime nomination_start
      datetime nomination_end
      datetime voting_start
      datetime voting_end
      datetime results_at
      bool auto_publish_results
      bool results_published
      datetime results_published_at
      bool is_active
      string mode
      string demo_phase
      datetime created_at
      datetime updated_at
    }

    POSITION {
      int id
      int election_id
      string name
      bool is_active
      int seats
      int display_order
    }

    VOTER {
      int id
      string voter_id
      string name
      int batch_year
      string campus_chapter
      string email
      string phone
      bool privacy_consent
      string pin
      bool has_voted
      bool is_active
      string session_token
      datetime created_at
      datetime updated_at
    }

    NOMINATION {
      int id
      int election_id
      int position_id
      int nominator_id
      string nominee_full_name
      int nominee_batch_year
      string nominee_campus_chapter
      string contact_email
      string contact_phone
      string reason
      string nominee_photo
      bool is_good_standing
      string status
      string rejection_reason
      bool promoted
      datetime promoted_at
      datetime created_at
    }

    CANDIDATE {
      int id
      int position_id
      int source_nomination_id
      string full_name
      int batch_year
      string campus_chapter
      string contact_email
      string contact_phone
      string bio
      string photo
      bool is_official
    }

    VOTE {
      int id
      int voter_id
      int position_id
      int candidate_id
      datetime created_at
    }

    ELECTION_REMINDER {
      int id
      int election_id
      date remind_at
      string note
      datetime created_at
    }

    NOTIFICATION {
      int id
      int voter_id
      string type
      string message
      bool is_read
      bool is_hidden
      datetime created_at
    }

    ADMIN_SESSION {
      int id
      int user_id
      string token
      datetime created_at
    }

    ACCESS_GATE {
      int id
      string name
      string passcode_hash
      int version
      datetime updated_at
    }

    USER {
      int id
      string username
      string auth_user_placeholder
    }
```

Notes:
- Simplified to pure Mermaid syntax (no PK/UNIQUE tags); relationships carry cardinality.
- If your preview still caches the old block, close and reopen the preview tab.
