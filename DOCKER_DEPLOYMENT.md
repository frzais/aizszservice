# Aizsz Service - Docker Deployment Guide

## Overview

This guide will help you deploy Aizsz Service (Telegram UserBot) using Docker.

## Prerequisites

- Docker installed on your system
- Telegram API credentials (API_ID, API_HASH)
- Session string for your Telegram account
- Database (Redis, MongoDB, or PostgreSQL)

## Quick Start

### 1. Environment Setup

Create a `.env` file with your configuration:

```bash
# Required
API_ID=your_api_id
API_HASH=your_api_hash
SESSION=your_session_string

# Database (choose one)
REDIS_URI=redis://localhost:6379
REDIS_PASSWORD=your_password

# OR
MONGO_URI=mongodb://localhost:27017/aizsz

# OR
DATABASE_URL=postgresql://user:pass@localhost:5432/aizsz
```

### 2. Generate Session String

Run the session generator:

```bash
python3 generate_session.py
```

### 3. Deploy with Docker

#### Option A: Using Docker Compose (Recommended)

```bash
docker-compose up -d
```

#### Option B: Using Docker Run Script

**Linux/Mac:**

```bash
./docker-run.sh
```

**Windows:**

```cmd
docker-run.bat
```

#### Option C: Manual Docker Commands

```bash
# Build image
docker build -t aizsz-service .

# Run container
docker run -d \
    --name aizsz-service \
    --restart unless-stopped \
    --env-file .env \
    -v "$(pwd)/logs:/app/logs" \
    -v "$(pwd)/plugins_cache:/app/plugins_cache" \
    aizsz-service
```

## Container Management

### View Logs

```bash
docker logs -f aizsz-service
```

### Stop Container

```bash
docker stop aizsz-service
```

### Restart Container

```bash
docker restart aizsz-service
```

### Update Container

```bash
docker-compose down
docker-compose pull
docker-compose up -d
```

## Multi-Client Support

To run multiple Telegram accounts, add additional session strings to your `.env`:

```bash
SESSION1=additional_session_1
SESSION2=additional_session_2
SESSION3=additional_session_3
SESSION4=additional_session_4
SESSION5=additional_session_5
```

## Volumes

The container uses the following volumes:

- `./logs:/app/logs` - Application logs
- `./plugins_cache:/app/plugins_cache` - Plugin cache
- `./asst.session:/app/asst.session:ro` - Session file (read-only)

## Environment Variables

### Required

- `API_ID` - Telegram API ID
- `API_HASH` - Telegram API Hash
- `SESSION` - Telegram session string

### Database (Choose One)

- `REDIS_URI` - Redis connection string
- `REDIS_PASSWORD` - Redis password
- `MONGO_URI` - MongoDB connection string
- `DATABASE_URL` - PostgreSQL connection string

### Optional

- `BOT_TOKEN` - Bot token for bot features
- `LOG_CHANNEL` - Channel ID for logs
- `HEROKU_API` - Heroku API key
- `HEROKU_APP_NAME` - Heroku app name
- `TZ` - Timezone (default: Asia/Jakarta)

## Troubleshooting

### Container Won't Start

1. Check if all required environment variables are set
2. Verify session string is valid
3. Check Docker logs: `docker logs aizsz-service`

### Database Connection Issues

1. Ensure database is running and accessible
2. Check connection strings in `.env`
3. Verify database credentials

### Permission Issues

1. Ensure Docker has permission to access volumes
2. Check file permissions on mounted directories

## Security Notes

- Never commit `.env` file to version control
- Keep session strings secure
- Use strong database passwords
- Regularly update dependencies

## Support

For issues and support, please check:

- [Ultroid Documentation](http://ultroid.tech/)
- [TeamUltroid Telegram](https://t.me/TeamUltroid)
