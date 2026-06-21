from datetime import datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Policy

policies_bp = Blueprint("policies", __name__)


@policies_bp.route("/")
def index():
    policies = Policy.query.order_by(Policy.updated_at.desc()).all()
    return render_template("policies/index.html", policies=policies)


@policies_bp.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        policy = Policy(
            title=request.form["title"],
            content=request.form.get("content"),
            version=request.form.get("version", "1.0"),
            status=request.form.get("status", "Taslak"),
            owner=request.form.get("owner"),
        )
        db.session.add(policy)
        db.session.commit()
        flash("Politika başarıyla eklendi.", "success")
        return redirect(url_for("policies.index"))
    return render_template("policies/form.html", policy=None, statuses=Policy.STATUSES)


@policies_bp.route("/<int:id>")
def view(id):
    policy = Policy.query.get_or_404(id)
    return render_template("policies/view.html", policy=policy)


@policies_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit(id):
    policy = Policy.query.get_or_404(id)
    if request.method == "POST":
        policy.title = request.form["title"]
        policy.content = request.form.get("content")
        policy.version = request.form.get("version", "1.0")
        policy.status = request.form.get("status", "Taslak")
        policy.owner = request.form.get("owner")
        policy.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        flash("Politika güncellendi.", "success")
        return redirect(url_for("policies.index"))
    return render_template("policies/form.html", policy=policy, statuses=Policy.STATUSES)


@policies_bp.route("/<int:id>/delete", methods=["POST"])
def delete(id):
    policy = Policy.query.get_or_404(id)
    db.session.delete(policy)
    db.session.commit()
    flash("Politika silindi.", "warning")
    return redirect(url_for("policies.index"))
