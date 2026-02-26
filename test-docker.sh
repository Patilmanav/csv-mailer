#!/bin/bash

echo "🧪 Testing CSV Mailer Docker Deployment"
echo "========================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env with your SMTP credentials before running the app"
fi

# Build the image
echo ""
echo "🔨 Building Docker image..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo "✅ Build successful"

# Start the container
echo ""
echo "🚀 Starting container..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ Failed to start container"
    exit 1
fi

echo "✅ Container started"

# Wait for app to be ready
echo ""
echo "⏳ Waiting for app to be ready..."
sleep 5

# Test health endpoint
echo ""
echo "🏥 Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:8000/health)

if [ $? -eq 0 ]; then
    echo "✅ Health check passed: $HEALTH_RESPONSE"
else
    echo "❌ Health check failed"
    echo "📋 Container logs:"
    docker-compose logs --tail=50
    exit 1
fi

# Test main page
echo ""
echo "🌐 Testing main page..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Main page accessible (HTTP $HTTP_CODE)"
else
    echo "❌ Main page returned HTTP $HTTP_CODE"
    docker-compose logs --tail=50
    exit 1
fi

echo ""
echo "========================================" 
echo "✅ All tests passed!"
echo ""
echo "📱 Access the app at: http://localhost:8000"
echo "📚 API docs at: http://localhost:8000/api/docs"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
