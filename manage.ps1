param (
    [Parameter(Mandatory=$true)]
    [string]$Command
)

switch ($Command) {
    "up" {
        Write-Host "🚀 Starting Kairos Platform..." -ForegroundColor Green
        docker-compose -f deploy/docker-compose.yaml up -d
    }
    "down" {
        Write-Host "🛑 Stopping Services..." -ForegroundColor Red
        docker-compose -f deploy/docker-compose.yaml down
    }
    "seed" {
        Write-Host "🌱 Seeding Database..." -ForegroundColor Yellow
        python scripts/seed_fake_data.py
    }
    "logs" {
        docker-compose -f deploy/docker-compose.yaml logs -f
    }
    Default {
        Write-Host "❌ Unknown command. Use: up, down, seed, logs" -ForegroundColor Red
    }
}