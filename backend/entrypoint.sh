#!/bin/bash
set -e

# Color output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Demucs API...${NC}"

# Check if packages are already installed
if [ ! -f "/app/.packages_installed" ]; then
    echo -e "${YELLOW}📦 First run detected - installing dependencies...${NC}"
    echo -e "${YELLOW}   This will take 2-3 minutes but only happens once.${NC}"
    
    # Install packages with pip cache
    pip install --cache-dir=/app/pip-cache -r /app/requirements.txt
    
    # Mark as installed
    touch /app/.packages_installed
    
    echo -e "${GREEN}✅ Dependencies installed successfully!${NC}"
else
    echo -e "${GREEN}✅ Using cached dependencies${NC}"
fi

# Start the application
echo -e "${GREEN}🎵 Starting API server on port 80...${NC}"
exec uvicorn main:app --host 0.0.0.0 --port 80
