#!/usr/bin/env python3
"""
Demo script for Image Quality Assessment Tool
Creates sample images and demonstrates the assessment functionality
"""

import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import os
from image_quality_assessor import ImageQualityAssessor


def create_sample_images():
    """Create sample images with different quality characteristics"""
    
    # Create samples directory
    os.makedirs('samples', exist_ok=True)
    
    # 1. High quality image
    img_high = np.zeros((600, 800, 3), dtype=np.uint8)
    img_high[:] = (70, 130, 180)  # Steel blue background
    
    # Add some geometric shapes with good contrast
    cv2.rectangle(img_high, (100, 100), (300, 200), (255, 255, 255), -1)
    cv2.circle(img_high, (500, 150), 80, (255, 215, 0), -1)
    cv2.rectangle(img_high, (150, 300), (650, 500), (220, 20, 60), 3)
    
    # Add text
    cv2.putText(img_high, 'HIGH QUALITY SAMPLE', (200, 400), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    cv2.imwrite('samples/high_quality.jpg', img_high, [cv2.IMWRITE_JPEG_QUALITY, 95])
    
    # 2. Low quality (blurry) image
    img_blur = img_high.copy()
    img_blur = cv2.GaussianBlur(img_blur, (15, 15), 0)
    cv2.putText(img_blur, 'BLURRY SAMPLE', (250, 400), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imwrite('samples/blurry_image.jpg', img_blur, [cv2.IMWRITE_JPEG_QUALITY, 50])
    
    # 3. Dark image
    img_dark = (img_high * 0.3).astype(np.uint8)
    cv2.putText(img_dark, 'DARK SAMPLE', (280, 400), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 2)
    cv2.imwrite('samples/dark_image.jpg', img_dark, [cv2.IMWRITE_JPEG_QUALITY, 80])
    
    # 4. Overexposed image
    img_bright = np.clip(img_high.astype(np.float32) * 1.8 + 50, 0, 255).astype(np.uint8)
    cv2.putText(img_bright, 'BRIGHT SAMPLE', (260, 400), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 100, 100), 2)
    cv2.imwrite('samples/bright_image.jpg', img_bright, [cv2.IMWRITE_JPEG_QUALITY, 80])
    
    # 5. Noisy image
    img_noisy = img_high.copy()
    noise = np.random.normal(0, 25, img_noisy.shape).astype(np.int16)
    img_noisy = np.clip(img_noisy.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    cv2.putText(img_noisy, 'NOISY SAMPLE', (270, 400), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imwrite('samples/noisy_image.jpg', img_noisy, [cv2.IMWRITE_JPEG_QUALITY, 80])
    
    # 6. Low contrast image
    img_low_contrast = cv2.convertScaleAbs(img_high, alpha=0.5, beta=100)
    cv2.putText(img_low_contrast, 'LOW CONTRAST', (240, 400), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (150, 150, 150), 2)
    cv2.imwrite('samples/low_contrast.jpg', img_low_contrast, [cv2.IMWRITE_JPEG_QUALITY, 80])
    
    print("Sample images created in 'samples/' directory:")
    print("- high_quality.jpg: Well-balanced, sharp image")
    print("- blurry_image.jpg: Blurred version for sharpness testing")
    print("- dark_image.jpg: Underexposed image")
    print("- bright_image.jpg: Overexposed image")
    print("- noisy_image.jpg: Image with added noise")
    print("- low_contrast.jpg: Low contrast image")


def run_demo():
    """Run assessment on all sample images"""
    
    # Create sample images if they don't exist
    if not os.path.exists('samples'):
        print("Creating sample images...")
        create_sample_images()
        print()
    
    # Initialize assessor
    assessor = ImageQualityAssessor()
    
    # Get all sample images
    sample_files = [f for f in os.listdir('samples') if f.endswith('.jpg')]
    
    print("Running Image Quality Assessment Demo")
    print("=" * 50)
    
    for filename in sorted(sample_files):
        filepath = os.path.join('samples', filename)
        print(f"\nAssessing: {filename}")
        print("-" * 30)
        
        # Assess image
        results = assessor.assess_image(filepath)
        
        if 'error' in results:
            print(f"Error: {results['error']}")
            continue
        
        # Print summary
        overall = results['overall']
        print(f"Overall Quality: {overall['quality']} ({overall['score']}%)")
        print(f"Summary: {overall['summary']}")
        
        # Print key metrics
        print("\nKey Metrics:")
        metrics = ['sharpness', 'brightness', 'contrast', 'noise']
        for metric in metrics:
            if metric in results:
                data = results[metric]
                print(f"  {metric.title()}: {data['quality']} (Score: {data['score']})")
        
        print(f"\nResolution: {results['resolution']['resolution']} - {results['resolution']['resolution_quality']}")


def assess_single_image(image_path):
    """Assess a single image and display full report"""
    
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        return
    
    assessor = ImageQualityAssessor()
    results = assessor.assess_image(image_path)
    
    if 'error' in results:
        print(f"Error assessing image: {results['error']}")
        return
    
    # Generate and display full report
    report = assessor.generate_report(results)
    print(report)
    
    # Save detailed results
    output_file = f"{os.path.splitext(image_path)[0]}_assessment.json"
    import json
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: {output_file}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Assess specific image
        image_path = sys.argv[1]
        assess_single_image(image_path)
    else:
        # Run demo with sample images
        run_demo()