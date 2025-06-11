#!/usr/bin/env python3
"""
Test script to demonstrate RAW image support
"""

from image_quality_assessor import ImageQualityAssessor
import os

def test_raw_support():
    """Test the raw image support functionality"""
    
    print("Testing RAW Image Support")
    print("=" * 50)
    
    # Initialize assessor
    assessor = ImageQualityAssessor()
    
    print("Supported RAW formats:")
    raw_formats = sorted(list(assessor.raw_extensions))
    for i, fmt in enumerate(raw_formats, 1):
        print(f"  {i:2d}. {fmt.upper()}")
    
    print(f"\nTotal supported RAW formats: {len(raw_formats)}")
    
    print("\nRAW Format Details:")
    print("-" * 30)
    
    format_info = {
        '.arw': 'Sony Alpha RAW',
        '.cr2': 'Canon RAW Version 2',
        '.cr3': 'Canon RAW Version 3',
        '.nef': 'Nikon Electronic Format',
        '.dng': 'Adobe Digital Negative',
        '.raf': 'Fujifilm RAW',
        '.orf': 'Olympus RAW Format',
        '.rw2': 'Panasonic RAW',
        '.pef': 'Pentax Electronic Format',
        '.srw': 'Samsung RAW',
        '.raw': 'Generic RAW format'
    }
    
    for ext, description in format_info.items():
        print(f"  {ext.upper():<5} - {description}")
    
    print("\nRAW Processing Features:")
    print("-" * 25)
    print("• Automatic white balance using camera settings")
    print("• Full resolution processing (no downsampling)")
    print("• Exposure preservation (no auto-brightness)")
    print("• 8-bit output for quality analysis")
    print("• Compatible with all existing quality metrics")
    
    print("\nRAW vs JPEG Quality Assessment:")
    print("-" * 35)
    print("RAW files typically provide:")
    print("• Higher dynamic range for better contrast analysis")
    print("• More accurate color information")
    print("• Better noise characteristics")
    print("• Higher bit depth for more precise measurements")
    print("• No compression artifacts")
    
    print("\nUsage Examples:")
    print("-" * 15)
    print("Command Line:")
    print("  python image_quality_assessor.py photo.arw")
    print("  python image_quality_assessor.py image.cr2")
    print("  python image_quality_assessor.py shot.nef")
    
    print("\nPython API:")
    print("  from image_quality_assessor import ImageQualityAssessor")
    print("  assessor = ImageQualityAssessor()")
    print("  results = assessor.assess_image('photo.dng')")
    
    print("\nWeb Interface:")
    print("  Upload any supported RAW file through the web interface")
    print("  at http://localhost:8080")
    
    print("\nTechnical Notes:")
    print("-" * 16)
    print("• RAW processing uses the rawpy library")
    print("• Camera white balance is automatically applied")
    print("• Processing may take longer than JPEG files")
    print("• Large RAW files are supported (up to 16MB via web)")
    print("• All quality metrics work identically with RAW and JPEG")

if __name__ == "__main__":
    test_raw_support()