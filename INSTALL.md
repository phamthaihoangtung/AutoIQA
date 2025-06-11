# Installation Guide - Image Quality Assessment System

This guide provides multiple installation methods for the Image Quality Assessment System, including conda environment setup.

## 🚀 Quick Start (Recommended)

### Option 1: Automated Conda Setup

```bash
# Clone or download the project
cd image-quality-assessment

# Run automated setup
python setup_conda.py
```

### Option 2: Manual Conda Setup

```bash
# Create environment from file
conda env create -f environment.yml

# Activate environment
conda activate image-quality-assessment

# Verify installation
python setup_conda.py --verify
```

## 📋 Installation Methods

### Method 1: Conda Environment (Recommended)

**Prerequisites:**
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution)

**Step-by-step:**

1. **Install Conda** (if not already installed):
   ```bash
   # Download and install Miniconda
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   bash Miniconda3-latest-Linux-x86_64.sh
   ```

2. **Create Environment:**
   ```bash
   conda env create -f environment.yml
   ```

3. **Activate Environment:**
   ```bash
   conda activate image-quality-assessment
   ```

4. **Test Installation:**
   ```bash
   python comprehensive_demo.py
   ```

### Method 2: Manual Conda Installation

```bash
# Create new environment
conda create -n image-quality-assessment python=3.9

# Activate environment
conda activate image-quality-assessment

# Install conda packages
conda install -c conda-forge numpy scipy matplotlib pillow scikit-image flask flask-cors requests

# Install pip packages
pip install opencv-python rawpy
```

### Method 3: Pip Installation

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Method 4: Docker Setup

```bash
# Using conda in Docker
docker run -it --rm -v $(pwd):/workspace continuumio/miniconda3 bash
cd /workspace
conda env create -f environment.yml
conda activate image-quality-assessment
```

## 🔧 Environment Details

### Conda Environment Specification

The `environment.yml` file includes:

```yaml
name: image-quality-assessment
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.9
  - pip
  - numpy
  - scipy
  - matplotlib
  - pillow
  - scikit-image
  - flask
  - flask-cors
  - requests
  - pip:
    - opencv-python
    - rawpy
```

### Package Versions

| Package | Version | Purpose |
|---------|---------|---------|
| Python | 3.9+ | Core runtime |
| NumPy | Latest | Numerical computations |
| OpenCV | Latest | Image processing |
| Pillow | Latest | Image I/O |
| Scikit-image | Latest | Advanced image analysis |
| Flask | Latest | Web framework |
| RawPy | Latest | RAW image processing |
| SciPy | Latest | Scientific computing |
| Matplotlib | Latest | Visualization |

## 🧪 Verification

### Automated Verification

```bash
python setup_conda.py --verify
```

### Manual Verification

```bash
python -c "
import numpy, cv2, PIL, skimage, flask, rawpy, scipy, matplotlib
print('✅ All packages imported successfully!')
print(f'NumPy: {numpy.__version__}')
print(f'OpenCV: {cv2.__version__}')
print(f'Pillow: {PIL.__version__}')
print(f'RawPy: {rawpy.__version__}')
"
```

### Test System Functionality

```bash
# Test CLI interface
python image_quality_assessor.py samples/high_quality.jpg

# Test RAW support
python test_raw_support.py

# Test web interface
python web_app.py
```

## 🐛 Troubleshooting

### Common Issues

1. **Conda not found:**
   ```bash
   # Add conda to PATH
   export PATH="$HOME/miniconda3/bin:$PATH"
   # Or restart terminal after conda installation
   ```

2. **Environment creation fails:**
   ```bash
   # Update conda
   conda update conda
   
   # Clear conda cache
   conda clean --all
   
   # Try creating environment again
   conda env create -f environment.yml
   ```

3. **OpenCV installation issues:**
   ```bash
   # Alternative OpenCV installation
   conda install -c conda-forge opencv
   ```

4. **RawPy compilation errors:**
   ```bash
   # Install build tools (Linux/Mac)
   conda install gcc_linux-64 gxx_linux-64  # Linux
   # or
   xcode-select --install  # Mac
   
   # Windows: Install Visual Studio Build Tools
   ```

5. **Permission errors:**
   ```bash
   # Use user installation
   pip install --user -r requirements.txt
   ```

### Platform-Specific Notes

**Windows:**
- Install Visual Studio Build Tools for RawPy compilation
- Use Anaconda Prompt for conda commands

**macOS:**
- Install Xcode command line tools: `xcode-select --install`
- Use Homebrew for additional dependencies if needed

**Linux:**
- Install build essentials: `sudo apt-get install build-essential`
- Some distributions may need additional libraries

## 🔄 Environment Management

### Useful Commands

```bash
# List environments
conda env list

# Update environment
conda env update -f environment.yml

# Export current environment
conda env export > environment.yml

# Remove environment
conda env remove -n image-quality-assessment

# Clone environment
conda create --name new-env --clone image-quality-assessment
```

### Updating Dependencies

```bash
# Activate environment
conda activate image-quality-assessment

# Update all packages
conda update --all

# Update specific package
conda update numpy

# Update pip packages
pip install --upgrade opencv-python rawpy
```

## 🚀 Quick Test

After installation, run this quick test:

```bash
# Activate environment
conda activate image-quality-assessment

# Run comprehensive demo
python comprehensive_demo.py

# Expected output:
# ✅ CLI interface working
# ✅ RAW support (27 formats)
# ✅ Quality metrics functional
# ✅ Natural language explanations
```

## 📞 Support

If you encounter issues:

1. **Check the troubleshooting section above**
2. **Verify your conda installation**: `conda --version`
3. **Check Python version**: `python --version` (should be 3.9+)
4. **Run verification script**: `python setup_conda.py --verify`
5. **Check environment**: `conda list` (in activated environment)

## 🎯 Next Steps

After successful installation:

1. **Test basic functionality**: `python comprehensive_demo.py`
2. **Try CLI assessment**: `python image_quality_assessor.py samples/high_quality.jpg`
3. **Start web interface**: `python web_app.py`
4. **Upload RAW files**: Test with your camera's RAW files
5. **Explore the API**: Check the documentation for integration

---

**Environment Name:** `image-quality-assessment`  
**Python Version:** 3.9+  
**Total Dependencies:** 10 packages  
**RAW Formats Supported:** 27 formats  
**Installation Time:** ~5-10 minutes