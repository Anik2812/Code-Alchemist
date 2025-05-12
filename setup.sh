
#
# Setup script for Code Alchemist CLI
# This script installs Code Alchemist and its dependencies
#

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "   ______          __        ___    __      __                _     __ "
echo "  / ____/___  ____/ /__     /   |  / /_____/ /_  ___  ____ _(_)___/ /_"
echo " / /   / __ \/ __  / _ \   / /| | / / ___/ __ \/ _ \/ __ \`/ / __  __/"
echo "/ /___/ /_/ / /_/ /  __/  / ___ |/ / /__/ / / /  __/ /_/ / / /_/ /_  "
echo "\____/\____/\__,_/\___/  /_/  |_/_/\___/_/ /_/\___/\__, /_/\__/\__/  "
echo "                                                  /____/             "
echo -e "${NC}"

echo -e "${CYAN}Setup Script for Code Alchemist CLI${NC}"
echo "==============================================="

# Check if script is run with root/sudo
if [ "$EUID" -eq 0 ]; then
  echo -e "${YELLOW}Warning: This script doesn't need to be run as root.${NC}"
  echo -e "${YELLOW}Running as root might cause permission issues for the current user.${NC}"
  read -p "Continue anyway? (y/n) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}Setup aborted.${NC}"
    exit 1
  fi
fi

# Check if Python is installed
echo -e "\n${CYAN}Checking dependencies...${NC}"
if ! command -v python3 &> /dev/null; then
  echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
  echo "Please install Python 3 and try again."
  exit 1
else
  python_version=$(python3 --version | awk '{print $2}')
  echo -e "${GREEN}✓ Found Python $python_version${NC}"
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
  echo -e "${RED}Error: pip3 is required but not installed.${NC}"
  echo "Please install pip3 and try again."
  exit 1
else
  pip_version=$(pip3 --version | awk '{print $2}')
  echo -e "${GREEN}✓ Found pip $pip_version${NC}"
fi

# Check if Amazon Q Developer CLI is installed
if ! command -v q &> /dev/null; then
  echo -e "${YELLOW}Warning: Amazon Q Developer CLI not found.${NC}"
  echo -e "Code Alchemist depends on Amazon Q Developer CLI."
  
  read -p "Would you like to install Amazon Q Developer CLI now? (y/n) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "\n${CYAN}Installing Amazon Q Developer CLI...${NC}"
    
    # Platform specific installation
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
      # Linux installation
      echo -e "${YELLOW}Please visit the following URL to install Amazon Q Developer CLI:${NC}"
      echo -e "https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/setup-qdeveloper.html"
      echo -e "${YELLOW}After installation, run this setup script again.${NC}"
      exit 0
    elif [[ "$OSTYPE" == "darwin"* ]]; then
      # macOS installation
      echo -e "${YELLOW}Please visit the following URL to install Amazon Q Developer CLI:${NC}"
      echo -e "https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/setup-qdeveloper.html"
      echo -e "${YELLOW}After installation, run this setup script again.${NC}"
      exit 0
    else
      echo -e "${RED}Unsupported operating system.${NC}"
      echo -e "${YELLOW}Please install Amazon Q Developer CLI manually:${NC}"
      echo -e "https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/setup-qdeveloper.html"
      exit 1
    fi
  else
    echo -e "${YELLOW}Skipping Amazon Q Developer CLI installation.${NC}"
    echo -e "${YELLOW}Note: Code Alchemist will not work properly without it.${NC}"
  fi
else
  q_version=$(q --version 2>&1 || echo "Unknown")
  echo -e "${GREEN}✓ Found Amazon Q Developer CLI: $q_version${NC}"
fi

# Give execute permission to the Code Alchemist Python script
echo -e "\n${CYAN}Setting up Code Alchemist...${NC}"
chmod +x ./code_alchemist.py
echo -e "${GREEN}✓ Gave execute permissions to code_alchemist.py${NC}"

# Create a symbolic link in /usr/local/bin if it doesn't exist
if [ -z "$NO_SYMLINK" ]; then
  echo -e "\n${CYAN}Would you like to create a symbolic link to make code-alchemist globally accessible?${NC}"
  echo -e "${YELLOW}This will require sudo access.${NC}"
  read -p "Create symbolic link? (y/n) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    SCRIPT_PATH=$(realpath ./code_alchemist.py)
    sudo ln -sf "$SCRIPT_PATH" /usr/local/bin/code-alchemist
    if [ $? -eq 0 ]; then
      echo -e "${GREEN}✓ Created symbolic link at /usr/local/bin/code-alchemist${NC}"
      echo -e "${GREEN}✓ You can now run 'code-alchemist' from anywhere${NC}"
    else
      echo -e "${RED}Failed to create symbolic link. Please check your permissions.${NC}"
    fi
  else
    echo -e "${YELLOW}Skipping symbolic link creation.${NC}"
  fi
fi

# Check if the user has an AWS Builder ID
echo -e "\n${CYAN}Checking AWS Builder ID authentication...${NC}"
q auth status &> /dev/null
if [ $? -ne 0 ]; then
  echo -e "${YELLOW}You need to authenticate with your AWS Builder ID to use Amazon Q Developer CLI.${NC}"
  read -p "Would you like to authenticate now? (y/n) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    q auth login
    if [ $? -eq 0 ]; then
      echo -e "${GREEN}✓ Authentication successful${NC}"
    else
      echo -e "${RED}Authentication failed. Please try again later.${NC}"
      echo -e "${YELLOW}You can authenticate manually by running 'q auth login'${NC}"
    fi
  else
    echo -e "${YELLOW}Skipping authentication.${NC}"
    echo -e "${YELLOW}Remember to run 'q auth login' before using Code Alchemist.${NC}"
  fi
else
  echo -e "${GREEN}✓ Already authenticated with AWS Builder ID${NC}"
fi

# Create demo files directory if it doesn't exist
if [ ! -d "sample_code" ]; then
  echo -e "\n${CYAN}Creating sample code directory...${NC}"
  mkdir -p sample_code
  echo -e "${GREEN}✓ Created sample_code directory${NC}"
fi

# Setup complete
echo -e "\n${GREEN}=========================================${NC}"
echo -e "${GREEN}Code Alchemist setup completed successfully!${NC}"
echo -e "${GREEN}=========================================${NC}"

echo -e "\n${CYAN}Next steps:${NC}"
echo -e "  1. Try running the demo: ${YELLOW}./demo.sh${NC}"
echo -e "  2. Run Code Alchemist: ${YELLOW}./code_alchemist.py${NC}"
echo -e "  3. Read the documentation: ${YELLOW}README.md${NC}"

echo -e "\n${BLUE}Happy coding!${NC}"