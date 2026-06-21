from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Control

controls_bp = Blueprint("controls", __name__)


@controls_bp.route("/")
def index():
    category = request.args.get("category")
    status = request.args.get("status")

    query = Control.query
    if category:
        query = query.filter_by(category=category)
    if status:
        query = query.filter_by(status=status)

    controls = query.order_by(Control.control_id).all()
    categories = db.session.query(Control.category).distinct().order_by(Control.category).all()
    categories = [c[0] for c in categories]

    totals = {s: Control.query.filter_by(status=s).count() for s in Control.STATUSES}
    totals["Toplam"] = Control.query.count()

    return render_template(
        "controls/index.html",
        controls=controls,
        categories=categories,
        statuses=Control.STATUSES,
        selected_category=category,
        selected_status=status,
        totals=totals,
    )


@controls_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit(id):
    control = Control.query.get_or_404(id)
    if request.method == "POST":
        control.status = request.form.get("status", "Uygulanmadı")
        control.evidence = request.form.get("evidence")
        control.responsible = request.form.get("responsible")
        control.notes = request.form.get("notes")
        db.session.commit()
        flash("Kontrol güncellendi.", "success")
        return redirect(url_for("controls.index"))
    return render_template("controls/form.html", control=control, statuses=Control.STATUSES)
