package main

import (
"context"
"fmt"
"log"
"net"
"os"

"github.com/redis/go-redis/v9"
"google.golang.org/grpc"
"google.golang.org/grpc/reflection"
pb "github.com/kairos-platform/services/go-feature-server/pb"
)

type server struct {
pb.UnimplementedFeatureStoreServiceServer
rdb *redis.Client
}

func (s *server) GetOnlineFeatures(ctx context.Context, req *pb.GetOnlineFeaturesRequest) (*pb.GetOnlineFeaturesResponse, error) {
key := fmt.Sprintf("%s:%s", req.FeatureViewName, req.EntityId)
val, err := s.rdb.HGetAll(ctx, key).Result()
if err != nil {
log.Printf(" Redis Error: %v", err)
return nil, err
}
responseMap := make(map[string]string)
for _, fName := range req.FeatureNames {
if v, ok := val[fName]; ok {
responseMap[fName] = v
}
}
return &pb.GetOnlineFeaturesResponse{Values: responseMap}, nil
}

func main() {
redisAddr := os.Getenv("REDIS_ADDR")
if redisAddr == "" {
redisAddr = "kairos-cache:6379"
}
rdb := redis.NewClient(&redis.Options{Addr: redisAddr})
lis, err := net.Listen("tcp", ":50051")
if err != nil {
log.Fatalf("failed to listen: %v", err)
}
s := grpc.NewServer()
pb.RegisterFeatureStoreServiceServer(s, &server{rdb: rdb})
reflection.Register(s)
fmt.Printf(" Kairos Go Server listening on :50051 (Redis: %s)\n", redisAddr)
if err := s.Serve(lis); err != nil {
log.Fatalf("failed to serve: %v", err)
}
}
