#!/bin/bash

# Aizsz Service - Docker Run Script
# This script helps you run the Aizsz Service container easily

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env file exists
if [ ! -f .env ]; then
    print_error ".env file not found!"
    print_status "Please create .env file from .env.example template"
    print_status "Run: cp .env.example .env"
    print_status "Then edit .env with your actual values"
    exit 1
fi

# Check if required environment variables are set
source .env

if [ -z "$API_ID" ] || [ -z "$API_HASH" ] || [ -z "$SESSION" ]; then
    print_error "Required environment variables not set!"
    print_status "Please set API_ID, API_HASH, and SESSION in .env file"
    exit 1
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p logs plugins_cache

# Build the Docker image
print_status "Building Docker image..."
docker build -t aizsz-service .

if [ $? -eq 0 ]; then
    print_success "Docker image built successfully!"
else
    print_error "Failed to build Docker image!"
    exit 1
fi

# Stop existing container if running
if [ "$(docker ps -q -f name=aizsz-service)" ]; then
    print_warning "Stopping existing container..."
    docker stop aizsz-service
fi

# Remove existing container if exists
if [ "$(docker ps -aq -f name=aizsz-service)" ]; then
    print_warning "Removing existing container..."
    docker rm aizsz-service
fi

# Run the container
print_status "Starting Aizsz Service container..."
docker run -d \
    --name aizsz-service \
    --restart unless-stopped \
    --env-file .env \
    -v "$(pwd)/logs:/app/logs" \
    -v "$(pwd)/plugins_cache:/app/plugins_cache" \
    -v "$(pwd)/asst.session:/app/asst.session:ro" \
    aizsz-service

if [ $? -eq 0 ]; then
    print_success "Aizsz Service started successfully!"
    print_status "Container name: aizsz-service"
    print_status "To view logs: docker logs -f aizsz-service"
    print_status "To stop: docker stop aizsz-service"
    print_status "To restart: docker restart aizsz-service"
else
    print_error "Failed to start container!"
    exit 1
fi

# Show container status
print_status "Container status:"
docker ps -f name=aizsz-service
