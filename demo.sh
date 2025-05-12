#!/bin/bash
#
# Demo script for Code Alchemist CLI
# This script demonstrates the various capabilities of Code Alchemist
#

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    exit 1
fi

# Function to display section headers
section() {
    echo -e "\n${BLUE}======================================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${BLUE}======================================================${NC}"
    sleep 1
}

# Function to run a command with colored output
run_cmd() {
    echo -e "${YELLOW}>> $1${NC}"
    sleep 0.5
    eval "$1"
    echo ""
    sleep 1
}

# Function to create a sample messy code file for demonstration
create_sample_code() {
    local dir="$1"
    mkdir -p "$dir"
    
    # Create a messy Python file
    cat > "$dir/messy_app.py" << 'EOF'
# This is an intentionally messy Python script for demonstration purposes
import sys, os, json, random
from datetime import datetime, timedelta

# Global variables
counter=0
DEBUG=True

# Some utility functions
def add_numbers(a,b):
    return a+b

def subtract_numbers(a,b):
    return a-b

def multiply_numbers(a,b):
    return a*b

def divide_numbers(a,b):
    if b==0:
        print("Error: Division by zero!")
        return None
    return a/b

# A class with poor structure
class DataProcessor:
    def __init__(self, data):
        self.data = data
        self.processed = False
        self.result = None
        
    def process(self):
        # Process the data somehow
        if isinstance(self.data, list):
            total = 0
            for item in self.data:
                if isinstance(item, (int, float)):
                    total += item
                elif isinstance(item, str):
                    try:
                        total += float(item)
                    except:
                        pass
            self.result = total
        elif isinstance(self.data, dict):
            values = []
            for key, value in self.data.items():
                if isinstance(value, (int, float)):
                    values.append(value)
                elif isinstance(value, str):
                    try:
                        values.append(float(value))
                    except:
                        pass
            if values:
                self.result = sum(values)
            else:
                self.result = 0
        else:
            self.result = 0
        
        self.processed = True
        return self.result
    
    # Duplicate functionality with slight variations
    def process_list(self, data_list):
        total = 0
        for item in data_list:
            if isinstance(item, (int, float)):
                total += item
            elif isinstance(item, str):
                try:
                    total += float(item)
                except:
                    pass
        return total
    
    def process_dict(self, data_dict):
        values = []
        for key, value in data_dict.items():
            if isinstance(value, (int, float)):
                values.append(value)
            elif isinstance(value, str):
                try:
                    values.append(float(value))
                except:
                    pass
        if values:
            return sum(values)
        else:
            return 0
            
# Security issue: Insecure password handling
def check_login(username, password):
    # Hard-coded credentials (security issue)
    if username == "admin" and password == "password123":
        return True
    else:
        return False

# Performance issue: Inefficient algorithm
def find_duplicates(data):
    duplicates = []
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            if data[i] == data[j] and data[i] not in duplicates:
                duplicates.append(data[i])
    return duplicates

# Function that does multiple things instead of single responsibility
def process_and_save_data(data, filename, format_type):
    # Process the data
    processor = DataProcessor(data)
    result = processor.process()
    
    # Format the data
    if format_type == "json":
        formatted_data = json.dumps({"result": result, "timestamp": str(datetime.now())})
    elif format_type == "text":
        formatted_data = f"Result: {result}\nTimestamp: {datetime.now()}"
    else:
        formatted_data = str(result)
    
    # Save the data
    with open(filename, "w") as f:
        f.write(formatted_data)
    
    # Print status
    print(f"Data processed and saved to {filename}")
    
    # Return something
    return result

# Main function with some issues
def main():
    print("Welcome to the messy data processor!")
    
    # Example data
    data1 = [1, 2, "3", 4, "5"]
    data2 = {"a": 1, "b": 2, "c": "3"}
    
    # Process data1
    print("Processing data1...")
    processor1 = DataProcessor(data1)
    result1 = processor1.process()
    print(f"Result 1: {result1}")
    
    # Process data2 differently for no good reason
    print("Processing data2...")
    result2 = process_and_save_data(data2, "output.txt", "text")
    print(f"Result 2: {result2}")
    
    # Find duplicates inefficiently
    big_data = [random.randint(1, 10) for _ in range(20)]
    print(f"Big data: {big_data}")
    duplicates = find_duplicates(big_data)
    print(f"Duplicates: {duplicates}")
    
    # Security issue
    if check_login("admin", "password123"):
        print("Login successful!")
    else:
        print("Login failed!")

if __name__ == "__main__":
    main()
EOF

    # Create a README with minimal information
    cat > "$dir/README.md" << 'EOF'
# Sample Project

This is a sample project for demonstrating Code Alchemist.
EOF

    echo -e "${GREEN}Created sample code in $dir${NC}"
}

# Function to clean up demo files
cleanup() {
    echo -e "${YELLOW}Cleaning up demo files...${NC}"
    rm -rf sample_code alchemist_output new_project analysis.md refactoring.md security_optimizations.md dashboard.md docs
    echo -e "${GREEN}Cleanup complete!${NC}"
}

# Main demo script
clear
echo -e "${BLUE}"
echo "   ______          __        ___    __      __                _     __ "
echo "  / ____/___  ____/ /__     /   |  / /_____/ /_  ___  ____ _(_)___/ /_"
echo " / /   / __ \/ __  / _ \   / /| | / / ___/ __ \/ _ \/ __ \`/ / __  __/"
echo "/ /___/ /_/ / /_/ /  __/  / ___ |/ / /__/ / / /  __/ /_/ / / /_/ /_  "
echo "\____/\____/\__,_/\___/  /_/  |_/_/\___/_/ /_/\___/\__, /_/\__/\__/  "
echo "                                                  /____/             "
echo -e "${NC}"

echo -e "${CYAN}Demo Script for Code Alchemist CLI${NC}"
echo "==============================================="

# Trap cleanup on exit
trap cleanup EXIT

# Ensure we have permission to run the script
chmod +x ./code_alchemist.py

# Create sample code
section "Creating sample messy code for demonstration"
create_sample_code "sample_code"

# Show basic help
section "Showing basic help information"
run_cmd "./code_alchemist.py"

# Setup a new project
section "Setting up a new project structure"
# Create the new_project directory first
mkdir -p new_project
run_cmd "./code_alchemist.py setup new_project --type python --name 'My Awesome Project'"
echo -e "${GREEN}Created project structure in new_project/${NC}"
# Only try to list if directory exists
if [ -d "new_project" ]; then
    ls -la new_project
else
    echo -e "${RED}Directory new_project was not created${NC}"
fi

# Create docs directory for the document command output
mkdir -p docs

# Analyze code
section "Analyzing code quality"
run_cmd "./code_alchemist.py analyze sample_code/messy_app.py --format markdown --output analysis.md"
echo -e "${GREEN}Analysis results saved to analysis.md${NC}"

# Document code
section "Generating documentation"
run_cmd "./code_alchemist.py document sample_code/messy_app.py"
echo -e "${GREEN}Documentation generated in docs/${NC}"
# Only try to list if directory exists
if [ -d "docs" ]; then
    ls -la docs
else
    echo -e "${RED}Directory docs was not created${NC}"
fi

# Refactor suggestions
section "Suggesting code refactoring"
run_cmd "./code_alchemist.py refactor sample_code/messy_app.py --output refactoring.md"
echo -e "${GREEN}Refactoring suggestions saved to refactoring.md${NC}"

# Optimization suggestions
section "Suggesting optimizations"
run_cmd "./code_alchemist.py optimize sample_code/messy_app.py --security --output security_optimizations.md"
echo -e "${GREEN}Security optimization suggestions saved to security_optimizations.md${NC}"

# Generate project dashboard
section "Generating project dashboard"
run_cmd "./code_alchemist.py dashboard sample_code --output dashboard.md"
echo -e "${GREEN}Project dashboard saved to dashboard.md${NC}"

# Create alchemist_output directory for transmute command
mkdir -p alchemist_output

# Full transmutation
section "Performing full transmutation (all features at once)"
run_cmd "./code_alchemist.py transmute sample_code"
echo -e "${GREEN}Full transmutation completed. Results in alchemist_output/${NC}"
# Only try to list if directory exists
if [ -d "alchemist_output" ]; then
    ls -la alchemist_output
else
    echo -e "${RED}Directory alchemist_output was not created${NC}"
fi

# Show some example output - only if files exist
section "Showing excerpt from generated dashboard"
if [ -f "alchemist_output/PROJECT_DASHBOARD.md" ]; then
    run_cmd "head -n 20 alchemist_output/PROJECT_DASHBOARD.md"
else
    echo -e "${RED}Dashboard file not found${NC}"
fi

section "Showing excerpt from refactoring suggestions"
if [ -f "alchemist_output/refactoring.md" ]; then
    run_cmd "head -n 20 alchemist_output/refactoring.md"
else
    echo -e "${RED}Refactoring file not found${NC}"
fi

# Conclusion
section "Demo completed!"
echo -e "${GREEN}You've now seen the core features of Code Alchemist CLI.${NC}"
echo -e "${YELLOW}To explore more options and details, try: ${NC}"
echo -e "  ./code_alchemist.py [command] --help"
echo ""
echo -e "${CYAN}Happy coding!${NC}"