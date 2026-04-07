# Monday Morning Outage: Debugging Steps

### 1. Nginx Check (The Entry Point)
`ssh ubuntu@ec2-ip "sudo tail -n 50 /var/log/nginx/error.log"`
* **Checking for:** `413 Request Entity Too Large`. If POD photos are high-res, Nginx might block them before reaching Django.

### 2. Django Logs (The Application)
`tail -f /home/ubuntu/symflow/logs/django.log`
* **Checking for:** `S3 Upload Error` or `AWS SignatureDoesNotMatch`. Verifies if the EC2 has the correct IAM role to write to S3.

### 3. Celery Flower (The Task Queue)
* **Action:** Access the Flower Dashboard at port 5555.
* **Checking for:** Tasks stuck in `PENDING`. If workers are down, the image is saved to S3 but the AI validation never triggers.

### 4. Bedrock / RDS Check
* **Action:** Check CloudWatch logs for the Bedrock Model Endpoint.
* **Checking for:** Throttling exceptions. If the AI validation fails, the task won't write the final status to RDS.
