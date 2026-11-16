# Resilient Container Platform & CI/CD

**Region:** `us-east-2` (Ohio)
**Domain:** `oliver-capstone.work.gd`

## 1. Architecture Diagram
![Architecture Diagram](docs/screenshots/01-architecture.png)

## 2. CI/CD Proof
![CI/CD Pipeline](docs/screenshots/02-pipeline.png)

## 3. Scaling Proof
![Scaling Proof](docs/screenshots/03-scaling.png)

## 4. DR Runbook & Failover Proof
Route 53 Health Checks trigger a failover to an S3 static error page when the primary ALB is unhealthy. AWS Backup is configured for daily RDS snapshots.

![DR Failover](docs/screenshots/04-dr-failover.png)

## 5. AWS Backup Proof
![AWS Backup](docs/screenshots/05-dr-backup.png)
