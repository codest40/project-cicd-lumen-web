from flask import Blueprint, render_template, jsonify, request
import logging
import asyncio
import logic
import crud

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="(%(asctime)s) [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("run.log")
    ]
)

page = Blueprint("page", __name__)


# ------------------------------
# HTML Routes (async)
# ------------------------------
@page.get("/")
async def home():
    # render_template is blocking — run it in a thread to keep the event loop free
    rendered = await asyncio.to_thread(render_template, "test.html")
    return rendered


@page.get("/home")
async def test():
    rendered = await asyncio.to_thread(render_template, "index.html")
    return rendered


# ------------------------------
# API Routes (async)
# ------------------------------
@page.get("/api/get-item")
async def get_item():
    try:
        result = await logic.get_data()
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error in get_item(): {e}")
        return jsonify({"error": str(e)}), 500


@page.post("/api-search")
async def api_search():
    try:
        data = request.get_json()
        name = (data.get("name", "") if data else "").strip()
        result = await logic.get_search(name)
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Error in api_search(): {e}")
        return jsonify({"error": str(e)}), 500





# ------------------------
# VISITORS
# ------------------------
@page.route("/api/visitors", methods=["GET"])
async def visitors_get():
    return jsonify(await crud.get_visitors()), 200

@page.route("/api/visitors", methods=["POST"])
async def visitors_post():
    data = request.get_json()
    name = data.get("name")
    return jsonify(await crud.add_visitor(name)), 201

@page.route("/api/visitors/<int:item_id>", methods=["DELETE"])
async def visitors_delete(item_id):
    return jsonify(await crud.delete_visitor(item_id)), 200


# ------------------------
# HEALTH
# ------------------------
@page.route("/api/health", methods=["GET"])
async def health_get():
    return jsonify(await crud.get_health()), 200

@page.route("/api/health", methods=["POST"])
async def health_post():
    data = request.get_json()
    status = data.get("status")
    info = data.get("info", "")
    return jsonify(await crud.add_health(status, info)), 201

@page.route("/api/health/<int:item_id>", methods=["DELETE"])
async def health_delete(item_id):
    return jsonify(await crud.delete_health(item_id)), 200
