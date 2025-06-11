#!/usr/bin/env python3
"""
Image Quality Assessment Tool
Automated assessment of image quality with natural language explanations
"""

import cv2
import numpy as np
from PIL import Image, ImageStat
from skimage import measure, filters, feature
from scipy import ndimage
import matplotlib.pyplot as plt
import os
import json
import rawpy
from typing import Dict, Tuple, List, Any


class ImageQualityAssessor:
    """Main class for assessing image quality with multiple metrics"""
    
    def __init__(self):
        self.results = {}
        self.explanations = {}
        
        # Supported raw formats
        self.raw_extensions = {
            '.arw', '.cr2', '.cr3', '.nef', '.dng', '.raf', '.orf', '.rw2', 
            '.pef', '.srw', '.x3f', '.3fr', '.fff', '.iiq', '.k25', '.kdc',
            '.mef', '.mos', '.mrw', '.nrw', '.ptx', '.r3d', '.raw', '.rwl',
            '.rwz', '.sr2', '.srf', '.srw'
        }
    
    def load_image(self, image_path: str) -> Tuple[np.ndarray, np.ndarray]:
        """Load image in both BGR (OpenCV) and RGB formats, supporting raw files"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Check if it's a raw file
        file_ext = os.path.splitext(image_path)[1].lower()
        
        if file_ext in self.raw_extensions:
            # Load raw image using rawpy
            try:
                with rawpy.imread(image_path) as raw:
                    # Process raw to RGB with default settings
                    img_rgb = raw.postprocess(
                        use_camera_wb=True,  # Use camera white balance
                        half_size=False,     # Full resolution
                        no_auto_bright=True, # Preserve exposure
                        output_bps=8         # 8-bit output
                    )
                
                # Convert RGB to BGR for OpenCV compatibility
                img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
                
                return img_bgr, img_rgb
                
            except Exception as e:
                raise ValueError(f"Could not process raw image {image_path}: {str(e)}")
        
        else:
            # Load regular image with OpenCV (BGR)
            img_bgr = cv2.imread(image_path)
            if img_bgr is None:
                raise ValueError(f"Could not load image: {image_path}")
            
            # Convert to RGB
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            
            return img_bgr, img_rgb
    
    def assess_sharpness(self, image: np.ndarray) -> Dict[str, Any]:
        """Assess image sharpness using Laplacian variance"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Thresholds for sharpness assessment
        if laplacian_var > 500:
            quality = "Excellent"
            description = "The image is very sharp with crisp details and clear edges."
        elif laplacian_var > 200:
            quality = "Good"
            description = "The image has good sharpness with most details clearly visible."
        elif laplacian_var > 100:
            quality = "Fair"
            description = "The image has moderate sharpness but some details may appear soft."
        else:
            quality = "Poor"
            description = "The image appears blurry or out of focus with poor detail definition."
        
        return {
            "score": round(laplacian_var, 2),
            "quality": quality,
            "description": description,
            "metric": "Laplacian Variance"
        }
    
    def assess_brightness(self, image: np.ndarray) -> Dict[str, Any]:
        """Assess image brightness"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mean_brightness = np.mean(gray)
        
        # Brightness assessment (0-255 scale)
        if 80 <= mean_brightness <= 180:
            quality = "Excellent"
            description = "The image has optimal brightness with good visibility of details."
        elif 60 <= mean_brightness <= 200:
            quality = "Good"
            description = "The image brightness is acceptable with minor adjustments needed."
        elif 40 <= mean_brightness <= 220:
            quality = "Fair"
            description = "The image is either slightly too dark or too bright."
        else:
            if mean_brightness < 40:
                quality = "Poor"
                description = "The image is too dark, making details difficult to see."
            else:
                quality = "Poor"
                description = "The image is overexposed with blown-out highlights."
        
        return {
            "score": round(mean_brightness, 2),
            "quality": quality,
            "description": description,
            "metric": "Mean Brightness (0-255)"
        }
    
    def assess_contrast(self, image: np.ndarray) -> Dict[str, Any]:
        """Assess image contrast using standard deviation"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        contrast_std = np.std(gray)
        
        # Contrast assessment
        if contrast_std > 60:
            quality = "Excellent"
            description = "The image has excellent contrast with a good range of tones."
        elif contrast_std > 40:
            quality = "Good"
            description = "The image has good contrast with adequate tonal separation."
        elif contrast_std > 25:
            quality = "Fair"
            description = "The image has moderate contrast but could benefit from enhancement."
        else:
            quality = "Poor"
            description = "The image has poor contrast appearing flat or washed out."
        
        return {
            "score": round(contrast_std, 2),
            "quality": quality,
            "description": description,
            "metric": "Standard Deviation"
        }
    
    def assess_noise(self, image: np.ndarray) -> Dict[str, Any]:
        """Assess image noise using edge detection"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur and calculate difference
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        noise_estimate = np.std(gray - blurred)
        
        # Noise assessment
        if noise_estimate < 5:
            quality = "Excellent"
            description = "The image has minimal noise with clean, smooth areas."
        elif noise_estimate < 10:
            quality = "Good"
            description = "The image has low noise levels that don't significantly impact quality."
        elif noise_estimate < 20:
            quality = "Fair"
            description = "The image has moderate noise that may be noticeable in smooth areas."
        else:
            quality = "Poor"
            description = "The image has high noise levels that significantly degrade quality."
        
        return {
            "score": round(noise_estimate, 2),
            "quality": quality,
            "description": description,
            "metric": "Noise Estimate (lower is better)"
        }
    
    def assess_color_balance(self, image: np.ndarray) -> Dict[str, Any]:
        """Assess color balance by analyzing channel means"""
        b, g, r = cv2.split(image)
        
        mean_b, mean_g, mean_r = np.mean(b), np.mean(g), np.mean(r)
        
        # Calculate color balance deviation
        overall_mean = (mean_r + mean_g + mean_b) / 3
        deviations = [abs(mean_r - overall_mean), abs(mean_g - overall_mean), abs(mean_b - overall_mean)]
        max_deviation = max(deviations)
        
        # Color balance assessment
        if max_deviation < 10:
            quality = "Excellent"
            description = "The image has excellent color balance with neutral tones."
        elif max_deviation < 20:
            quality = "Good"
            description = "The image has good color balance with minor color casts."
        elif max_deviation < 35:
            quality = "Fair"
            description = "The image has noticeable color cast that may need correction."
        else:
            # Determine dominant color cast
            if mean_r > mean_g and mean_r > mean_b:
                cast = "reddish"
            elif mean_g > mean_r and mean_g > mean_b:
                cast = "greenish"
            else:
                cast = "bluish"
            
            quality = "Poor"
            description = f"The image has a strong {cast} color cast affecting overall appearance."
        
        return {
            "score": round(max_deviation, 2),
            "quality": quality,
            "description": description,
            "metric": "Max Channel Deviation",
            "channel_means": {"red": round(mean_r, 2), "green": round(mean_g, 2), "blue": round(mean_b, 2)}
        }
    
    def assess_saturation(self, image: np.ndarray) -> Dict[str, Any]:
        """Assess color saturation"""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        saturation = hsv[:, :, 1]
        mean_saturation = np.mean(saturation)
        
        # Saturation assessment (0-255 scale)
        if 80 <= mean_saturation <= 150:
            quality = "Excellent"
            description = "The image has optimal color saturation with vibrant but natural colors."
        elif 60 <= mean_saturation <= 180:
            quality = "Good"
            description = "The image has good color saturation with appealing colors."
        elif 40 <= mean_saturation <= 200:
            quality = "Fair"
            description = "The image saturation could be improved for better color appeal."
        else:
            if mean_saturation < 40:
                quality = "Poor"
                description = "The image appears washed out with very low color saturation."
            else:
                quality = "Poor"
                description = "The image is oversaturated with unnatural, intense colors."
        
        return {
            "score": round(mean_saturation, 2),
            "quality": quality,
            "description": description,
            "metric": "Mean Saturation (0-255)"
        }
    
    def assess_resolution_quality(self, image: np.ndarray) -> Dict[str, Any]:
        """Assess resolution and detail quality"""
        height, width = image.shape[:2]
        total_pixels = height * width
        
        # Edge detection for detail assessment
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / total_pixels
        
        # Resolution categories
        if total_pixels >= 8000000:  # 8MP+
            res_quality = "High Resolution"
        elif total_pixels >= 2000000:  # 2MP+
            res_quality = "Medium Resolution"
        else:
            res_quality = "Low Resolution"
        
        # Detail assessment
        if edge_density > 0.1:
            detail_quality = "Rich Detail"
            description = f"The image is {res_quality.lower()} ({width}x{height}) with rich detail and sharp edges."
        elif edge_density > 0.05:
            detail_quality = "Moderate Detail"
            description = f"The image is {res_quality.lower()} ({width}x{height}) with moderate detail levels."
        else:
            detail_quality = "Low Detail"
            description = f"The image is {res_quality.lower()} ({width}x{height}) with limited detail or smooth content."
        
        return {
            "resolution": f"{width}x{height}",
            "total_pixels": total_pixels,
            "edge_density": round(edge_density, 4),
            "resolution_quality": res_quality,
            "detail_quality": detail_quality,
            "description": description
        }
    
    def calculate_overall_score(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall image quality score"""
        quality_scores = {
            "Excellent": 4,
            "Good": 3,
            "Fair": 2,
            "Poor": 1
        }
        
        # Weight different aspects
        weights = {
            "sharpness": 0.25,
            "brightness": 0.15,
            "contrast": 0.20,
            "noise": 0.20,
            "color_balance": 0.10,
            "saturation": 0.10
        }
        
        total_score = 0
        for aspect, weight in weights.items():
            if aspect in results:
                quality = results[aspect]["quality"]
                total_score += quality_scores[quality] * weight
        
        # Convert to percentage
        overall_percentage = (total_score / 4) * 100
        
        # Overall assessment
        if overall_percentage >= 85:
            overall_quality = "Excellent"
            summary = "This is a high-quality image with excellent technical characteristics."
        elif overall_percentage >= 70:
            overall_quality = "Good"
            summary = "This is a good quality image with minor areas for improvement."
        elif overall_percentage >= 55:
            overall_quality = "Fair"
            summary = "This image has acceptable quality but would benefit from enhancement."
        else:
            overall_quality = "Poor"
            summary = "This image has significant quality issues that should be addressed."
        
        return {
            "score": round(overall_percentage, 1),
            "quality": overall_quality,
            "summary": summary
        }
    
    def assess_image(self, image_path: str) -> Dict[str, Any]:
        """Perform comprehensive image quality assessment"""
        try:
            img_bgr, img_rgb = self.load_image(image_path)
            
            results = {
                "image_path": image_path,
                "sharpness": self.assess_sharpness(img_bgr),
                "brightness": self.assess_brightness(img_bgr),
                "contrast": self.assess_contrast(img_bgr),
                "noise": self.assess_noise(img_bgr),
                "color_balance": self.assess_color_balance(img_bgr),
                "saturation": self.assess_saturation(img_bgr),
                "resolution": self.assess_resolution_quality(img_bgr)
            }
            
            # Calculate overall score
            results["overall"] = self.calculate_overall_score(results)
            
            return results
            
        except Exception as e:
            return {"error": str(e)}
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate a natural language report of the assessment"""
        if "error" in results:
            return f"Error assessing image: {results['error']}"
        
        report = []
        report.append("=" * 60)
        report.append("IMAGE QUALITY ASSESSMENT REPORT")
        report.append("=" * 60)
        report.append(f"Image: {os.path.basename(results['image_path'])}")
        report.append("")
        
        # Overall assessment
        overall = results["overall"]
        report.append(f"OVERALL QUALITY: {overall['quality']} ({overall['score']}%)")
        report.append(f"{overall['summary']}")
        report.append("")
        
        # Detailed assessments
        report.append("DETAILED ANALYSIS:")
        report.append("-" * 40)
        
        # Resolution and detail
        res = results["resolution"]
        report.append(f"Resolution & Detail:")
        report.append(f"  • {res['description']}")
        report.append("")
        
        # Technical aspects
        aspects = ["sharpness", "brightness", "contrast", "noise", "color_balance", "saturation"]
        
        for aspect in aspects:
            if aspect in results:
                data = results[aspect]
                aspect_name = aspect.replace("_", " ").title()
                report.append(f"{aspect_name}:")
                report.append(f"  • Quality: {data['quality']}")
                report.append(f"  • Score: {data['score']} ({data['metric']})")
                report.append(f"  • {data['description']}")
                report.append("")
        
        # Recommendations
        report.append("RECOMMENDATIONS:")
        report.append("-" * 40)
        recommendations = self.generate_recommendations(results)
        for rec in recommendations:
            report.append(f"• {rec}")
        
        return "\n".join(report)
    
    def generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate improvement recommendations based on assessment"""
        recommendations = []
        
        if results["sharpness"]["quality"] in ["Poor", "Fair"]:
            recommendations.append("Consider using a tripod or faster shutter speed to improve sharpness")
        
        if results["brightness"]["quality"] in ["Poor", "Fair"]:
            if results["brightness"]["score"] < 80:
                recommendations.append("Increase exposure or adjust shadows to brighten the image")
            else:
                recommendations.append("Reduce exposure or adjust highlights to prevent overexposure")
        
        if results["contrast"]["quality"] in ["Poor", "Fair"]:
            recommendations.append("Enhance contrast using curves or levels adjustment")
        
        if results["noise"]["quality"] in ["Poor", "Fair"]:
            recommendations.append("Apply noise reduction or use lower ISO settings when capturing")
        
        if results["color_balance"]["quality"] in ["Poor", "Fair"]:
            recommendations.append("Adjust white balance or apply color correction")
        
        if results["saturation"]["quality"] in ["Poor", "Fair"]:
            if results["saturation"]["score"] < 60:
                recommendations.append("Increase color saturation for more vibrant appearance")
            else:
                recommendations.append("Reduce saturation for more natural color appearance")
        
        if not recommendations:
            recommendations.append("Image quality is good - no major improvements needed")
        
        return recommendations


def main():
    """Main function for command-line usage"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python image_quality_assessor.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    assessor = ImageQualityAssessor()
    results = assessor.assess_image(image_path)
    report = assessor.generate_report(results)
    
    print(report)
    
    # Save results as JSON
    output_file = f"{os.path.splitext(image_path)[0]}_quality_report.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: {output_file}")


if __name__ == "__main__":
    main()