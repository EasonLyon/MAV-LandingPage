# Landing Page Image Generator & Editor

A comprehensive Python system for generating and editing high-quality images for landing pages using Flux AI with advanced prompt generation, visual style templates, and powerful editing capabilities.

## 🚀 Features

### Image Generation
- **Advanced Prompt Generation**: Transforms advertising copy into detailed image prompts using psychological frameworks
- **6 Visual Style Templates**: High contrast, incongruous elements, eye contact, negative space, hand-drawn, and cute+creepy styles
- **25+ Color Palettes**: Industry-specific and emotion-driven color combinations
- **HTML Content Extraction**: Automatically extract content from existing landing pages
- **Batch Processing**: Generate multiple images with different styles and configurations
- **Multi-Style Variations**: Generate the same concept in different visual styles
- **Asian Demographics**: Automatically ensures human subjects have Asian appearance

### Image Editing
- **Advanced Image Editing**: Edit existing images with natural language prompts
- **10+ Editing Templates**: Color changes, text replacement, background swapping, branding, and professional enhancement
- **Smart Editing**: AI-powered edit suggestions based on advertising copy analysis
- **Iterative Editing**: Apply sequential edits while maintaining character consistency
- **Batch Editing**: Apply multiple edits simultaneously or iteratively
- **Text Replacement**: Advanced text editing with style preservation
- **Brand Enhancement**: Logo addition, color scheme application, professional styling

### Technical Features
- **Professional CLI**: Full-featured command-line interface with comprehensive options
- **Robust API Integration**: Proper polling, error handling, and image management
- **Workflow Automation**: Pre-built workflows for common editing scenarios

## 📁 Project Structure

```
python-scripts/
├── image_generator.py          # Main CLI script (generation + editing)
├── prompt_generator.py         # Advanced prompt generation engine
├── flux_api_client.py         # Flux API integration (generation + editing)
├── visual_styles.py           # Visual style templates and configurations
├── image_editor.py            # Image editing templates and workflows
├── config.py                  # Configuration settings
├── utils.py                   # Utility functions
├── requirements.txt           # Python dependencies
├── .env.template             # Environment variables template
├── generated_images/         # Output folder for images
├── examples/                 # Sample configurations and prompts
│   ├── sample_prompts.md
│   ├── sample_configs.json
│   ├── editing_examples.md   # Comprehensive editing examples
│   └── editing_workflows.json # Pre-built editing workflows
└── README.md                 # This file
```

## 🛠️ Installation

### 1. Install Dependencies

```bash
cd python-scripts
pip install -r requirements.txt
```

### 2. Set Up API Key

Copy the environment template and add your Flux API key:

```bash
cp .env.template .env
# Edit .env file and add your BFL_API_KEY
```

### 3. Verify Installation

```bash
python image_generator.py status
```

## 🎯 Quick Start

### Generate from Text Prompt

```bash
python image_generator.py generate "Professional business meeting in modern office"
```

### Generate from Advertising Copy

```bash
python image_generator.py from-copy "Transform your business with our AI solution. Save 50% on operations costs and boost productivity by 300%. Trusted by 10,000+ companies."
```

### Extract from HTML Landing Page

```bash
python image_generator.py from-html ../MAV/01-MAV_SalesForYou.html --section hero
```

### Multiple Style Variations

```bash
python image_generator.py multi-style "Executive team collaboration" --styles high_contrast --styles negative_space
```

### Edit Existing Images

```bash
# Simple edit
python image_generator.py edit image.jpg "Change the car color to red"

# Smart editing based on copy
python image_generator.py smart-edit image.jpg "Professional consulting services. Trusted by 500+ companies." --interactive

# Text replacement
python image_generator.py replace-text image.jpg "Welcome" "Get Started"

# Template-based editing
python image_generator.py edit-template image.jpg color_change -p object=car -p new_color=blue
```

## 📖 Detailed Usage

### Command Overview

```bash
python image_generator.py --help
```

#### Image Generation Commands:

- `generate` - Generate single image from text prompt
- `from-copy` - Generate from advertising copy with analysis
- `from-html` - Extract content from HTML and generate
- `multi-style` - Generate same prompt in multiple styles
- `batch` - Process multiple prompts from file

#### Image Editing Commands:

- `edit` - Edit image with natural language prompt
- `edit-template` - Edit using predefined templates
- `replace-text` - Replace text in images
- `smart-edit` - AI-powered editing based on copy analysis
- `batch-edit` - Apply multiple edits from file
- `list-edit-templates` - Show available editing templates
- `suggest-edits` - Get edit suggestions from ad copy

#### Utility Commands:

- `list-styles` - Show available visual styles
- `list-palettes` - Show available color palettes
- `validate-image` - Validate generated image
- `status` - Show system status

### Visual Styles

#### 1. High Contrast and Vivid Colors
- **Best for**: Products, urgent offers, tech solutions
- **Formula**: Bold subject + Vibrant colors + Simple background + Sharp lighting
- **Example**: "Neon smartphone glowing against black background, cyan and magenta lighting"

#### 2. Incongruous Elements
- **Best for**: Creative services, disruptive innovations
- **Formula**: Familiar object + Surreal twist + Dreamlike context
- **Example**: "Coffee cup floating in space filled with stars, dreamlike atmosphere"

#### 3. Intense Eye Contact
- **Best for**: Personal services, trust-building
- **Formula**: Central figure + Emotive eyes + Portrait focus + Minimal distraction
- **Example**: "Professional consultant with intense gaze, cybernetic eyes glowing blue"

#### 4. Negative Space and Mystery
- **Best for**: Luxury brands, sophisticated services
- **Formula**: Minimal subject + Large empty space + Subtle emotion + Limited palette
- **Example**: "Single luxury watch floating in white void, elegant shadows"

#### 5. Hand-Drawn/Childlike
- **Best for**: Creative industries, family services
- **Formula**: Simple shapes + Imperfect lines + Playful subjects + Bright colors
- **Example**: "Crayon drawing of happy family using product, notebook paper background"

#### 6. Style Contrast (Cute + Creepy)
- **Best for**: Gaming, entertainment, unique positioning
- **Formula**: Cute character + Disturbing detail + Contrasting palette + Mood conflict
- **Example**: "Kawaii robot with glowing red eyes, candy-colored background"

### Color Palettes

#### Business/Professional
- `deep_blue_orange` - Professional yet energetic
- `navy_bright_coral` - Modern with personality
- `crimson_charcoal_silver` - Bold corporate edge

#### Technology/Digital
- `cyan_magenta` - Vibrant tech appeal
- `black_neon_green` - Gaming/tech aesthetics
- `royal_blue_neon_pink` - Edgy digital brands

#### Health/Wellness
- `sky_navy_white` - Clean healthcare feel
- `dark_teal_peach` - Fresh lifestyle vibe
- `emerald_ivory_gold` - Upscale wellness

## 🎨 Advanced Features

### Image Generation

#### Advertising Copy Analysis

The system automatically analyzes advertising copy to determine:

- **Value Proposition**: Main offering and benefits
- **Target Audience**: Business, personal, students, health, tech
- **Pain Points**: Problems mentioned in copy
- **Emotional Tone**: Urgent, aspirational, fear, excitement, trust
- **Image Purpose**: Bold offering, pain attention, end result, product pricing, click bait

#### Prompt Generation Process

1. **Copy Analysis**: Extract key components from advertising text
2. **Purpose Determination**: Decide primary image purpose
3. **Style Selection**: Choose visual style based on audience and tone
4. **Color Palette**: Select colors aligned with industry and emotion
5. **Typography**: Choose text style matching visual approach
6. **Comprehensive Assembly**: Build detailed prompt with all elements

### Image Editing

#### Editing Templates

The system includes 10+ specialized editing templates:

- **Object Modification**: Color changes, lighting improvement, resolution enhancement
- **Text Editing**: Text replacement, CTA enhancement with style preservation
- **Background Changes**: Professional backgrounds, studio settings, context switching
- **Brand Enhancement**: Logo addition, brand color application, professional styling
- **Trust Building**: Security badges, testimonials, certification logos

#### Smart Editing Features

- **AI-Powered Suggestions**: Automatic edit recommendations based on copy analysis
- **Iterative Editing**: Sequential edits that maintain character consistency
- **Batch Processing**: Apply multiple edits simultaneously or progressively
- **Industry Optimization**: Specialized edits for healthcare, tech, finance, education

#### Advanced Editing Capabilities

- **Character Consistency**: Maintain appearance across multiple edits
- **Text Style Preservation**: Replace text while keeping original formatting
- **Brand Integration**: Seamlessly add logos and brand elements
- **Professional Enhancement**: Transform casual images into business-quality photos

### Batch Processing

Create a JSON file with multiple prompts:

```json
[
  {
    "prompt": "Business automation dashboard",
    "style": "high_contrast",
    "palette": "cyan_magenta",
    "aspect_ratio": "16:9"
  },
  {
    "prompt": "Team collaboration meeting",
    "style": "eye_contact", 
    "palette": "deep_blue_orange",
    "aspect_ratio": "1:1"
  }
]
```

Then run:
```bash
python image_generator.py batch prompts.json
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```env
BFL_API_KEY=your_flux_api_key_here
API_ENDPOINT=global
DEFAULT_MODEL=flux_kontext
```

### Custom Configurations

Modify `config.py` for:

- API settings and endpoints
- Color palette definitions
- Typography styles
- File naming conventions
- Output formats and quality

## 📊 Examples and Use Cases

### E-commerce Product
```bash
python image_generator.py from-copy "Revolutionary fitness tracker with heart rate monitoring. 40% off today only. Join 100,000+ healthy users."
```

### B2B SaaS
```bash
python image_generator.py from-copy "Automate workflows and boost productivity 300%. AI-powered platform for growing teams. 14-day free trial."
```

### Educational Course
```bash
python image_generator.py from-copy "Master digital marketing in 30 days. Learn from experts, get certified, land dream job. Limited enrollment."
```

### Healthcare Service
```bash
python image_generator.py from-copy "End chronic pain naturally. Proven holistic approach, no surgery required. Book consultation today."
```

## 🛡️ Best Practices

### Image Generation

#### Prompt Quality
- Be specific about setting, lighting, and composition
- Include emotional context and desired mood
- Mention any branding elements or themes
- Consider your target audience demographics

#### Style Selection
- **High contrast**: For urgent offers and tech products
- **Negative space**: For luxury and professional services  
- **Hand-drawn**: For creative and family-oriented businesses
- **Eye contact**: For trust-building and personal services

### Image Editing

#### Editing Strategy
- **Start Simple**: Begin with basic edits before complex transformations
- **Use Templates**: Leverage predefined templates for consistent results
- **Test Iteratively**: Use smart-edit for automatic suggestions first
- **Maintain Consistency**: Use iterative editing for character-based images

#### Text Replacement Best Practices
- Use exact text as it appears in the image (case-sensitive)
- Preserve original formatting when possible
- Use quotation marks around text to be replaced
- Keep replacement text similar length to original

#### Brand Application
- Apply brand colors consistently across all elements
- Position logos in non-intrusive locations
- Maintain visual hierarchy and contrast
- Test brand elements across different backgrounds

### Batch Operations
- Group related prompts for consistency
- Use consistent style/palette for brand coherence
- Test different variations before final selection
- Organize outputs with clear naming conventions

## 🔍 Troubleshooting

### Common Issues

#### API Connection Problems
```bash
# Check system status
python image_generator.py status

# Verify API key
echo $BFL_API_KEY

# Test with different endpoint
python image_generator.py generate "test" --endpoint eu
```

#### Poor Image Quality
```bash
# Analyze your copy first
python image_generator.py from-copy "your copy" --analyze-only

# Try different styles
python image_generator.py multi-style "your prompt"

# Use more detailed prompts
python image_generator.py generate "very detailed specific prompt with lighting and composition"
```

#### Image Editing Issues
```bash
# Get edit suggestions first
python image_generator.py suggest-edits "your advertising copy"

# Use smart editing for automatic optimization
python image_generator.py smart-edit image.jpg "your copy" --interactive

# Try template-based editing for consistent results
python image_generator.py list-edit-templates
python image_generator.py edit-template image.jpg template_name -p param=value
```

#### Text Replacement Problems
```bash
# Use exact text with quotes
python image_generator.py replace-text image.jpg "Choose joy" "Choose success"

# For stylized text, describe the style
python image_generator.py edit image.jpg "Replace the decorative text 'joy' with 'success' maintaining the same artistic font style"
```

#### File Management Issues
```bash
# Validate generated images
python image_generator.py validate-image generated_images/image.jpg

# Check project structure
python image_generator.py status
```

### Error Messages

- **"API key is required"**: Set BFL_API_KEY in environment or .env file
- **"Generation failed"**: Check API credits and internet connection
- **"Invalid aspect ratio"**: Use supported ratios (3:7 to 7:3)
- **"File not found"**: Verify file paths and permissions
- **"Template not found"**: Use `list-edit-templates` to see available templates
- **"Text not found in image"**: Ensure exact text match including case and formatting

## 🔄 Integration Workflow

### Complete Landing Page Image Workflow

#### 1. Initial Image Generation
```bash
# Extract content from existing page
python image_generator.py from-html landing-page.html --section hero

# Generate initial image from advertising copy
python image_generator.py from-copy "Professional AI consulting. Transform your business with proven methodology."

# Test multiple styles for comparison
python image_generator.py multi-style "your content" --styles high_contrast --styles negative_space
```

#### 2. Smart Optimization
```bash
# Get automatic edit suggestions
python image_generator.py suggest-edits "Professional AI consulting. Transform your business."

# Apply AI-powered optimizations
python image_generator.py smart-edit generated_image.jpg "Professional AI consulting. Transform your business." --apply-all
```

#### 3. Brand Application
```bash
# Apply brand colors
python image_generator.py edit-template optimized_image.jpg brand_colors -p elements="accents" -p brand_color_scheme="company blue and orange"

# Add company logo
python image_generator.py edit-template branded_image.jpg logo_addition -p logo_description="tech company" -p position="top right"

# Enhance professional appearance
python image_generator.py edit-template logo_image.jpg professional_enhancement -p specific_changes="clean composition, business styling"
```

#### 4. Final Optimization
```bash
# Replace any text elements
python image_generator.py replace-text final_image.jpg "Contact Us" "Schedule Consultation"

# Validate final result
python image_generator.py validate-image final_optimized_image.jpg
```

### Brand Consistency Workflow

#### 1. Brand Definition
```bash
# Define brand parameters in config
# Document preferred:
# - Color schemes (2-3 combinations)
# - Visual styles (1-2 primary styles)
# - Logo specifications
# - Professional standards
```

#### 2. Template Creation
```bash
# Create brand-specific editing workflows
# Save as JSON files in examples/
# Include consistent parameters for:
# - Brand color applications
# - Logo positioning
# - Professional enhancement levels
```

#### 3. Batch Brand Application
```bash
# Apply consistent branding across multiple images
python image_generator.py batch-edit image1.jpg brand_workflow.json --iterative
python image_generator.py batch-edit image2.jpg brand_workflow.json --iterative
# Repeat for all brand images
```

#### 4. Quality Assurance
```bash
# Validate all brand images
for image in brand_images/*.jpg; do
  python image_generator.py validate-image "$image"
done

# Check brand consistency
# Review color schemes, logo placement, professional standards
```

### A/B Testing Workflow

#### 1. Create Variations
```bash
# Generate multiple CTA variations
python image_generator.py batch-edit base_image.jpg cta_variations.json

# Create different color scheme tests
python image_generator.py batch-edit base_image.jpg color_tests.json

# Test professional enhancement levels
python image_generator.py batch-edit base_image.jpg professional_levels.json
```

#### 2. Performance Tracking
```bash
# Use consistent naming for tracking
# Example: cta_test_green_button.jpg, cta_test_red_button.jpg
# Track conversion rates by filename pattern
```

### Automated Pipeline Integration

#### 1. Content Management Integration
```bash
# Extract content from CMS/HTML
python image_generator.py from-html "$CMS_EXPORT_PATH" --section hero

# Apply smart editing automatically
python image_generator.py smart-edit generated.jpg "$ADVERTISING_COPY" --apply-all
```

#### 2. CI/CD Integration
```bash
#!/bin/bash
# Automated image generation pipeline
# 1. Generate base image
python image_generator.py from-copy "$AD_COPY" --style "$BRAND_STYLE" --palette "$BRAND_PALETTE"

# 2. Apply brand consistency
python image_generator.py edit-template generated.jpg brand_colors -p elements="all" -p brand_color_scheme="$BRAND_COLORS"

# 3. Add logo
python image_generator.py edit-template branded.jpg logo_addition -p logo_description="$LOGO_DESC" -p position="top right"

# 4. Validate and deploy
python image_generator.py validate-image final.jpg && deploy_image final.jpg
```

## 📈 Performance Tips

### Generation Optimization
- Use `batch` command for multiple images to optimize API usage
- Cache successful prompts and styles for reuse
- Generate multiple aspect ratios in single batch
- Use appropriate output formats (JPEG for photos, PNG for graphics)

### Editing Optimization  
- Use `smart-edit` for automatic optimization suggestions
- Apply `batch-edit` for multiple related changes
- Use template-based editing for consistent results
- Cache successful edit templates and workflows

### Quality Assurance
- Validate images immediately after generation/editing
- Test edit templates on sample images before batch operations
- Use iterative editing for character-based images
- Maintain backup copies before applying major edits

### Workflow Efficiency
- Start with smart editing suggestions before manual edits
- Use predefined workflows for common scenarios
- Organize outputs with clear naming conventions
- Document successful configurations for reuse

## 🤝 Contributing

To extend the system:

### Image Generation Extensions
1. **Add Visual Styles**: Extend `visual_styles.py` with new style templates
2. **Add Color Palettes**: Define new palettes in `config.py`
3. **Enhance Analysis**: Improve copy analysis in `prompt_generator.py`
4. **Add Integrations**: Extend `utils.py` for new file formats or services

### Image Editing Extensions
1. **Add Editing Templates**: Create new templates in `image_editor.py`
2. **Enhance Smart Editing**: Improve AI-powered suggestions in copy analysis
3. **Add Workflows**: Define new industry-specific editing workflows
4. **Integrate Tools**: Add support for additional image processing capabilities

### System Improvements
1. **Performance**: Optimize API usage and batch processing
2. **UI/UX**: Enhance CLI interface and error handling
3. **Documentation**: Expand examples and use case coverage
4. **Testing**: Add automated testing for generation and editing functions

## 🆘 Support

For issues and questions:

1. Check this README and examples first
2. Run `python image_generator.py status` to diagnose problems
3. Review logs for detailed error information
4. Test with simple prompts to isolate issues

## 📝 License

This project is designed for landing page image generation and integrates with the Flux AI API. Ensure compliance with Flux AI terms of service for commercial usage.

---

**Happy Image Generating & Editing! 🎨✨**

Transform your landing pages with AI-powered visual content generation and professional image editing that converts visitors into customers.

## 📚 Additional Resources

- **[Editing Examples](examples/editing_examples.md)**: Comprehensive editing examples and use cases
- **[Editing Workflows](examples/editing_workflows.json)**: Pre-built workflows for common scenarios  
- **[Generation Examples](examples/sample_prompts.md)**: Generation examples and best practices
- **[Configuration Templates](examples/sample_configs.json)**: Ready-to-use configuration examples

## 🏆 Key Features Summary

✅ **Generate** professional images from advertising copy  
✅ **Edit** existing images with natural language prompts  
✅ **Smart optimization** with AI-powered suggestions  
✅ **Brand consistency** with automated color and logo application  
✅ **Batch processing** for efficient workflow automation  
✅ **Template system** for repeatable professional results  
✅ **Industry optimization** for healthcare, tech, finance, education  
✅ **Character consistency** across iterative edits  
✅ **Text replacement** with style preservation  
✅ **Complete workflows** from generation to final optimization