from flask import render_template, redirect, url_for, Blueprint, jsonify, request

from app import db
from app.models import URL
from app.utils import generate_uuid

import urllib.parse

bp = Blueprint("routes", __name__)


@bp.app_errorhandler(404)
def not_found_error(error):
    # TODO: add error feedback for user
    return redirect(url_for("routes.index"))


@bp.route('/')
@bp.route("/<slug>")
def index(slug=None):
    if slug:
        forward_url = URL.query.filter_by(slug=slug).first_or_404().forward_url

        if forward_url.find("http://") != 0 and forward_url.find("https://") != 0:
            forward_url = "http://" + forward_url

        return redirect(forward_url)

    return render_template("index.html")


@bp.route("/generate_link", methods=["POST"])
def generate_link():
    forward_url = request.form.get("forward_url", "", str)
    if not forward_url:
        return jsonify({"status_msg": "A forward_url must be supplied for link generation."}), 400

    slug = request.form.get("slug", "", str)
    if not slug:
        slug = generate_uuid()

    if URL.query.filter_by(slug=slug).first():
        return jsonify({"status_msg": "Slug already in use :/"}), 400

    db.session.add(URL(slug, forward_url))
    db.session.commit()

    return jsonify({
        "slug": slug,
        "forward_url": forward_url,
        "short_url": urllib.parse.urljoin(request.base_url, slug)
    }), 200
