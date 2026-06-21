from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Risk, Asset

risks_bp = Blueprint("risks", __name__)


@risks_bp.route("/")
def index():
    risks = Risk.query.order_by(Risk.created_at.desc()).all()
    return render_template("risks/index.html", risks=risks)


@risks_bp.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        asset_id = request.form.get("asset_id") or None
        risk = Risk(
            title=request.form["title"],
            description=request.form.get("description"),
            asset_id=int(asset_id) if asset_id else None,
            likelihood=int(request.form.get("likelihood", 1)),
            impact=int(request.form.get("impact", 1)),
            treatment=request.form.get("treatment", "Kabul Et"),
            treatment_plan=request.form.get("treatment_plan"),
            status=request.form.get("status", "Açık"),
            owner=request.form.get("owner"),
        )
        db.session.add(risk)
        db.session.commit()
        flash("Risk başarıyla eklendi.", "success")
        return redirect(url_for("risks.index"))
    assets = Asset.query.order_by(Asset.name).all()
    return render_template("risks/form.html", risk=None, assets=assets,
                           treatments=Risk.TREATMENTS, statuses=Risk.STATUSES)


@risks_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit(id):
    risk = Risk.query.get_or_404(id)
    if request.method == "POST":
        asset_id = request.form.get("asset_id") or None
        risk.title = request.form["title"]
        risk.description = request.form.get("description")
        risk.asset_id = int(asset_id) if asset_id else None
        risk.likelihood = int(request.form.get("likelihood", 1))
        risk.impact = int(request.form.get("impact", 1))
        risk.treatment = request.form.get("treatment", "Kabul Et")
        risk.treatment_plan = request.form.get("treatment_plan")
        risk.status = request.form.get("status", "Açık")
        risk.owner = request.form.get("owner")
        db.session.commit()
        flash("Risk güncellendi.", "success")
        return redirect(url_for("risks.index"))
    assets = Asset.query.order_by(Asset.name).all()
    return render_template("risks/form.html", risk=risk, assets=assets,
                           treatments=Risk.TREATMENTS, statuses=Risk.STATUSES)


@risks_bp.route("/<int:id>/delete", methods=["POST"])
def delete(id):
    risk = Risk.query.get_or_404(id)
    db.session.delete(risk)
    db.session.commit()
    flash("Risk silindi.", "warning")
    return redirect(url_for("risks.index"))
