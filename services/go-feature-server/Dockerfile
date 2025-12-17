FROM golang:1.23-bookworm as builder

# 1. Install Protoc
RUN apt-get update && apt-get install -y protobuf-compiler

# 2. Install Go Plugins (PINNED VERSIONS)
RUN go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.34.2
RUN go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.4.0

WORKDIR /app

# 3. Copy source code
COPY api/ ./api/
COPY services/go-feature-server/ ./services/go-feature-server/

# 4. Generate Protobufs
RUN protoc --go_out=. --go-grpc_out=. api/proto/v1/kairos.proto

# 5. Move generated files
RUN cp -r github.com/kairos-platform/services/go-feature-server/pb services/go-feature-server/

# 6. Build the Binary
WORKDIR /app/services/go-feature-server

# --- FIX IS HERE: Force specific versions compatible with Go 1.23 ---
RUN go get google.golang.org/grpc@v1.64.0
RUN go get google.golang.org/protobuf@v1.34.2
# ------------------------------------------------------------------

RUN go mod tidy
RUN go build -o server cmd/main.go

# --- Final Stage ---
FROM debian:bookworm-slim
WORKDIR /app
COPY --from=builder /app/services/go-feature-server/server .

# Expose gRPC port
EXPOSE 50051
CMD ["./server"]