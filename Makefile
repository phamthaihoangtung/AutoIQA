# Image Quality Assessment System - Makefile
# ==========================================

.PHONY: help install install-conda install-pip test demo web clean verify

# Default target
help:
	@echo "Image Quality Assessment System"
	@echo "==============================="
	@echo ""
	@echo "Available targets:"
	@echo "  install        - Install using conda (recommended)"
	@echo "  install-conda  - Install using conda environment"
	@echo "  install-pip    - Install using pip"
	@echo "  verify         - Verify installation"
	@echo "  test           - Run comprehensive tests"
	@echo "  demo           - Run demonstration"
	@echo "  web            - Start web interface"
	@echo "  samples        - Generate sample images"
	@echo "  clean          - Clean generated files"
	@echo "  help           - Show this help"

# Install using conda (recommended)
install: install-conda

# Install using conda environment
install-conda:
	@echo "🚀 Setting up conda environment..."
	conda env create -f environment.yml
	@echo "✅ Environment created successfully!"
	@echo "📋 To activate: conda activate image-quality-assessment"

# Install using pip
install-pip:
	@echo "🚀 Installing with pip..."
	pip install -r requirements.txt
	@echo "✅ Packages installed successfully!"

# Verify installation
verify:
	@echo "🔍 Verifying installation..."
	python setup_conda.py --verify

# Run comprehensive tests
test:
	@echo "🧪 Running comprehensive tests..."
	python comprehensive_demo.py

# Run demonstration
demo:
	@echo "🎬 Running demonstration..."
	python comprehensive_demo.py

# Start web interface
web:
	@echo "🌐 Starting web interface..."
	@echo "📍 Access at: http://localhost:12000"
	python web_app.py

# Generate sample images
samples:
	@echo "🖼️  Generating sample images..."
	python demo.py

# Test CLI with sample
test-cli:
	@echo "🖥️  Testing CLI interface..."
	python image_quality_assessor.py samples/high_quality.jpg

# Test RAW support
test-raw:
	@echo "📷 Testing RAW format support..."
	python test_raw_support.py

# Clean generated files
clean:
	@echo "🧹 Cleaning generated files..."
	rm -rf samples/*.json
	rm -rf uploads/*
	rm -rf __pycache__
	rm -rf *.pyc
	rm -rf .pytest_cache
	@echo "✅ Cleanup complete!"

# Development setup
dev-setup: install-conda verify samples
	@echo "🛠️  Development environment ready!"
	@echo "📋 Next steps:"
	@echo "   conda activate image-quality-assessment"
	@echo "   make test"

# Quick start for new users
quickstart: install verify samples demo
	@echo "🎉 Quick start complete!"
	@echo "📋 Try these commands:"
	@echo "   make test-cli"
	@echo "   make web"

# Show environment info
info:
	@echo "📊 Environment Information"
	@echo "=========================="
	@echo "Python version: $(shell python --version)"
	@echo "Current directory: $(shell pwd)"
	@echo "Environment: $(CONDA_DEFAULT_ENV)"
	@echo "Available samples: $(shell ls samples/*.jpg 2>/dev/null | wc -l) images"

# Run all tests
test-all: verify test test-cli test-raw
	@echo "✅ All tests completed!"

# Install and run everything
all: install verify samples test web