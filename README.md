
# Leaderboard API - AWS Infrastructure Automation

A FastAPI-based leaderboard application with PostgreSQL (RDS) and Amazon MemoryDB for Redis, designed for automated deployment to AWS Elastic Beanstalk via GitHub Actions.

## 📁 Project Structure
```
leaderboard-app/
├── app/                       # FastAPI application source code
│   ├── main.py                # Entry point
│   ├── database.py            # PostgreSQL connection
│   ├── redis_client.py        # MemoryDB (Redis) connection
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   ├── crud.py                # CRUD operations (optional)
│   └── routes/
│       ├── leaderboard.py     # Leaderboard endpoints
│       └── session.py         # Session management
├── .ebextensions/             # Elastic Beanstalk configs
│   ├── 01_install_redis.config
│   └── 02_env_vars.config
├── .platform/                 # Platform hooks for nginx
│   └── nginx/
│       └── conf.d/
│           └── custom.conf
├── .github/workflows/         # GitHub Actions CI/CD
│   └── deploy.yml
├── docker-compose.yml         # Local development with Docker
├── Makefile                   # Make commands for local development
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

```
## 🚀 Local Development (Docker)

### Prerequisites
- Docker & Docker Compose
- Make (optional, but recommended)

### Run the application

```bash
# Start all services
make serve

# Or manually
docker compose up --build
```

### Test the API

```bash
# Health check
curl http://localhost:8000/health

# Submit a score
curl -X POST "http://localhost:8000/api/leaderboard/score?user_id=1&score=100.5&game_mode=classic"

# Get top 10 leaderboard
curl http://localhost:8000/api/leaderboard/top/10

# Create a session
curl http://localhost:8000/api/session/create
```

### Stop the application

```bash
make down
# or
docker compose down
```

### Clean everything (remove volumes)

```bash
make clean
```

## 🧪 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/` | Root welcome message |
| GET | `/api/leaderboard/top/{limit}` | Get top N scores (cached via Redis) |
| POST | `/api/leaderboard/score` | Submit a new score (invalidates cache) |
| GET | `/api/session/create` | Create a new session (stored in Redis) |

## ☁️ Deployment to AWS (Elastic Beanstalk)

### Prerequisites

- AWS account with IAM user having required permissions
- GitHub repository with secrets configured

### GitHub Secrets

| Secret | Description |
|--------|-------------|
| `AWS_ACCESS_KEY_ID` | IAM user access key |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key |

### Deploy via GitHub Actions

1. Push to `main` branch:
   ```bash
   git add .
   git commit -m "Deploy to AWS"
   git push origin main
   ```

2. GitHub Actions will:
   - Build the deployment package
   - Upload to S3
   - Create a new application version in Elastic Beanstalk
   - Update the environment with zero downtime

3. After deployment, test your live API:
   ```bash
   curl http://lks-leaderboard-env.xxxxxx.us-east-1.elasticbeanstalk.com/health
   ```

## 🛠 AWS Resources Used

| Service | Purpose |
|---------|---------|
| Elastic Beanstalk | Application hosting with Auto Scaling |
| Amazon RDS (PostgreSQL) | Primary database |
| Amazon MemoryDB for Redis | Caching & session storage |
| VPC + Subnets + IGW + NAT | Networking & private access |
| Security Groups | Firewall & access control |
| CloudWatch | Monitoring & logging |
| Systems Manager (SSM) | Remote instance management |
| IAM | Least privilege access |
| S3 | Deployment artifact storage |
| GitHub Actions | CI/CD automation |

## 📊 Monitoring & Troubleshooting

- **CloudWatch Dashboard**: View CPU, request count, Redis cache hits, etc.
- **Systems Manager Session Manager**: Connect to EC2 instances without SSH
- **Beanstalk Logs**: `/var/log/eb-activity.log` and `/var/log/nginx/error.log`

## 🧪 Simulate Failures

| Scenario | Action | Recovery |
|----------|--------|----------|
| App crash | `pkill -f uvicorn` via SSM | Auto Scaling replaces instance |
| Redis failure | Stop MemoryDB cluster | App falls back to DB |
| RDS failure | Stop RDS instance | Restore from backup |

## 📝 License

This project is created for LKS Cloud Computing 2026 training purposes.

---

**Happy coding! 🚀**
