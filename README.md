# Resilient Container Platform & CI/CD

**Region:** `us-east-2` (Ohio)
**Domain:** `oliver-capstone.work.gd`

## 1. Architecture Diagram
![Architecture Diagram](docs/screenshots/Architecture.png)

## 2. CI/CD Proof
![CI/CD Pipeline](docs/screenshots/pipeline.png)

## 3. Scaling Proof
![Scaling Proof](docs/screenshots/scaling.png)

## 4. DR Runbook & Failover Proof
Route 53 Health Checks trigger a failover to an S3 static error page when the primary ALB is unhealthy. AWS Backup is configured for daily RDS snapshots.

![DR Failover](docs/screenshots/dr-failover.png)

## 5. AWS Backup Proof
![AWS Backup](docs/screenshots/dr-backup.png)
