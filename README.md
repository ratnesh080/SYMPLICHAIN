
# Symplichain Software Engineering Intern Challenge

This repository contains the technical proposal and CI/CD configuration for the Symplichain Hackathon. It addresses system design for rate-limiting, mobile architecture strategy, automated deployment pipelines, and production debugging.

## 1. Shared Gateway Solution (Part 1)
**The Problem:** Managing a hard limit of 3 req/s across 25+ customers who may exceed 20 req/s during peak hours.

### Architecture: Distributed Fair Queuing
To ensure both **rate enforcement** and **customer fairness**, I propose using **Redis-backed per-customer queues**.

* **Mechanism:** Instead of a single global queue, each `customer_id` gets its own Redis List.
* **The Throttler:** A dedicated worker runs a loop with a precise "tick" of 333ms ($1000ms / 3$ requests).
* **Fairness:** The worker uses a **Round-Robin** selection. In each tick, it identifies the next customer with a non-empty queue and processes exactly one request. 
    * *Result:* If Customer A has 100 requests and Customer B has 1, Customer B will be served within a maximum of 2 "ticks" (666ms), regardless of Customer A's volume.
* **Failure Handling:** I've implemented a **Retry with Exponential Backoff** strategy (2s, 4s, 8s). If the external API returns a 5xx error, the task is re-queued with an incremented retry counter. After 3 attempts, it is moved to a Dead Letter Queue (DLQ) for manual inspection to avoid "poison pill" tasks clogging the worker.

---

## 2. Mobile Architecture (Part 2)
### Tech Stack: React Native + Tailwind (NativeWind)
* **Why:** Given that the SymFlow web platform uses **React and Tailwind**, React Native allows for maximum code reuse of business logic, validation schemas, and styling patterns. This ensures a consistent UI/UX with a faster development cycle.
* **Interaction Model:** * **Action-Oriented UI:** Large, high-contrast buttons for drivers who may be in low-light or outdoor environments.
    * **Offline-First:** Essential for logistics. Using `AsyncStorage` or `SQLite` to queue POD uploads when the driver is in a "dead zone," auto-syncing once a 4G/5G connection is restored.

---

## 3. CI/CD and Deployment (Part 3)
The deployment pipeline is automated via GitHub Actions, targeting an Ubuntu environment running Nginx and Gunicorn.

* **Staging:** Triggers on pushes to the `staging` branch.
* **Production:** Triggers on pushes to the `main` branch.

### Future Improvements
* **Dockerization:** Currently, the environment is managed manually on the EC2. Moving to Docker would eliminate "dependency drift" between Staging and Production.
* **Terraform:** Implementing IaC would allow us to replicate the RDS and ElastiCache setup across different AWS regions for better availability.

> **Note:** See `.github/workflows/` for the implementation details.

---

## 4. Debugging: The Monday Morning Outage (Part 4)
The POD upload failure involves multiple hops. My order of operations for root cause analysis:

1.  **Step 1: Check Nginx/Django Logs (`EC2`)**
    * *Command:* `tail -f /var/log/nginx/error.log` and `journalctl -u gunicorn`.
    * *Goal:* Check for `413 Request Entity Too Large` (Nginx block) or `500 Internal Server Error` (Django code crash).
2.  **Step 2: Inspect the Task Queue (`Celery Flower`)**
    * *Tool:* Flower Dashboard.
    * *Goal:* Check if tasks are stuck in `PENDING` (Worker down) or `FAILURE`. If failed, check the traceback to see if the Bedrock API call timed out.
3.  **Step 3: Verify S3 Permissions & Storage**
    * *Tool:* AWS S3 Console / CloudWatch.
    * *Goal:* Ensure the IAM role for the EC2 hasn't expired or changed, preventing the initial image save.
4.  **Step 4: Database Health (`RDS Console`)**
    * *Tool:* AWS RDS Performance Insights.
    * *Goal:* Ensure the DB isn't in a "Storage Full" state, which would prevent Celery from writing the final validation result.

---

## 5. Setup & Usage
1.  **Workflows:** Located in `.github/workflows/`.
2.  **Secrets:** The following secrets must be configured in GitHub for the actions to run:
    * `SSH_PRIVATE_KEY`
    * `EC2_HOST`
    * `PROD_EC2_IP`
