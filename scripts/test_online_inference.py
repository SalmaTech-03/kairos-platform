import grpc
import time
import sys
import os

# Add root to path so imports work
sys.path.append(os.getcwd())

from sdk.kairos_sdk.core import kairos_pb2, kairos_pb2_grpc

def test_inference():
    print(" Connecting to Kairos Feature Server (localhost:50051)...")
    
    # 1. Connect via gRPC
    # Note: If this fails, make sure 'manage.ps1 up' is running!
    channel = grpc.insecure_channel('localhost:50051')
    stub = kairos_pb2_grpc.FeatureStoreServiceStub(channel)

    # 2. Prepare Request
    # We want features for user_1001 (who has data in Redis)
    request = kairos_pb2.GetOnlineFeaturesRequest(
        feature_view_name="transaction_stats",
        entity_id="user_1001",
        feature_names=["amount", "is_fraud", "timestamp"]
    )

    # 3. Measure Latency
    print("   ⚡ Sending Request...")
    start_time = time.time()
    
    try:
        response = stub.GetOnlineFeatures(request)
        end_time = time.time()
        
        latency_ms = (end_time - start_time) * 1000

        print(f"\nRESPONSE RECEIVED in {latency_ms:.2f}ms!")
        print("    Feature Vector:")
        for k, v in response.values.items():
            print(f"      - {k}: {v}")
            
    except grpc.RpcError as e:
        print(f" RPC Failed: {e.code()} - {e.details()}")

if __name__ == "__main__":
    test_inference()