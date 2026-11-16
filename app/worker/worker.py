import json
import os
import signal
import sys
import time

import boto3
import redis

REGION = os.environ.get("AWS_REGION", "us-east-2")
QUEUE_URL = os.environ["SQS_QUEUE_URL"]
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))

sqs = boto3.client("sqs", region_name=REGION)
cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, socket_timeout=1, decode_responses=True)

running = True

def handle_sigterm(signum, frame):
    global running
    print("SIGTERM received, finishing current message and exiting...", flush=True)
    running = False

signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGINT, handle_sigterm)

def process(message):
    body = json.loads(message["Body"])
    order_id = body.get("order_id")
    time.sleep(0.2)
    cache.setex(f"order:{order_id}", 300, "processed")
    print(f"processed order={order_id} item={body.get('item')} qty={body.get('quantity', 1)}", flush=True)

def main():
    print(f"worker started; polling {QUEUE_URL}", flush=True)
    while running:
        resp = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=20,
            VisibilityTimeout=60,
        )
        for msg in resp.get("Messages", []):
            if not running:
                break
            try:
                process(msg)
                sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=msg["ReceiptHandle"])
            except Exception as e:
                print(f"error processing message: {e}", flush=True)
    print("worker exiting cleanly", flush=True)
    sys.exit(0)

if __name__ == "__main__":
    main()
