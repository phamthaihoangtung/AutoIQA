#!/usr/bin/env python3
"""
Test script to demonstrate the Image Quality Assessment Tool
"""

from image_quality_assessor import ImageQualityAssessor
import json

def test_assessment():
    """Test the assessment functionality with sample images"""
    
    print("Testing Image Quality Assessment Tool")
    print("=" * 50)
    
    # Initialize assessor
    assessor = ImageQualityAssessor()
    
    # Test with high quality image
    print("\n1. Testing High Quality Image:")
    print("-" * 30)
    
    results = assessor.assess_image('samples/high_quality.jpg')
    
    if 'error' in results:
        print(f"Error: {results['error']}")
        return
    
    # Print key results
    overall = results['overall']
    print(f"Overall Quality: {overall['quality']} ({overall['score']}%)")
    print(f"Summary: {overall['summary']}")
    
    print("\nKey Metrics:")
    for metric in ['sharpness', 'brightness', 'contrast', 'noise']:
        if metric in results:
            data = results[metric]
            print(f"  {metric.title()}: {data['quality']} (Score: {data['score']})")
            print(f"    Description: {data['description']}")
    
    print(f"\nResolution: {results['resolution']['resolution']} - {results['resolution']['resolution_quality']}")
    
    # Test with blurry image
    print("\n\n2. Testing Blurry Image:")
    print("-" * 30)
    
    results_blur = assessor.assess_image('samples/blurry_image.jpg')
    
    if 'error' not in results_blur:
        overall_blur = results_blur['overall']
        print(f"Overall Quality: {overall_blur['quality']} ({overall_blur['score']}%)")
        print(f"Summary: {overall_blur['summary']}")
        
        print("\nSharpness Analysis:")
        sharpness = results_blur['sharpness']
        print(f"  Quality: {sharpness['quality']} (Score: {sharpness['score']})")
        print(f"  Description: {sharpness['description']}")
    
    # Generate recommendations
    print("\n\n3. Natural Language Explanations:")
    print("-" * 40)
    
    recommendations = assessor.generate_recommendations(results)
    print("Recommendations for high_quality.jpg:")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")
    
    print("\n4. Technical Details:")
    print("-" * 20)
    print("The assessment uses multiple computer vision algorithms:")
    print("• Sharpness: Laplacian variance to detect blur")
    print("• Brightness: Mean pixel intensity analysis")
    print("• Contrast: Standard deviation of pixel values")
    print("• Noise: Gaussian blur comparison method")
    print("• Color Balance: RGB channel deviation analysis")
    print("• Saturation: HSV color space analysis")
    
    print("\n5. Quality Thresholds:")
    print("-" * 20)
    print("Sharpness (Laplacian Variance):")
    print("  Excellent: >500, Good: >200, Fair: >100, Poor: ≤100")
    print("Brightness (0-255 scale):")
    print("  Optimal: 80-180, Acceptable: 60-200")
    print("Contrast (Standard Deviation):")
    print("  Excellent: >60, Good: >40, Fair: >25, Poor: ≤25")
    print("Noise (Lower is better):")
    print("  Excellent: <5, Good: <10, Fair: <20, Poor: ≥20")

if __name__ == "__main__":
    test_assessment()