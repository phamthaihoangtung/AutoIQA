# Image Quality Assessment Tool

A comprehensive Python application for automated image quality assessment with natural language explanations. This tool analyzes various aspects of image quality and provides detailed reports in human-readable format.

## Features

### Quality Metrics Analyzed
- **Sharpness**: Uses Laplacian variance to detect blur and focus issues
- **Brightness**: Analyzes overall exposure levels
- **Contrast**: Measures tonal range and dynamic range
- **Noise**: Detects image noise and grain
- **Color Balance**: Checks for color casts and white balance issues
- **Saturation**: Evaluates color vibrancy and intensity
- **Resolution & Detail**: Assesses image size and detail richness

### Natural Language Explanations
- Clear, non-technical descriptions of each quality aspect
- Overall quality summary with percentage score
- Specific recommendations for improvement
- Detailed technical metrics for advanced users

### Multiple Interfaces
- **Command Line**: Direct assessment of image files
- **Web Interface**: User-friendly browser-based tool
- **Python API**: Integration into other applications

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Installation**:
   ```bash
   python demo.py
   ```

## Usage

### Command Line Interface

**Assess a single image**:
```bash
python image_quality_assessor.py path/to/your/image.jpg
```

**Run demo with sample images**:
```bash
python demo.py
```

**Assess specific image with full report**:
```bash
python demo.py path/to/your/image.jpg
```

### Web Interface

1. **Start the web server**:
   ```bash
   python web_app.py
   ```

2. **Open your browser** and navigate to:
   - Local: `http://localhost:12000`
   - Remote: Use the provided runtime URL

3. **Upload an image** by:
   - Dragging and dropping onto the upload area
   - Clicking to browse and select a file

### Python API

```python
from image_quality_assessor import ImageQualityAssessor

# Initialize assessor
assessor = ImageQualityAssessor()

# Assess an image
results = assessor.assess_image('path/to/image.jpg')

# Generate natural language report
report = assessor.generate_report(results)
print(report)

# Access specific metrics
sharpness = results['sharpness']
print(f"Sharpness: {sharpness['quality']} - {sharpness['description']}")
```

## Sample Output

```
============================================================
IMAGE QUALITY ASSESSMENT REPORT
============================================================
Image: sample_image.jpg

OVERALL QUALITY: Good (78.5%)
This is a good quality image with minor areas for improvement.

DETAILED ANALYSIS:
----------------------------------------
Resolution & Detail:
  • The image is medium resolution (1920x1080) with moderate detail levels.

Sharpness:
  • Quality: Good
  • Score: 245.67 (Laplacian Variance)
  • The image has good sharpness with most details clearly visible.

Brightness:
  • Quality: Excellent
  • Score: 128.45 (Mean Brightness (0-255))
  • The image has optimal brightness with good visibility of details.

Contrast:
  • Quality: Good
  • Score: 52.34 (Standard Deviation)
  • The image has good contrast with adequate tonal separation.

Noise:
  • Quality: Excellent
  • Score: 4.23 (Noise Estimate (lower is better))
  • The image has minimal noise with clean, smooth areas.

Color Balance:
  • Quality: Fair
  • Score: 23.45 (Max Channel Deviation)
  • The image has noticeable color cast that may need correction.

Saturation:
  • Quality: Good
  • Score: 95.67 (Mean Saturation (0-255))
  • The image has good color saturation with appealing colors.

RECOMMENDATIONS:
----------------------------------------
• Adjust white balance or apply color correction
```

## Technical Details

### Quality Assessment Algorithms

1. **Sharpness Detection**:
   - Uses Laplacian operator to detect edges
   - Higher variance indicates sharper images
   - Thresholds: Excellent (>500), Good (>200), Fair (>100), Poor (≤100)

2. **Brightness Analysis**:
   - Calculates mean pixel intensity
   - Optimal range: 80-180 (0-255 scale)
   - Detects underexposure and overexposure

3. **Contrast Measurement**:
   - Uses standard deviation of pixel intensities
   - Higher values indicate better contrast
   - Thresholds: Excellent (>60), Good (>40), Fair (>25), Poor (≤25)

4. **Noise Estimation**:
   - Compares original with Gaussian-blurred version
   - Lower values indicate cleaner images
   - Thresholds: Excellent (<5), Good (<10), Fair (<20), Poor (≥20)

5. **Color Balance Check**:
   - Analyzes RGB channel means
   - Calculates maximum deviation from neutral
   - Detects color casts (red, green, blue bias)

6. **Saturation Analysis**:
   - Uses HSV color space saturation channel
   - Optimal range: 80-150 (0-255 scale)
   - Detects oversaturation and desaturation

### Supported Formats
- PNG, JPG, JPEG, GIF, BMP, TIFF, WebP
- Maximum file size: 16MB (web interface)
- RGB and grayscale images

### Performance
- Typical processing time: 1-3 seconds per image
- Memory usage: ~50-100MB for high-resolution images
- Optimized for batch processing

## File Structure

```
├── image_quality_assessor.py  # Main assessment engine
├── web_app.py                 # Flask web interface
├── demo.py                    # Demo script and sample generator
├── requirements.txt           # Python dependencies
├── templates/
│   └── index.html            # Web interface template
├── samples/                   # Generated sample images
└── uploads/                   # Temporary upload directory
```

## Customization

### Adding New Metrics
1. Add assessment method to `ImageQualityAssessor` class
2. Include in `assess_image()` method
3. Update `calculate_overall_score()` weights
4. Add explanations in `generate_recommendations()`

### Adjusting Thresholds
Modify threshold values in individual assessment methods:
```python
def assess_sharpness(self, image):
    # Adjust these thresholds based on your requirements
    if laplacian_var > 500:  # Excellent threshold
        quality = "Excellent"
    # ... etc
```

### Custom Weighting
Adjust metric weights in `calculate_overall_score()`:
```python
weights = {
    "sharpness": 0.30,      # Increase sharpness importance
    "brightness": 0.15,
    "contrast": 0.20,
    "noise": 0.15,          # Decrease noise importance
    "color_balance": 0.10,
    "saturation": 0.10
}
```

## Troubleshooting

### Common Issues

1. **"Could not load image" error**:
   - Check file path and permissions
   - Verify image format is supported
   - Ensure file is not corrupted

2. **Web interface not loading**:
   - Check if port 12000 is available
   - Verify Flask dependencies are installed
   - Check firewall settings

3. **Poor assessment accuracy**:
   - Ensure images are in RGB format
   - Check for extremely small or large images
   - Verify image content is suitable for analysis

### Performance Optimization

1. **For batch processing**:
   ```python
   assessor = ImageQualityAssessor()  # Initialize once
   for image_path in image_list:
       results = assessor.assess_image(image_path)
   ```

2. **For large images**:
   - Consider resizing before assessment
   - Use lower quality JPEG compression for faster loading

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

This project is open source and available under the MIT License.