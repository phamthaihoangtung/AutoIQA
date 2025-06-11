#!/bin/bash

# Image Quality Assessment System - Setup Script
# ==============================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}🔧 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo -e "${BLUE}"
    echo "============================================================"
    echo " $1"
    echo "============================================================"
    echo -e "${NC}"
}

# Check if conda is installed
check_conda() {
    if command -v conda &> /dev/null; then
        print_success "Conda found: $(conda --version)"
        return 0
    else
        print_error "Conda not found"
        return 1
    fi
}

# Install conda if not present
install_conda() {
    print_header "Installing Miniconda"
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        CONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        CONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
    else
        print_error "Unsupported OS. Please install conda manually."
        exit 1
    fi
    
    print_status "Downloading Miniconda..."
    wget -O miniconda.sh "$CONDA_URL"
    
    print_status "Installing Miniconda..."
    bash miniconda.sh -b -p "$HOME/miniconda3"
    
    print_status "Adding conda to PATH..."
    export PATH="$HOME/miniconda3/bin:$PATH"
    
    # Initialize conda
    conda init bash
    
    print_success "Miniconda installed successfully!"
    print_warning "Please restart your terminal or run: source ~/.bashrc"
    
    rm miniconda.sh
}

# Setup conda environment
setup_conda_env() {
    print_header "Setting up Conda Environment"
    
    ENV_NAME="image-quality-assessment"
    
    # Check if environment already exists
    if conda env list | grep -q "$ENV_NAME"; then
        print_warning "Environment '$ENV_NAME' already exists"
        read -p "Do you want to remove and recreate it? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_status "Removing existing environment..."
            conda env remove -n "$ENV_NAME" -y
        else
            print_status "Using existing environment"
            return 0
        fi
    fi
    
    print_status "Creating conda environment from environment.yml..."
    conda env create -f environment.yml
    
    print_success "Environment '$ENV_NAME' created successfully!"
}

# Verify installation
verify_installation() {
    print_header "Verifying Installation"
    
    print_status "Activating environment..."
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate image-quality-assessment
    
    print_status "Running verification script..."
    python setup_conda.py --verify
    
    print_success "Installation verified!"
}

# Generate sample images
generate_samples() {
    print_header "Generating Sample Images"
    
    print_status "Creating sample images for testing..."
    python demo.py
    
    print_success "Sample images generated in samples/ directory"
}

# Run comprehensive demo
run_demo() {
    print_header "Running Comprehensive Demo"
    
    print_status "Testing all system features..."
    python comprehensive_demo.py
    
    print_success "Demo completed successfully!"
}

# Main setup function
main() {
    print_header "Image Quality Assessment System Setup"
    
    echo "This script will set up the Image Quality Assessment System with conda."
    echo "It will install dependencies and test the system functionality."
    echo
    
    # Check current directory
    if [[ ! -f "environment.yml" ]]; then
        print_error "environment.yml not found. Please run this script from the project directory."
        exit 1
    fi
    
    # Check conda installation
    if ! check_conda; then
        read -p "Conda not found. Do you want to install Miniconda? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            install_conda
            print_warning "Please restart your terminal and run this script again."
            exit 0
        else
            print_error "Conda is required. Please install it manually."
            exit 1
        fi
    fi
    
    # Setup environment
    setup_conda_env
    
    # Verify installation
    verify_installation
    
    # Generate samples
    generate_samples
    
    # Run demo
    run_demo
    
    print_header "Setup Complete!"
    
    echo "🎉 Image Quality Assessment System is ready to use!"
    echo
    echo "📋 To get started:"
    echo "   conda activate image-quality-assessment"
    echo "   python image_quality_assessor.py samples/high_quality.jpg"
    echo
    echo "📋 To start the web interface:"
    echo "   python web_app.py"
    echo "   # Then open http://localhost:12000"
    echo
    echo "📋 To test RAW support:"
    echo "   python test_raw_support.py"
    echo
    echo "📋 Available commands:"
    echo "   make help          # Show all available commands"
    echo "   make test          # Run comprehensive tests"
    echo "   make web           # Start web interface"
    echo
}

# Handle command line arguments
case "${1:-}" in
    --help|-h)
        echo "Image Quality Assessment System Setup Script"
        echo
        echo "Usage: $0 [option]"
        echo
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo "  --conda-only   Only setup conda environment"
        echo "  --verify       Only verify installation"
        echo "  --demo         Only run demo"
        echo
        exit 0
        ;;
    --conda-only)
        check_conda || exit 1
        setup_conda_env
        ;;
    --verify)
        verify_installation
        ;;
    --demo)
        run_demo
        ;;
    *)
        main
        ;;
esac