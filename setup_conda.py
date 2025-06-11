#!/usr/bin/env python3
"""
Conda Environment Setup Script for Image Quality Assessment System
================================================================

This script helps set up the conda environment for the image quality assessment system.
It provides both automated setup and manual instructions.
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔧 {description}...")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Success: {description}")
        if result.stdout:
            print(f"Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {description}")
        print(f"Error message: {e.stderr}")
        return False

def check_conda():
    """Check if conda is installed"""
    try:
        result = subprocess.run("conda --version", shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Conda found: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError:
        print("❌ Conda not found")
        return False

def setup_environment():
    """Set up the conda environment"""
    print("=" * 60)
    print("🚀 Image Quality Assessment - Conda Environment Setup")
    print("=" * 60)
    
    # Check if conda is available
    if not check_conda():
        print_manual_instructions()
        return False
    
    # Check if environment.yml exists
    if not os.path.exists("environment.yml"):
        print("❌ environment.yml not found in current directory")
        return False
    
    print(f"\n📍 Current directory: {os.getcwd()}")
    print(f"📍 Platform: {platform.system()} {platform.machine()}")
    
    # Create conda environment
    env_name = "image-quality-assessment"
    
    # Check if environment already exists
    result = subprocess.run(f"conda env list | grep {env_name}", shell=True, capture_output=True)
    if result.returncode == 0:
        print(f"\n⚠️  Environment '{env_name}' already exists")
        response = input("Do you want to remove and recreate it? (y/N): ").lower()
        if response == 'y':
            if not run_command(f"conda env remove -n {env_name} -y", f"Removing existing environment '{env_name}'"):
                return False
        else:
            print("Skipping environment creation")
            print_activation_instructions(env_name)
            return True
    
    # Create new environment
    if not run_command(f"conda env create -f environment.yml", "Creating conda environment"):
        return False
    
    print_activation_instructions(env_name)
    return True

def print_activation_instructions(env_name):
    """Print instructions for activating the environment"""
    print("\n" + "=" * 60)
    print("🎉 Environment Setup Complete!")
    print("=" * 60)
    
    print(f"\n📋 To activate the environment:")
    print(f"   conda activate {env_name}")
    
    print(f"\n📋 To test the installation:")
    print(f"   python comprehensive_demo.py")
    
    print(f"\n📋 To start the web interface:")
    print(f"   python web_app.py")
    
    print(f"\n📋 To deactivate when done:")
    print(f"   conda deactivate")
    
    print(f"\n📋 To remove the environment (if needed):")
    print(f"   conda env remove -n {env_name}")

def print_manual_instructions():
    """Print manual setup instructions"""
    print("\n" + "=" * 60)
    print("📋 Manual Setup Instructions")
    print("=" * 60)
    
    print("\n1️⃣ Install Miniconda or Anaconda:")
    print("   https://docs.conda.io/en/latest/miniconda.html")
    
    print("\n2️⃣ Create environment from file:")
    print("   conda env create -f environment.yml")
    
    print("\n3️⃣ Activate environment:")
    print("   conda activate image-quality-assessment")
    
    print("\n4️⃣ Test installation:")
    print("   python comprehensive_demo.py")
    
    print("\n" + "=" * 60)
    print("🔧 Alternative: Manual Package Installation")
    print("=" * 60)
    
    print("\n1️⃣ Create new environment:")
    print("   conda create -n image-quality-assessment python=3.9")
    
    print("\n2️⃣ Activate environment:")
    print("   conda activate image-quality-assessment")
    
    print("\n3️⃣ Install conda packages:")
    print("   conda install -c conda-forge numpy scipy matplotlib pillow scikit-image flask flask-cors requests")
    
    print("\n4️⃣ Install pip packages:")
    print("   pip install opencv-python rawpy")
    
    print("\n" + "=" * 60)
    print("🐳 Docker Alternative")
    print("=" * 60)
    
    print("\nIf you prefer Docker, you can also use:")
    print("   docker run -it --rm -v $(pwd):/workspace continuumio/miniconda3 bash")
    print("   cd /workspace")
    print("   conda env create -f environment.yml")
    print("   conda activate image-quality-assessment")

def verify_installation():
    """Verify that all packages are installed correctly"""
    print("\n" + "=" * 60)
    print("🔍 Verifying Installation")
    print("=" * 60)
    
    packages_to_test = [
        ("numpy", "import numpy; print(f'NumPy: {numpy.__version__}')"),
        ("opencv-python", "import cv2; print(f'OpenCV: {cv2.__version__}')"),
        ("pillow", "import PIL; print(f'Pillow: {PIL.__version__}')"),
        ("scikit-image", "import skimage; print(f'Scikit-image: {skimage.__version__}')"),
        ("flask", "import flask; print(f'Flask: {flask.__version__}')"),
        ("rawpy", "import rawpy; print(f'RawPy: {rawpy.__version__}')"),
        ("scipy", "import scipy; print(f'SciPy: {scipy.__version__}')"),
        ("matplotlib", "import matplotlib; print(f'Matplotlib: {matplotlib.__version__}')")
    ]
    
    all_good = True
    for package_name, test_code in packages_to_test:
        try:
            result = subprocess.run([sys.executable, "-c", test_code], 
                                  capture_output=True, text=True, check=True)
            print(f"✅ {result.stdout.strip()}")
        except subprocess.CalledProcessError as e:
            print(f"❌ {package_name}: Failed to import")
            print(f"   Error: {e.stderr.strip()}")
            all_good = False
    
    if all_good:
        print("\n🎉 All packages installed successfully!")
        print("\n📋 Ready to run:")
        print("   python comprehensive_demo.py")
    else:
        print("\n⚠️  Some packages failed to install. Please check the errors above.")

def main():
    """Main setup function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--verify":
        verify_installation()
        return
    
    if len(sys.argv) > 1 and sys.argv[1] == "--manual":
        print_manual_instructions()
        return
    
    success = setup_environment()
    
    if success:
        print("\n🔍 Verifying installation...")
        verify_installation()
    
    print("\n" + "=" * 60)
    print("📚 Additional Resources")
    print("=" * 60)
    print("• Conda documentation: https://docs.conda.io/")
    print("• Environment management: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html")
    print("• Troubleshooting: https://docs.conda.io/projects/conda/en/latest/user-guide/troubleshooting.html")

if __name__ == "__main__":
    main()