import time
import sys
import os

def run_worker():
    print(" Kairos Background Worker Started...")
    print("   [INFO] Listening for materialization jobs in Redis Queue...")
    
    while True:
        # Simulation of a job processor
        # In production, this would pop from a Redis list or Kafka topic
        time.sleep(60)
        # print("   [HEARTBEAT] Worker is alive.")

if __name__ == "__main__":
    try:
        run_worker()
    except KeyboardInterrupt:
        print("  Worker Stopping...")