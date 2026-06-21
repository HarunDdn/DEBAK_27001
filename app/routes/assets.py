from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Asset

assets_bp = Blueprint("assets", __name__)


@assets_bp.route("/")
def index():
    assets = Asset.query.order_by(Asset.created_at.desc()).all()
    return render_template("assets/index.html", assets=assets)


@assets_bp.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        asset = Asset(
            name=request.form["name"],
            description=request.form.get("description"),
            category=request.form.get("category"),
            owner=request.form.get("owner"),
            classification=request.form.get("classification", "Dahili"),
        )
        db.session.add(asset)
        db.session.commit()
        flash("Varlık başarıyla eklendi.", "success")
        return redirect(url_for("assets.index"))
    return render_template("assets/form.html", asset=None, categories=Asset.CATEGORIES, classifications=Asset.CLASSIFICATIONS)


@assets_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit(id):
    asset = Asset.query.get_or_404(id)
    if request.method == "POST":
        asset.name = request.form["name"]
        asset.description = request.form.get("description")
        asset.category = request.form.get("category")
        asset.owner = request.form.get("owner")
        asset.classification = request.form.get("classification", "Dahili")
        db.session.commit()
        flash("Varlık güncellendi.", "success")
        return redirect(url_for("assets.index"))
    return render_template("assets/form.html", asset=asset, categories=Asset.CATEGORIES, classifications=Asset.CLASSIFICATIONS)


@assets_bp.route("/<int:id>/delete", methods=["POST"])
def delete(id):
    asset = Asset.query.get_or_404(id)
    db.session.delete(asset)
    db.session.commit()
    flash("Varlık silindi.", "warning")
    return redirect(url_for("assets.index"))
