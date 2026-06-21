import pytest
from app import create_app, db
from app.models import Asset, Risk, Policy, Incident, Control


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "test-secret"


@pytest.fixture
def app():
    application = create_app("tests.test_app.TestConfig")
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# ── Dashboard ────────────────────────────────────────────────────────────────

def test_dashboard_loads(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"DEBAK" in resp.data


# ── Assets ───────────────────────────────────────────────────────────────────

def test_asset_list_empty(client):
    resp = client.get("/assets/")
    assert resp.status_code == 200


def test_asset_create_and_list(client):
    resp = client.post(
        "/assets/new",
        data={"name": "Sunucu", "category": "Donanım", "classification": "Dahili", "owner": "BT"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Sunucu" in resp.data


def test_asset_edit(client, app):
    with app.app_context():
        asset = Asset(name="Laptop", category="Donanım", classification="Dahili")
        db.session.add(asset)
        db.session.commit()
        asset_id = asset.id

    resp = client.post(
        f"/assets/{asset_id}/edit",
        data={"name": "Laptop Pro", "category": "Donanım", "classification": "Gizli"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Laptop Pro" in resp.data


def test_asset_delete(client, app):
    with app.app_context():
        asset = Asset(name="Silinecek Varlık", classification="Dahili")
        db.session.add(asset)
        db.session.commit()
        asset_id = asset.id

    resp = client.post(f"/assets/{asset_id}/delete", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Silinecek Varl" not in resp.data


# ── Risks ────────────────────────────────────────────────────────────────────

def test_risk_list_empty(client):
    resp = client.get("/risks/")
    assert resp.status_code == 200


def test_risk_create(client):
    resp = client.post(
        "/risks/new",
        data={
            "title": "Yetkisiz Erişim",
            "likelihood": "4",
            "impact": "5",
            "treatment": "Azalt",
            "status": "Açık",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Yetkisiz" in resp.data


def test_risk_score_property(app):
    with app.app_context():
        risk = Risk(title="Test", likelihood=4, impact=3)
        assert risk.risk_score == 12
        assert risk.risk_level == "Orta"

        risk_high = Risk(title="Yüksek", likelihood=5, impact=5)
        assert risk_high.risk_score == 25
        assert risk_high.risk_level == "Yüksek"

        risk_low = Risk(title="Düşük", likelihood=1, impact=2)
        assert risk_low.risk_score == 2
        assert risk_low.risk_level == "Düşük"


# ── Policies ─────────────────────────────────────────────────────────────────

def test_policy_create_and_view(client, app):
    resp = client.post(
        "/policies/new",
        data={
            "title": "Erişim Kontrolü Politikası",
            "version": "1.0",
            "status": "Onaylandı",
            "owner": "BGYS Ekibi",
            "content": "Erişim yetkileri en az ayrıcalık ilkesiyle verilir.",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Eri" in resp.data

    with app.app_context():
        policy = Policy.query.first()
        assert policy is not None
        policy_id = policy.id

    resp2 = client.get(f"/policies/{policy_id}")
    assert resp2.status_code == 200


# ── Incidents ────────────────────────────────────────────────────────────────

def test_incident_create_and_list(client):
    resp = client.post(
        "/incidents/new",
        data={
            "title": "Phishing E-postası",
            "severity": "Yüksek",
            "status": "Açık",
            "reporter": "Ahmet Yılmaz",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Phishing" in resp.data


def test_incident_resolve(client, app):
    with app.app_context():
        inc = Incident(title="Test Olayı", severity="Orta", status="Açık")
        db.session.add(inc)
        db.session.commit()
        inc_id = inc.id

    resp = client.post(
        f"/incidents/{inc_id}/edit",
        data={
            "title": "Test Olayı",
            "severity": "Orta",
            "status": "Çözüldü",
            "resolution": "Sorun giderildi.",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200

    with app.app_context():
        updated = db.session.get(Incident, inc_id)
        assert updated.status == "Çözüldü"
        assert updated.resolved_at is not None


# ── Controls ─────────────────────────────────────────────────────────────────

def test_controls_seeded(client, app):
    with app.app_context():
        count = Control.query.count()
        assert count > 0, "Annex A kontrolleri tohumlanmış olmalı"


def test_controls_list(client):
    resp = client.get("/controls/")
    assert resp.status_code == 200
    assert b"A.5" in resp.data


def test_control_edit(client, app):
    with app.app_context():
        ctrl = Control.query.first()
        ctrl_id = ctrl.id

    resp = client.post(
        f"/controls/{ctrl_id}/edit",
        data={
            "status": "Uygulandı",
            "responsible": "BT Güvenlik",
            "evidence": "Politika dokümanı mevcut.",
            "notes": "",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200

    with app.app_context():
        updated = db.session.get(Control, ctrl_id)
        assert updated.status == "Uygulandı"
        assert updated.responsible == "BT Güvenlik"


def test_controls_filter_by_category(client, app):
    with app.app_context():
        category = Control.query.first().category

    resp = client.get(f"/controls/?category={category}")
    assert resp.status_code == 200


def test_controls_filter_by_status(client):
    resp = client.get("/controls/?status=Uygulanmadı")
    assert resp.status_code == 200
