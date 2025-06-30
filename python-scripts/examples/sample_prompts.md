# Sample Prompts and Use Cases

This document provides examples of how to use the image generation system with different types of landing page content.

## Basic Generation Examples

### Simple Product Showcase
```bash
python image_generator.py generate "Professional business laptop on modern desk, clean minimalist setup"
```

### Service-Based Business
```bash
python image_generator.py generate "Consultant presenting to business team" --style high_contrast
```

### Tech/Software Product
```bash
python image_generator.py generate "Modern dashboard interface on laptop screen" --style futuristic --palette cyan_magenta
```

## Advanced Copy-Based Generation

### E-commerce Product
```bash
python image_generator.py from-copy "Revolutionary fitness tracker that monitors heart rate, sleep, and activity. Save 40% today only. Transform your health journey with our award-winning technology trusted by 100,000+ users."
```

### B2B SaaS Solution
```bash
python image_generator.py from-copy "Automate your business workflows and increase productivity by 300%. Our AI-powered platform eliminates manual tasks, reduces errors, and scales with your team. Get started with a 14-day free trial."
```

### Educational/Course Content
```bash
python image_generator.py from-copy "Master digital marketing in 30 days with our comprehensive course. Learn from industry experts, get hands-on experience, and join a community of successful marketers. Limited spots available."
```

### Health/Wellness Service
```bash
python image_generator.py from-copy "End chronic pain naturally with our proven holistic approach. Thousands of patients have found relief without surgery or medication. Book your consultation today."
```

## Multi-Style Variations

Generate the same concept in different styles to see what works best:

```bash
python image_generator.py multi-style "Business person achieving success" --styles high_contrast --styles negative_space --styles hand_drawn
```

## HTML Content Extraction

Extract content from existing landing pages:

```bash
python image_generator.py from-html ../MAV/01-MAV_SalesForYou.html --section hero
python image_generator.py from-html ../WorldMasterclass/01-VinceEEC.html --section features
```

## Batch Generation

Create a batch file `batch_prompts.json`:

```json
[
  {
    "prompt": "Transform your business with AI automation",
    "style": "high_contrast",
    "palette": "deep_blue_orange"
  },
  {
    "prompt": "Achieve financial freedom through smart investing",
    "style": "negative_space",
    "palette": "emerald_ivory_gold"
  },
  {
    "prompt": "Learn new skills online from expert instructors",
    "style": "hand_drawn",
    "palette": "orange_teal_cream"
  }
]
```

Then run:
```bash
python image_generator.py batch batch_prompts.json
```

## Industry-Specific Examples

### Healthcare/Medical
- **Copy**: "Advanced medical imaging that saves lives. Our AI diagnostic tool detects diseases 50% faster than traditional methods."
- **Expected Style**: negative_space or high_contrast
- **Expected Palette**: sky_navy_white

### Real Estate
- **Copy**: "Find your dream home with our exclusive property matching service. 95% customer satisfaction rate."
- **Expected Style**: high_contrast or negative_space
- **Expected Palette**: emerald_ivory_gold

### Automotive
- **Copy**: "Experience the future of driving with our electric vehicle. Zero emissions, maximum performance."
- **Expected Style**: high_contrast
- **Expected Palette**: crimson_charcoal_silver

### Food & Restaurant
- **Copy**: "Farm-to-table dining experience. Fresh ingredients, award-winning chef, unforgettable flavors."
- **Expected Style**: hand_drawn or incongruous
- **Expected Palette**: orange_teal_cream

### Technology/Software
- **Copy**: "Next-generation cloud platform that scales infinitely. 99.9% uptime guaranteed."
- **Expected Style**: high_contrast or cute_creepy
- **Expected Palette**: cyan_magenta or black_neon_green

### Fashion/Lifestyle
- **Copy**: "Sustainable fashion that makes a statement. Eco-friendly materials, timeless designs."
- **Expected Style**: negative_space or hand_drawn
- **Expected Palette**: dark_teal_peach

## Visual Style Use Cases

### high_contrast
- **Best for**: Products that need to stand out, urgent offers, tech solutions
- **Characteristics**: Bold subjects, vivid colors, sharp lighting
- **Example**: "Revolutionary smartphone camera, neon lighting, black background"

### incongruous
- **Best for**: Creative services, disruptive innovations, attention-grabbing content
- **Characteristics**: Familiar objects with surreal twists
- **Example**: "Coffee cup floating in space filled with stars, dreamlike atmosphere"

### eye_contact
- **Best for**: Personal services, trust-building, human-centered businesses
- **Characteristics**: Direct gaze, emotional connection, portrait focus
- **Example**: "Professional consultant with intense gaze, cybernetic eyes glowing, dark background"

### negative_space
- **Best for**: Luxury brands, minimalist products, sophisticated services
- **Characteristics**: Minimal subjects, vast empty space, subtle emotions
- **Example**: "Single luxury watch on white void, minimal placement, elegant shadows"

### hand_drawn
- **Best for**: Creative industries, children's products, artisanal services
- **Characteristics**: Simple shapes, imperfect lines, bright colors
- **Example**: "Crayon drawing of happy family using product, notebook paper background"

### cute_creepy
- **Best for**: Gaming, entertainment, unique brand positioning
- **Characteristics**: Cute base with disturbing elements, mood conflict
- **Example**: "Kawaii robot with glowing red eyes, candy-colored background, stitched smile"

## Color Palette Use Cases

### Business/Professional
- `deep_blue_orange`: Professional yet energetic
- `navy_bright_coral`: Modern with personality
- `crimson_charcoal_silver`: Bold corporate edge

### Technology/Digital
- `cyan_magenta`: Vibrant tech appeal
- `black_neon_green`: Gaming/tech aesthetics
- `royal_blue_neon_pink`: Edgy digital brands

### Health/Wellness
- `sky_navy_white`: Clean healthcare feel
- `dark_teal_peach`: Fresh lifestyle vibe
- `emerald_ivory_gold`: Upscale wellness

### Creative/Lifestyle
- `hot_pink_lime`: Trendy Gen Z appeal
- `purple_neon_yellow`: Creative energy
- `orange_teal_cream`: Friendly approachable

## Tips for Best Results

1. **Be Specific**: Include details about the setting, lighting, and composition
2. **Consider Your Audience**: Match the visual style to your target demographic
3. **Test Multiple Styles**: Use multi-style generation to compare approaches
4. **Include Branding Elements**: Mention colors, themes that align with your brand
5. **Focus on Emotion**: Describe the feeling you want to convey
6. **Use Asian Demographics**: The system automatically handles this for human subjects
7. **Optimize for 1024x1024**: All images are generated in square format for maximum versatility

## Troubleshooting Common Issues

### Low Quality Results
- Make prompts more specific and detailed
- Try different visual styles
- Ensure good color palette selection

### Wrong Style for Content
- Use `--analyze-only` flag to understand how your copy is being interpreted
- Override automatic style selection with `--style` parameter
- Review style characteristics and match to your content type

### API Issues
- Verify API key is set correctly
- Check internet connection
- Try different endpoint (eu, us, global)

### File Management
- Use `status` command to check system health
- Validate images with `validate-image` command
- Organize outputs using custom directories