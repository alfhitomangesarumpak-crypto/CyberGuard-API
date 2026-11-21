from app import create_app
from app.extensions import db
from app.models import User, Asset, Vulnerability, Incident, IncidentResponse

app = create_app()

def seed_data():
    with app.app_context():
        print("Membersihkan data lama (jika ada)...")
        db.session.query(IncidentResponse).delete()
        db.session.query(Incident).delete()
        db.session.query(Vulnerability).delete()
        db.session.query(Asset).delete()
        db.session.query(User).delete()
        db.session.commit()

        # 1. Seed Users (Aktor SOC)
        admin = User(username="admin_soc", email="admin@cyberguard.local", role="admin")
        admin.set_password("AdminPass123!")

        analyst = User(username="budi_analyst", email="budi@cyberguard.local", role="analyst")
        analyst.set_password("AnalystPass123!")

        db.session.add_all([admin, analyst])
        db.session.commit()

        # 2. Seed Assets (Infrastruktur IT)
        asset1 = Asset(
            asset_name="Core-DB-Server-01",
            ip_address="10.10.1.15",
            asset_type="Database",
            criticality="critical",
            owner_department="Finance & Core Banking"
        )
        asset2 = Asset(
            asset_name="Web-Portal-Production",
            ip_address="192.168.100.24",
            asset_type="Web App",
            criticality="high",
            owner_department="Digital Services"
        )
        asset3 = Asset(
            asset_name="HR-Workstation-08",
            ip_address="172.16.5.42",
            asset_type="Workstation",
            criticality="medium",
            owner_department="Human Resources"
        )
        db.session.add_all([asset1, asset2, asset3])
        db.session.commit()

        # 3. Seed Vulnerabilities (Risiko / CVE)
        vuln1 = Vulnerability(
            asset_id=asset1.id,
            cve_code="CVE-2026-1042",
            title="PostgreSQL Privilege Escalation Vulnerability",
            cvss_score=8.8,
            severity="high",
            status="open"
        )
        vuln2 = Vulnerability(
            asset_id=asset2.id,
            cve_code="CVE-2026-2219",
            title="Cross-Site Scripting (XSS) on Login Parameter",
            cvss_score=6.1,
            severity="medium",
            status="in_progress"
        )
        vuln3 = Vulnerability(
            asset_id=asset2.id,
            cve_code="CVE-2025-9981",
            title="Outdated OpenSSL TLS Buffer Overflow",
            cvss_score=9.8,
            severity="critical",
            status="patched"
        )
        db.session.add_all([vuln1, vuln2, vuln3])
        db.session.commit()

        # 4. Seed Incidents (Laporan Insiden Keamanan)
        inc1 = Incident(
            asset_id=asset2.id,
            reported_by=analyst.id,
            title="Suspicious SQL Injection Payload Attempts",
            incident_type="Web Attack",
            severity="high",
            status="investigating",
            description="WAF mendeteksi 450 percobaan SQL injection dari IP eksternal dalam 10 menit."
        )
        inc2 = Incident(
            asset_id=asset3.id,
            reported_by=admin.id,
            title="Phishing Attachment Executed on HR PC",
            incident_type="Phishing",
            severity="critical",
            status="open",
            description="Karyawan membuka lampiran makro mencurigakan; terdeteksi koneksi keluar ke C2 server."
        )
        db.session.add_all([inc1, inc2])
        db.session.commit()

        # 5. Seed Incident Responses (Tindakan Mitigasi)
        resp1 = IncidentResponse(
            incident_id=inc1.id,
            responder_id=analyst.id,
            action_taken="Block Source IP on Firewall",
            notes="Memblokir subnet penyerang pada perimeter firewall dan mengaktifkan rate-limiting."
        )
        resp2 = IncidentResponse(
            incident_id=inc2.id,
            responder_id=admin.id,
            action_taken="Network Isolation",
            notes="Memutus koneksi jaringan HR-Workstation-08 dari VLAN internal untuk analisis forensik."
        )
        db.session.add_all([resp1, resp2])
        db.session.commit()

        print("Seeding selesai! Berhasil mengisi data simulasi ke 5 tabel.")

if __name__ == "__main__":
    seed_data()