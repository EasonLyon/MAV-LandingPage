# Image Editing Examples and Templates

This document provides comprehensive examples of how to use the advanced image editing features for landing page optimization.

## Quick Start Examples

### Basic Image Editing
```bash
# Simple color change
python image_generator.py edit image.jpg "Change the car color to red"

# Background replacement
python image_generator.py edit image.jpg "Replace the background with a modern office"

# Text replacement
python image_generator.py replace-text image.jpg "Welcome" "Get Started"
```

### Template-Based Editing
```bash
# Use predefined color change template
python image_generator.py edit-template image.jpg color_change -p object=car -p new_color=blue

# Professional enhancement
python image_generator.py edit-template image.jpg professional_enhancement -p specific_changes="formal attire, clean background"

# Add company logo
python image_generator.py edit-template image.jpg logo_addition -p logo_description="tech company" -p position="top right"
```

### Smart Editing (AI-Powered)
```bash
# Automatically suggest and apply edits based on ad copy
python image_generator.py smart-edit image.jpg "Professional consulting services. Trusted by 500+ companies." --interactive

# Apply all high-priority suggestions automatically
python image_generator.py smart-edit image.jpg "Revolutionary AI software. Save 50% on operations." --apply-all
```

## Editing Templates Reference

### Object Modification Templates

#### 1. Color Change
**Template:** `color_change`
**Parameters:** `object`, `new_color`

```bash
python image_generator.py edit-template image.jpg color_change -p object=shirt -p new_color=blue
python image_generator.py edit-template image.jpg color_change -p object=background -p new_color=white
python image_generator.py edit-template image.jpg color_change -p object="call-to-action button" -p new_color=green
```

#### 2. Background Replacement
**Template:** `background_replacement`
**Parameters:** `new_background`

```bash
python image_generator.py edit-template image.jpg background_replacement -p new_background="modern office"
python image_generator.py edit-template image.jpg background_replacement -p new_background="clean white studio"
python image_generator.py edit-template image.jpg background_replacement -p new_background="professional conference room"
```

### Text Editing Templates

#### 3. Text Replacement
**Template:** `text_replacement`
**Parameters:** `original_text`, `new_text`

```bash
python image_generator.py edit-template image.jpg text_replacement -p original_text="Welcome" -p new_text="Get Started"
python image_generator.py edit-template image.jpg text_replacement -p original_text="Product Name" -p new_text="AI Solution"
python image_generator.py edit-template image.jpg text_replacement -p original_text="50% OFF" -p new_text="LIMITED TIME"
```

#### 4. CTA Enhancement
**Template:** `cta_enhancement`
**Parameters:** `new_cta`

```bash
python image_generator.py edit-template image.jpg cta_enhancement -p new_cta="Start Free Trial"
python image_generator.py edit-template image.jpg cta_enhancement -p new_cta="Get Instant Access"
python image_generator.py edit-template image.jpg cta_enhancement -p new_cta="Book Consultation"
```

### Brand Enhancement Templates

#### 5. Logo Addition
**Template:** `logo_addition`
**Parameters:** `logo_description`, `position`

```bash
python image_generator.py edit-template image.jpg logo_addition -p logo_description="modern tech company" -p position="top right"
python image_generator.py edit-template image.jpg logo_addition -p logo_description="medical clinic" -p position="bottom left"
python image_generator.py edit-template image.jpg logo_addition -p logo_description="consulting firm" -p position="top left"
```

#### 6. Brand Colors
**Template:** `brand_colors`
**Parameters:** `elements`, `brand_color_scheme`

```bash
python image_generator.py edit-template image.jpg brand_colors -p elements="buttons and accents" -p brand_color_scheme="blue and orange theme"
python image_generator.py edit-template image.jpg brand_colors -p elements="headers and highlights" -p brand_color_scheme="green and white theme"
python image_generator.py edit-template image.jpg brand_colors -p elements="borders and text" -p brand_color_scheme="red and black theme"
```

### Professional Enhancement Templates

#### 7. Professional Enhancement
**Template:** `professional_enhancement`
**Parameters:** `specific_changes`

```bash
python image_generator.py edit-template image.jpg professional_enhancement -p specific_changes="cleaner background, formal attire"
python image_generator.py edit-template image.jpg professional_enhancement -p specific_changes="better lighting, corporate setting"
python image_generator.py edit-template image.jpg professional_enhancement -p specific_changes="remove casual elements, add business accessories"
```

#### 8. Trust Building
**Template:** `trust_building`
**Parameters:** `trust_elements`

```bash
python image_generator.py edit-template image.jpg trust_building -p trust_elements="security badges, certification logos"
python image_generator.py edit-template image.jpg trust_building -p trust_elements="customer testimonial quotes, 5-star ratings"
python image_generator.py edit-template image.jpg trust_building -p trust_elements="award badges, industry certifications"
```

### Technical Enhancement Templates

#### 9. Lighting Improvement
**Template:** `lighting_improvement`
**Parameters:** `lighting_style`

```bash
python image_generator.py edit-template image.jpg lighting_improvement -p lighting_style="bright and professional"
python image_generator.py edit-template image.jpg lighting_improvement -p lighting_style="warm and inviting"
python image_generator.py edit-template image.jpg lighting_improvement -p lighting_style="dramatic and attention-grabbing"
```

#### 10. Resolution Enhancement
**Template:** `resolution_enhancement`
**Parameters:** None

```bash
python image_generator.py edit-template image.jpg resolution_enhancement
```

## Advanced Editing Workflows

### Iterative Editing Sequence

Create `edits_sequence.json`:
```json
[
  "Remove the object from her face",
  "She is now taking a selfie in the streets of Paris, it's a lovely day out",
  "It's now snowing, everything is covered in snow",
  "Add a warm winter coat and scarf for the cold weather"
]
```

Apply iteratively (each edit builds on the previous):
```bash
python image_generator.py batch-edit image.jpg edits_sequence.json --iterative
```

### Brand Consistency Workflow

```bash
# Step 1: Apply brand colors
python image_generator.py edit-template image.jpg brand_colors -p elements="buttons, headers, and key elements" -p brand_color_scheme="deep blue and orange corporate theme"

# Step 2: Add logo (use output from step 1)
python image_generator.py edit-template step1_output.jpg logo_addition -p logo_description="professional tech company" -p position="top right"

# Step 3: Professional polish (use output from step 2)
python image_generator.py edit-template step2_output.jpg professional_enhancement -p specific_changes="clean layout, consistent typography"
```

### CTA Optimization Workflow

```bash
# Step 1: Replace CTA text
python image_generator.py replace-text image.jpg "Sign Up" "Start Free Trial"

# Step 2: Enhance CTA visibility
python image_generator.py edit step1_output.jpg "Make the 'Start Free Trial' button more prominent with bold text and high contrast background"

# Step 3: Add urgency elements
python image_generator.py edit step2_output.jpg "Add 'Limited Time' text near the button in smaller font"
```

## Industry-Specific Examples

### Healthcare/Medical
```bash
# Professional medical image
python image_generator.py smart-edit doctor_image.jpg "Advanced medical imaging that saves lives. Our AI diagnostic tool detects diseases 50% faster."

# Manual approach
python image_generator.py edit-template doctor_image.jpg professional_enhancement -p specific_changes="clean medical environment, professional attire"
python image_generator.py edit-template output.jpg trust_building -p trust_elements="medical certifications, patient safety badges"
```

### Technology/Software
```bash
# Tech product showcase
python image_generator.py smart-edit software_image.jpg "Next-generation cloud platform that scales infinitely. 99.9% uptime guaranteed."

# Manual approach
python image_generator.py edit-template software_image.jpg brand_colors -p elements="interface elements" -p brand_color_scheme="cyan and magenta tech theme"
python image_generator.py edit-template output.jpg resolution_enhancement
```

### Real Estate
```bash
# Property showcase
python image_generator.py smart-edit property_image.jpg "Find your dream home with our exclusive property matching service. 95% customer satisfaction rate."

# Manual approach
python image_generator.py edit-template property_image.jpg lighting_improvement -p lighting_style="warm and inviting"
python image_generator.py edit-template output.jpg trust_building -p trust_elements="industry awards, customer testimonials"
```

### Financial Services
```bash
# Professional financial services
python image_generator.py smart-edit finance_image.jpg "Secure investment platform. Trusted by professionals, proven results since 2010."

# Manual approach
python image_generator.py edit-template finance_image.jpg professional_enhancement -p specific_changes="formal business attire, corporate environment"
python image_generator.py edit-template output.jpg brand_colors -p elements="accents and highlights" -p brand_color_scheme="dark blue and gold financial theme"
```

## Text Replacement Mastery

### Best Practices for Text Editing

#### Exact Text Matching
```bash
# Use exact text as it appears in the image
python image_generator.py replace-text image.jpg "Choose joy" "Choose BFL"
python image_generator.py replace-text image.jpg "SPECIAL OFFER" "LIMITED TIME"
```

#### Preserving Style vs. Updating Style
```bash
# Preserve original formatting
python image_generator.py replace-text image.jpg "Welcome" "Get Started" --preserve-style

# Update with new style
python image_generator.py replace-text image.jpg "Welcome" "Get Started" --no-preserve-style
```

#### Complex Text Replacements
```bash
# Multiple word replacement
python image_generator.py replace-text image.jpg "Sync & Bloom" "FLUX & JOY"

# Case-sensitive replacements
python image_generator.py edit image.jpg "Replace 'joy' with 'BFL' maintaining uppercase format"
```

## Batch Editing Strategies

### Independent Edits (A/B Testing)
Create `ab_test_edits.json`:
```json
[
  "Change the call-to-action button to green",
  "Change the call-to-action button to red", 
  "Change the call-to-action button to blue",
  "Make the call-to-action button larger and more prominent"
]
```

```bash
python image_generator.py batch-edit original_image.jpg ab_test_edits.json
```

### Progressive Enhancement
Create `enhancement_sequence.json`:
```json
[
  "Improve the lighting to be bright and professional",
  "Replace the background with a clean, modern office environment", 
  "Add a professional tech company logo in the top right corner",
  "Enhance image quality and sharpness, make details crisp and clear"
]
```

```bash
python image_generator.py batch-edit original_image.jpg enhancement_sequence.json --iterative
```

### Comprehensive Brand Application
Create `brand_application.json`:
```json
[
  "Apply brand colors: change buttons and accents to match blue and orange theme",
  "Add modern tech company logo in top right corner",
  "Replace 'Contact Us' with 'Start Free Trial' in bold, prominent style",
  "Add trust indicators: security badges, certification logos",
  "Make the image more professional and business-like: clean background, formal attire"
]
```

```bash
python image_generator.py batch-edit original_image.jpg brand_application.json --iterative
```

## Smart Editing Use Cases

### Automatic Optimization Based on Copy

#### E-commerce Product
```bash
python image_generator.py smart-edit product_image.jpg "Revolutionary fitness tracker with heart rate monitoring. 40% off today only. Join 100,000+ healthy users." --interactive
```

**Expected Automatic Suggestions:**
- Add pricing/discount emphasis
- Enhance product visibility
- Add trust indicators (user count)
- Improve professional appearance

#### B2B Service
```bash
python image_generator.py smart-edit service_image.jpg "Professional consulting services. Trusted by Fortune 500 companies. Guaranteed results." --apply-all
```

**Expected Automatic Suggestions:**
- Professional enhancement
- Trust building elements
- Corporate color scheme
- Logo addition

#### Educational Course
```bash
python image_generator.py smart-edit course_image.jpg "Master digital marketing in 30 days. Learn from industry experts. Limited enrollment." --interactive
```

**Expected Automatic Suggestions:**
- Educational color scheme (orange/teal)
- CTA enhancement for enrollment
- Trust indicators (expert credentials)
- Professional instructor appearance

## Character Consistency in Iterative Edits

### Maintaining Character Appearance
```bash
# First edit with character consistency instruction
python image_generator.py edit portrait.jpg "Remove the sunglasses. Maintain character appearance and facial features for consistency in future edits."

# Subsequent edits automatically maintain consistency
python image_generator.py edit output1.jpg "She is now in a professional office setting. Keep the same character appearance and style as previous image."

python image_generator.py edit output2.jpg "Add a business suit. Keep the same character appearance and style as previous image."
```

## Troubleshooting Common Editing Issues

### Text Not Changing
```bash
# Use exact quotes around text
python image_generator.py replace-text image.jpg "Choose joy" "Choose success"

# If text is stylized, describe the style
python image_generator.py edit image.jpg "Replace the decorative text 'joy' with 'success' maintaining the same artistic font style"
```

### Color Changes Not Applying
```bash
# Be specific about which object
python image_generator.py edit image.jpg "Change the red car in the center to blue color"

# Specify color relationships
python image_generator.py edit image.jpg "Change the button color to green while maintaining contrast with the white background"
```

### Background Not Replacing Well
```bash
# Include lighting instructions
python image_generator.py edit image.jpg "Replace background with modern office, ensure lighting matches the subject"

# Specify perspective consistency
python image_generator.py edit image.jpg "Replace background with conference room, maintain the same camera angle and perspective"
```

### Logo Addition Issues
```bash
# Specify size and integration
python image_generator.py edit image.jpg "Add a small, professional tech company logo in the top right corner that blends naturally with the image"

# Include transparency/integration instructions
python image_generator.py edit image.jpg "Add company logo with subtle transparency so it doesn't overpower the main subject"
```

## Performance Tips for Editing

1. **Start Simple**: Begin with basic edits before applying complex changes
2. **Use Templates**: Leverage predefined templates for consistent results
3. **Batch Similar Edits**: Group similar changes for efficiency
4. **Test Character Consistency**: Use iterative editing for character-based images
5. **Validate Results**: Always check edited images before using in production
6. **Smart Editing First**: Try smart-edit for automatic optimization suggestions

## Integration with Generation Workflow

### Full Landing Page Image Workflow
```bash
# Step 1: Generate initial image
python image_generator.py from-copy "Professional AI consulting. Transform your business with our proven methodology."

# Step 2: Apply smart edits based on copy
python image_generator.py smart-edit generated_image.jpg "Professional AI consulting. Transform your business with our proven methodology." --apply-all

# Step 3: Apply brand consistency
python image_generator.py edit-template final_image.jpg brand_colors -p elements="accents" -p brand_color_scheme="company blue and orange"

# Step 4: Add specific CTA
python image_generator.py replace-text branded_image.jpg "Contact Us" "Schedule Consultation"
```

This comprehensive editing system allows you to create perfectly optimized landing page images that align with your marketing goals and brand requirements.