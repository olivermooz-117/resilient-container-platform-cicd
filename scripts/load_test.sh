#!/usr/bin/env bash
# Simple load test against the ALB to trigger ALBRequestCountPerTarget scaling
# Usage: ./load_test.sh <alb-dns> [seconds]
set -euo pipefail
ALB="${1:?alb dns required}"
DUR="${2:-120}"
end=$(( $(date +%s) + DUR ))
while [ "$(date +%s)" -lt "$end" ]; do
  curl -s "http://$ALB/health" > /dev/null
done
echo "load test complete"
