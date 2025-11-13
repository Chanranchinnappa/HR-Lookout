#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BASE_URL="http://localhost:8000/api/v1"

echo -e "${BLUE}=== HR-Lookout RBAC Test Script ===${NC}\n"

# Test 1: Health Check
echo -e "${BLUE}Test 1: Health Check${NC}"
curl -s ${BASE_URL}/health/ | python3 -m json.tool
echo -e "\n"

# Test 2: Login and get token
echo -e "${BLUE}Test 2: Login${NC}"
read -p "Enter username: " USERNAME
read -sp "Enter password: " PASSWORD
echo ""

LOGIN_RESPONSE=$(curl -s -X POST ${BASE_URL}/auth/login/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}")

TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('token', ''))")

if [ -z "$TOKEN" ]; then
    echo -e "${RED}Login failed. Response: $LOGIN_RESPONSE${NC}"
    exit 1
fi

echo -e "${GREEN}Login successful! Token: ${TOKEN:0:20}...${NC}\n"

# Test 3: Get current user profile
echo -e "${BLUE}Test 3: Get User Profile${NC}"
curl -s ${BASE_URL}/auth/me/ \
  -H "Authorization: Token $TOKEN" | python3 -m json.tool
echo -e "\n"

# Test 4: Get detailed profile with roles
echo -e "${BLUE}Test 4: Get Profile with Roles & Permissions${NC}"
curl -s ${BASE_URL}/auth/profile/ \
  -H "Authorization: Token $TOKEN" | python3 -m json.tool
echo -e "\n"

echo -e "${GREEN}=== All tests completed ===${NC}"
