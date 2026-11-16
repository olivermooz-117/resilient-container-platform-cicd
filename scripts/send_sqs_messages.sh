#!/usr/bin/env bash
# Sends N orders to the ALB to prove web -> SQS -> worker decoupling
# Usage: ./send_sqs_messages.sh <alb-dns> [count]
set -euo pipefail
ALB="${1:?alb dns required}"
COUNT="${2:-20}"
for i in $(seq 1 "$COUNT"); do
  curl -s -X POST "http://$ALB/order" \
    -H "Content-Type: application/json" \
    -d "{\"item\":\"widget$i\",\"quantity\":1}" > /dev/null
done
echo "sent $COUNT orders"
