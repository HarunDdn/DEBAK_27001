from datetime import datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Incident

incidents_bp = Blueprint("incidents", __name__)


@incidents_bp.route("/")
def index():
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    return render_template("incidents/index.html", incidents=incidents)


@incidents_bp.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        incident = Incident(
            title=request.form["title"],
            description=request.form.get("description"),
            severity=request.form.get("severity", "Orta"),
            status=request.form.get("status", "Açık"),
            reporter=request.form.get("reporter"),
            assignee=request.form.get("assignee"),
        )
        db.session.add(incident)
        db.session.commit()
        flash("Olay başarıyla kaydedildi.", "success")
        return redirect(url_for("incidents.index"))
    return render_template("incidents/form.html", incident=None,
                           severities=Incident.SEVERITIES, statuses=Incident.STATUSES)


@incidents_bp.route("/<int:id>")
def view(id):
    incident = Incident.query.get_or_404(id)
    return render_template("incidents/view.html", incident=incident,
                           severities=Incident.SEVERITIES, statuses=Incident.STATUSES)


@incidents_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit(id):
    incident = Incident.query.get_or_404(id)
    if request.method == "POST":
        incident.title = request.form["title"]
        incident.description = request.form.get("description")
        incident.severity = request.form.get("severity", "Orta")
        incident.assignee = request.form.get("assignee")
        incident.resolution = request.form.get("resolution")
        new_status = request.form.get("status", "Açık")
        if new_status in ("Çözüldü", "Kapatıldı") and incident.status not in ("Çözüldü", "Kapatıldı"):
            incident.resolved_at = datetime.now(timezone.utc)
        incident.status = new_status
        db.session.commit()
        flash("Olay güncellendi.", "success")
        return redirect(url_for("incidents.view", id=id))
    return render_template("incidents/form.html", incident=incident,
                           severities=Incident.SEVERITIES, statuses=Incident.STATUSES)


@incidents_bp.route("/<int:id>/delete", methods=["POST"])
def delete(id):
    incident = Incident.query.get_or_404(id)
    db.session.delete(incident)
    db.session.commit()
    flash("Olay silindi.", "warning")
    return redirect(url_for("incidents.index"))
