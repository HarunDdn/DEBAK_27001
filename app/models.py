from datetime import datetime, timezone
from app import db


class Asset(db.Model):
    __tablename__ = "assets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    owner = db.Column(db.String(100))
    classification = db.Column(db.String(50), default="Dahili")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    risks = db.relationship("Risk", back_populates="asset", lazy=True)

    CATEGORIES = ["Donanım", "Yazılım", "Veri", "İnsan", "Hizmet", "Tesis", "Diğer"]
    CLASSIFICATIONS = ["Genel", "Dahili", "Gizli", "Çok Gizli"]


class Risk(db.Model):
    __tablename__ = "risks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    asset_id = db.Column(db.Integer, db.ForeignKey("assets.id"), nullable=True)
    likelihood = db.Column(db.Integer, default=1)   # 1-5
    impact = db.Column(db.Integer, default=1)        # 1-5
    treatment = db.Column(db.String(50), default="Kabul Et")
    treatment_plan = db.Column(db.Text)
    status = db.Column(db.String(50), default="Açık")
    owner = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    asset = db.relationship("Asset", back_populates="risks")

    TREATMENTS = ["Kabul Et", "Azalt", "Aktar", "Kaçın"]
    STATUSES = ["Açık", "İşleniyor", "Kapalı"]

    @property
    def risk_score(self):
        return self.likelihood * self.impact

    @property
    def risk_level(self):
        score = self.risk_score
        if score <= 5:
            return "Düşük"
        elif score <= 12:
            return "Orta"
        else:
            return "Yüksek"

    @property
    def risk_level_class(self):
        level = self.risk_level
        return {"Düşük": "success", "Orta": "warning", "Yüksek": "danger"}.get(level, "secondary")


class Policy(db.Model):
    __tablename__ = "policies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    version = db.Column(db.String(20), default="1.0")
    status = db.Column(db.String(50), default="Taslak")
    owner = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    STATUSES = ["Taslak", "Gözden Geçiriliyor", "Onaylandı", "Arşivlendi"]


class Incident(db.Model):
    __tablename__ = "incidents"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    severity = db.Column(db.String(50), default="Orta")
    status = db.Column(db.String(50), default="Açık")
    reporter = db.Column(db.String(100))
    assignee = db.Column(db.String(100))
    resolution = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    resolved_at = db.Column(db.DateTime, nullable=True)

    SEVERITIES = ["Düşük", "Orta", "Yüksek", "Kritik"]
    STATUSES = ["Açık", "İnceleniyor", "Çözüldü", "Kapatıldı"]

    @property
    def severity_class(self):
        return {
            "Düşük": "success",
            "Orta": "warning",
            "Yüksek": "danger",
            "Kritik": "dark",
        }.get(self.severity, "secondary")


class Control(db.Model):
    __tablename__ = "controls"

    id = db.Column(db.Integer, primary_key=True)
    control_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(300), nullable=False)
    category = db.Column(db.String(100))
    status = db.Column(db.String(50), default="Uygulanmadı")
    evidence = db.Column(db.Text)
    responsible = db.Column(db.String(100))
    notes = db.Column(db.Text)

    STATUSES = ["Uygulanmadı", "Kısmi", "Uygulandı", "Geçerli Değil"]

    @property
    def status_class(self):
        return {
            "Uygulanmadı": "danger",
            "Kısmi": "warning",
            "Uygulandı": "success",
            "Geçerli Değil": "secondary",
        }.get(self.status, "secondary")
