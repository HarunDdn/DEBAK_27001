from flask import Blueprint, render_template
from app.models import Asset, Risk, Policy, Incident, Control

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def dashboard():
    stats = {
        "assets": Asset.query.count(),
        "risks_open": Risk.query.filter_by(status="Açık").count(),
        "risks_high": sum(
            1 for r in Risk.query.all() if r.risk_level == "Yüksek"
        ),
        "policies_approved": Policy.query.filter_by(status="Onaylandı").count(),
        "policies_total": Policy.query.count(),
        "incidents_open": Incident.query.filter_by(status="Açık").count(),
        "incidents_total": Incident.query.count(),
        "controls_implemented": Control.query.filter_by(status="Uygulandı").count(),
        "controls_total": Control.query.count(),
    }

    if stats["controls_total"] > 0:
        stats["controls_pct"] = round(
            stats["controls_implemented"] / stats["controls_total"] * 100, 1
        )
    else:
        stats["controls_pct"] = 0

    recent_risks = (
        Risk.query.filter_by(status="Açık")
        .order_by(Risk.created_at.desc())
        .limit(5)
        .all()
    )
    recent_incidents = (
        Incident.query.filter(Incident.status.in_(["Açık", "İnceleniyor"]))
        .order_by(Incident.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard.html",
        stats=stats,
        recent_risks=recent_risks,
        recent_incidents=recent_incidents,
    )
