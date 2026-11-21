# CyberGuard-API 🛡️

**CyberGuard-API** adalah layanan RESTful API berbasis **Python (Flask)** dengan arsitektur **MVC (Model-View-Controller)** untuk manajemen operasi keamanan siber (*Cybersecurity Operations Management*). Sistem ini mengelola inventaris aset IT, pemantauan kerentanan (*vulnerabilities*), pelaporan insiden keamanan (*incidents*), hingga pencatatan tindakan respons insiden (*incident responses*).

---

## Fitur Utama & Arsitektur

* **Arsitektur MVC Modular:** Pemisahan kode yang jelas antara lapisan database (`models`), validasi (`schemas`), logika bisnis (`controllers`), dan routing (`routes`).
* **5 Entitas Relasional:** `User`, `Asset`, `Vulnerability`, `Incident`, dan `IncidentResponse` yang terhubung menggunakan *Foreign Key* dan relasi ORM SQLAlchemy.
* **Validasi Input Ketat:** Menggunakan **Marshmallow** untuk memvalidasi format email, alamat IPv4, skor CVSS (`0.0` – `10.0`), dan tingkat keparahan (*severity*).
* **Global Error Handling:** Format respons error JSON yang seragam untuk kode HTTP `400`, `401`, `404`, `405`, dan `500`.
* **Automated Testing:** Pengujian otomatis seluruh alur CRUD dan relasi entitas menggunakan **Pytest**.

---

## Struktur Proyek

```text
CyberGuard-API/
├── app/
│   ├── controllers/        # Logika bisnis CRUD & penanganan transaksi DB
│   ├── models/             # Definisi tabel & relasi SQLAlchemy
│   ├── routes/             # Definisi Blueprint & endpoint REST API
│   ├── schemas/            # Skema serialisasi & validasi Marshmallow
│   ├── __init__.py         # Application Factory & Global Error Handlers
│   └── extensions.py       # Inisialisasi SQLAlchemy & Flask-Migrate
├── migrations/             # File migrasi skema database
├── tests/
│   └── test_api.py         # Automated unit & integration testing (Pytest)
├── config.py               # Konfigurasi environment & database
├── requirements.txt        # Daftar dependensi Python
├── run.py                  # Entry point server Flask
├── seed.py                 # Script pengisian data simulasi awal
└── README.md               # Dokumentasi proyek

## Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    USERS ||--o{ INCIDENTS : "reports (reported_by)"
    USERS ||--o{ INCIDENT_RESPONSES : "handles (responder_id)"
    ASSETS ||--o{ VULNERABILITIES : "has (asset_id)"
    ASSETS ||--o{ INCIDENTS : "affected_in (asset_id)"
    INCIDENTS ||--o{ INCIDENT_RESPONSES : "resolved_by (incident_id)"

    USERS {
        int id PK
        string username
        string email
        string password_hash
        string role
        datetime created_at
    }
    ASSETS {
        int id PK
        string asset_name
        string ip_address
        string asset_type
        string criticality
        string owner_department
        datetime created_at
    }
    VULNERABILITIES {
        int id PK
        int asset_id FK
        string cve_code
        string title
        float cvss_score
        string severity
        string status
        datetime discovered_at
    }
    INCIDENTS {
        int id PK
        int asset_id FK
        int reported_by FK
        string title
        string incident_type
        string severity
        string status
        text description
        datetime reported_at
    }
    INCIDENT_RESPONSES {
        int id PK
        int incident_id FK
        int responder_id FK
        text action_taken
        text notes
        datetime responded_at
    }