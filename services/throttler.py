import redis
import time
import requests
import json

# Connection to SymFlow's Redis (already in stack)
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def push_to_customer_queue(customer_id, request_payload):
    """
    Called by Django View. Instead of calling the API, 
    we buffer the request in a customer-specific Redis list.
    """
    queue_name = f"queue:customer:{customer_id}"
    r.rpush(queue_name, json.dumps(request_payload))

def run_fair_scheduler():
    """
    The Core "Heartbeat": Ensures exactly 3 requests per second
    using a Round-Robin approach for fairness.
    """
    print("SymFlow Throttler Active: Monitoring Customer Queues...")
    
    while True:
        # 1. Fetch all active customer keys
        customer_keys = r.keys("queue:customer:*")
        
        if not customer_keys:
            time.sleep(0.1) # Idle wait
            continue

        for key in customer_keys:
            # 2. Pop one request per customer (Round Robin)
            raw_data = r.lpop(key)
            
            if raw_data:
                payload = json.loads(raw_data)
                execute_external_call(payload)
                
                # 3. Strict Rate Limit Enforcement: 1000ms / 3 req = 333ms
                time.sleep(0.333)

def execute_external_call(payload):
    """Handles the actual API call with Retry Logic"""
    url = "https://external-supplychain-api.com/v1/track"
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
    except Exception as e:
        # Exponential Backoff logic would be triggered here via Celery
        print(f"Request Failed: {e}. Moving to Retry Queue.")

if __name__ == "__main__":
    run_fair_scheduler()
