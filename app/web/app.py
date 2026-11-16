import json
import os
import time
import uuid

import boto3
import redis
from flask import Flask, jsonify, request

app = Flask(__name__)

REGION = os.environ.get("AWS_REGION", "us-east-2")
QUEUE_URL = os.environ["SQS_QUEUE_URL"]
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "ecommerce")

sqs = boto3.client("sqs", region_name=REGION)
cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, socket_timeout=1, decode_responses=True)


@app.get("/health")
def health():
    return "ok", 200


@app.post("/order")
def create_order():
    body = request.get_json(silent=True) or {}
    order_id = str(uuid.uuid4())
    message = {
        "order_id": order_id,
        "item": body.get("item", "unknown"),
        "quantity": int(body.get("quantity", 1)),
        "created_at": int(time.time()),
    }
    sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=json.dumps(message))
    cache.setex(f"order:{order_id}", 300, "queued")
    return jsonify({"order_id": order_id, "status": "queued"}), 202


@app.get("/order/<order_id>")
def order_status(order_id):
    cached = cache.get(f"order:{order_id}")
    if cached:
        return jsonify({"order_id": order_id, "status": cached, "source": "cache"}), 200
    return jsonify({"order_id": order_id, "status": "unknown", "source": "miss"}), 404


@app.get("/")
def index():
    return jsonify({"service": "ecommerce-web", "region": REGION, "db_host": DB_HOST}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
