#!/usr/bin/env python3
"""
Main CLI Script for Landing Page Image Generation
Comprehensive image generation system using Flux API with advanced prompt generation
"""
import click
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import our modules
try:
    from config import FluxConfig, ColorPalettes, ProjectPaths
    from flux_api_client import FluxAPIClient, quick_generate, batch_generate_styles, quick_edit, batch_edit_variations
    from prompt_generator import AdvancedPromptGenerator, quick_prompt_from_copy, analyze_copy_only
    from visual_styles import VisualStyleSelector
    from image_editor import LandingPageImageEditor, ImageEditingWorkflows, get_editor, suggest_edits, build_edit_prompt
    from utils import (
        HTMLParser, extract_landing_page_content, 
        FileManager, ImageValidator, ProgressTracker,
        validate_project_structure
    )
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    sys.exit(1)

@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--api-key', help='Override API key from environment')
@click.option('--endpoint', default='global', help='API endpoint to use (global, eu, us)')
@click.pass_context
def cli(ctx, verbose, api_key, endpoint):
    """
    Landing Page Image Generator
    
    Generate high-quality images for landing pages using Flux AI with advanced prompt generation.
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Store common options in context
    ctx.ensure_object(dict)
    ctx.obj['api_key'] = api_key
    ctx.obj['endpoint'] = endpoint
    
    # Validate project structure
    validation = validate_project_structure()
    missing = [k for k, v in validation.items() if not v]
    if missing:
        logger.warning(f"Project structure issues: {missing}")

@cli.command()
@click.argument('prompt', type=str)
@click.option('--style', '-s', type=click.Choice(VisualStyleSelector.get_style_names()), 
              help='Visual style to apply')
@click.option('--palette', '-p', type=click.Choice(ColorPalettes.list_palettes()),
              help='Color palette to use')
@click.option('--output', '-o', type=click.Path(), help='Output directory')
@click.option('--filename', '-f', help='Custom filename')
@click.option('--aspect-ratio', '-ar', default='1:1', help='Image aspect ratio')
@click.option('--seed', type=int, help='Seed for reproducibility')
@click.pass_context
def generate(ctx, prompt, style, palette, output, filename, aspect_ratio, seed):
    """
    Generate a single image from a text prompt
    
    Example:
        python image_generator.py generate "A professional business person using a laptop"
    """
    try:
        # Initialize client
        client = FluxAPIClient(
            api_key=ctx.obj.get('api_key'),
            endpoint=ctx.obj.get('endpoint')
        )
        
        # Set output directory
        output_dir = Path(output) if output else ProjectPaths.GENERATED_IMAGES_DIR
        
        # Generate enhanced prompt if style is specified
        if style:
            style_info = VisualStyleSelector.get_style(style)
            if style_info:
                enhanced_prompt = f"{prompt}, {style_info['formula'].lower()}"
                prompt = enhanced_prompt
                logger.info(f"Applied style: {style}")
        
        # Build generation parameters
        gen_params = {
            'aspect_ratio': aspect_ratio,
            'preferred_palette': palette
        }
        
        if seed:
            gen_params['seed'] = seed
        
        logger.info(f"Generating image with prompt: {prompt[:100]}...")
        
        # Generate and download image
        result = client.generate_and_download(
            prompt=prompt,
            filename=filename,
            directory=output_dir,
            **gen_params
        )
        
        if result['status'] == 'completed':
            click.echo(f"✅ Image generated successfully!")
            click.echo(f"📁 Saved to: {result['local_path']}")
            click.echo(f"🔗 Original URL: {result['image_url']}")
        else:
            click.echo(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        click.echo(f"❌ Error: {str(e)}")
        sys.exit(1)

@cli.command()
@click.argument('ad_copy', type=str)
@click.option('--style', '-s', type=click.Choice(VisualStyleSelector.get_style_names()),
              help='Override automatic style selection')
@click.option('--palette', '-p', type=click.Choice(ColorPalettes.list_palettes()),
              help='Override automatic palette selection')
@click.option('--output', '-o', type=click.Path(), help='Output directory')
@click.option('--analyze-only', is_flag=True, help='Only analyze copy without generating image')
@click.option('--show-prompt', is_flag=True, help='Show generated prompt')
@click.pass_context
def from_copy(ctx, ad_copy, style, palette, output, analyze_only, show_prompt):
    """
    Generate image from advertising copy with advanced analysis
    
    Example:
        python image_generator.py from-copy "Transform your business with our AI-powered solution. Save 50% on operations and boost productivity by 300%."
    """
    try:
        # Initialize prompt generator
        generator = AdvancedPromptGenerator()
        
        if analyze_only:
            # Only analyze the copy
            analysis = generator.analyze_advertising_copy(ad_copy)
            click.echo("📊 Advertising Copy Analysis:")
            click.echo(json.dumps(analysis, indent=2))
            return
        
        # Generate comprehensive prompt
        logger.info("Analyzing advertising copy...")
        full_prompt = generator.generate_comprehensive_prompt(
            ad_copy,
            preferred_style=style,
            preferred_palette=palette,
            include_text=True
        )
        
        if show_prompt:
            click.echo("🎯 Generated Prompt:")
            click.echo("-" * 50)
            click.echo(full_prompt)
            click.echo("-" * 50)
        
        # Initialize client and generate
        client = FluxAPIClient(
            api_key=ctx.obj.get('api_key'),
            endpoint=ctx.obj.get('endpoint')
        )
        
        output_dir = Path(output) if output else ProjectPaths.GENERATED_IMAGES_DIR
        
        logger.info("Generating image from analyzed copy...")
        
        result = client.generate_and_download(
            prompt=full_prompt,
            directory=output_dir
        )
        
        if result['status'] == 'completed':
            click.echo(f"✅ Image generated from advertising copy!")
            click.echo(f"📁 Saved to: {result['local_path']}")
            
            # Save analysis and prompt for reference
            analysis_file = Path(result['local_path']).with_suffix('.json')
            analysis_data = {
                'original_copy': ad_copy,
                'analysis': generator.analyze_advertising_copy(ad_copy),
                'generated_prompt': full_prompt,
                'generation_result': result
            }
            
            with open(analysis_file, 'w', encoding='utf-8') as f:
                json.dump(analysis_data, f, indent=2, ensure_ascii=False)
            
            click.echo(f"📋 Analysis saved to: {analysis_file}")
        else:
            click.echo(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Copy-based generation failed: {str(e)}")
        click.echo(f"❌ Error: {str(e)}")
        sys.exit(1)

@cli.command()
@click.argument('html_file', type=click.Path(exists=True))
@click.option('--section', type=click.Choice(['hero', 'features', 'testimonials', 'pricing']),
              help='Specific section to focus on')
@click.option('--style', '-s', type=click.Choice(VisualStyleSelector.get_style_names()),
              help='Visual style to apply')
@click.option('--output', '-o', type=click.Path(), help='Output directory')
@click.pass_context
def from_html(ctx, html_file, section, style, output):
    """
    Generate image from HTML landing page content
    
    Example:
        python image_generator.py from-html landing-page.html --section hero
    """
    try:
        html_path = Path(html_file)
        
        logger.info(f"Extracting content from: {html_path}")
        
        # Extract content from HTML
        extracted_content = HTMLParser.extract_text_from_html(html_path)
        
        # Focus on specific section if requested
        if section:
            content_map = {
                'hero': ['title', 'headings', 'cta_buttons'],
                'features': ['features', 'paragraphs'],
                'testimonials': ['testimonials'],
                'pricing': ['pricing', 'cta_buttons']
            }
            
            relevant_keys = content_map.get(section, list(extracted_content.keys()))
            filtered_content = {k: v for k, v in extracted_content.items() if k in relevant_keys}
            ad_copy = HTMLParser.consolidate_content_for_prompt(filtered_content)
        else:
            ad_copy = HTMLParser.consolidate_content_for_prompt(extracted_content)
        
        click.echo(f"📄 Extracted content: {ad_copy[:200]}...")
        
        # Generate image using from_copy logic
        ctx.invoke(from_copy, ad_copy=ad_copy, style=style, output=output, show_prompt=True)
        
    except Exception as e:
        logger.error(f"HTML-based generation failed: {str(e)}")
        click.echo(f"❌ Error: {str(e)}")
        sys.exit(1)

@cli.command()
@click.argument('base_prompt', type=str)
@click.option('--styles', '-s', multiple=True, type=click.Choice(VisualStyleSelector.get_style_names()),
              help='Specific styles to generate (default: all styles)')
@click.option('--output', '-o', type=click.Path(), help='Output directory')
@click.pass_context
def multi_style(ctx, base_prompt, styles, output):
    """
    Generate the same prompt in multiple visual styles
    
    Example:
        python image_generator.py multi-style "Professional business meeting" --styles high_contrast --styles hand_drawn
    """
    try:
        # Use all styles if none specified
        if not styles:
            styles = VisualStyleSelector.get_style_names()
        
        output_dir = Path(output) if output else ProjectPaths.GENERATED_IMAGES_DIR / "multi_style"
        output_dir.mkdir(exist_ok=True, parents=True)
        
        logger.info(f"Generating {len(styles)} variations of: {base_prompt[:50]}...")
        
        # Initialize client
        client = FluxAPIClient(
            api_key=ctx.obj.get('api_key'),
            endpoint=ctx.obj.get('endpoint')
        )
        
        # Generate prompts for each style
        prompts = []
        for style in styles:
            style_info = VisualStyleSelector.get_style(style)
            if style_info:
                enhanced_prompt = f"{base_prompt}, {style_info['formula'].lower()}"
                prompts.append({
                    'prompt': enhanced_prompt,
                    'style': style
                })
        
        # Batch generate
        progress = ProgressTracker(len(prompts), "Multi-style generation")
        results = []
        
        for i, prompt_data in enumerate(prompts):
            try:
                filename = f"{prompt_data['style']}_{i+1:02d}"
                result = client.generate_and_download(
                    prompt=prompt_data['prompt'],
                    filename=filename,
                    directory=output_dir
                )
                results.append({**result, **prompt_data})
                progress.update()
                
            except Exception as e:
                logger.error(f"Failed to generate style {prompt_data['style']}: {str(e)}")
                results.append({
                    'status': 'failed',
                    'error': str(e),
                    'style': prompt_data['style']
                })
                progress.update()
        
        progress.finish()
        
        # Report results
        successful = [r for r in results if r['status'] == 'completed']
        failed = [r for r in results if r['status'] == 'failed']
        
        click.echo(f"✅ Generated {len(successful)}/{len(results)} images successfully")
        
        if successful:
            click.echo(f"📁 Saved to: {output_dir}")
            for result in successful:
                click.echo(f"  - {result['style']}: {Path(result['local_path']).name}")
        
        if failed:
            click.echo(f"❌ Failed styles: {[r['style'] for r in failed]}")
        
    except Exception as e:
        logger.error(f"Multi-style generation failed: {str(e)}")
        click.echo(f"❌ Error: {str(e)}")
        sys.exit(1)

@cli.command()
@click.argument('prompts_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output directory')
@click.option('--concurrent', '-c', type=int, default=1, help='Number of concurrent generations')
@click.pass_context
def batch(ctx, prompts_file, output, concurrent):
    """
    Generate images from a batch file (JSON or text)
    
    Example batch.json:
    [
        {"prompt": "Business meeting", "style": "high_contrast"},
        {"prompt": "Product showcase", "style": "hand_drawn", "palette": "red_white"}
    ]
    """
    try:
        prompts_path = Path(prompts_file)
        
        # Load prompts from file
        if prompts_path.suffix.lower() == '.json':
            with open(prompts_path, 'r', encoding='utf-8') as f:
                prompts_data = json.load(f)
        else:
            # Assume text file with one prompt per line
            with open(prompts_path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
                prompts_data = [{"prompt": line} for line in lines]
        
        if not prompts_data:
            click.echo("❌ No prompts found in file")
            return
        
        output_dir = Path(output) if output else ProjectPaths.GENERATED_IMAGES_DIR / "batch"
        output_dir.mkdir(exist_ok=True, parents=True)
        
        logger.info(f"Processing {len(prompts_data)} prompts from: {prompts_path}")
        
        # Initialize client
        client = FluxAPIClient(
            api_key=ctx.obj.get('api_key'),
            endpoint=ctx.obj.get('endpoint')
        )
        
        # Process batch
        results = client.batch_generate(prompts_data, output_directory=output_dir)
        
        # Report results
        successful = [r for r in results if r['status'] == 'completed']
        failed = [r for r in results if r['status'] == 'failed']
        
        click.echo(f"✅ Batch processing completed: {len(successful)}/{len(results)} successful")
        
        if successful:
            click.echo(f"📁 Images saved to: {output_dir}")
        
        if failed:
            click.echo(f"❌ Failed prompts: {len(failed)}")
            for result in failed[:5]:  # Show first 5 failures
                click.echo(f"  - {result.get('prompt', 'Unknown')[:50]}...")
        
        # Save detailed results
        results_file = output_dir / f"batch_results_{FileManager.generate_filename()}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        click.echo(f"📋 Detailed results saved to: {results_file}")
        
    except Exception as e:
        logger.error(f"Batch generation failed: {str(e)}")
        click.echo(f"❌ Error: {str(e)}")
        sys.exit(1)

@cli.command()
def list_styles():
    """List all available visual styles"""
    styles = VisualStyleSelector.get_all_styles()
    
    click.echo("🎨 Available Visual Styles:")
    click.echo("=" * 50)
    
    for style_key, style_info in styles.items():
        click.echo(f"\n{style_key.upper()}:")
        click.echo(f"  Name: {style_info['name']}")
        click.echo(f"  Formula: {style_info['formula']}")
        
        if style_info.get('prompt_examples'):
            click.echo(f"  Example: {style_info['prompt_examples'][0][:80]}...")

@cli.command()
def list_palettes():
    """List all available color palettes"""
    palettes = ColorPalettes.PALETTES
    
    click.echo("🎨 Available Color Palettes:")
    click.echo("=" * 50)
    
    for name, palette in palettes.items():
        click.echo(f"\n{name}:")
        click.echo(f"  Colors: {palette['primary']} + {palette['secondary']}")
        if 'tertiary' in palette:
            click.echo(f"         + {palette['tertiary']}")
        click.echo(f"  Use case: {palette['description']}")

@cli.command()
@click.argument('image_path', type=click.Path(exists=True))
def validate_image(image_path):
    """Validate an image file"""
    result = ImageValidator.validate_image(image_path)
    
    click.echo(f"🔍 Image Validation Results for: {result['path']}")
    click.echo("=" * 50)
    
    if result['valid']:
        click.echo("✅ Image is valid")
    else:
        click.echo("❌ Image has issues")
    
    click.echo(f"📏 Dimensions: {result['dimensions']}")
    click.echo(f"📄 Format: {result['format']}")
    click.echo(f"💾 Size: {result['size_mb']:.2f} MB")
    click.echo(f"✔️ Correct size: {result.get('correct_size', 'Unknown')}")
    
    if result['errors']:
        click.echo("\n⚠️ Issues found:")
        for error in result['errors']:
            click.echo(f"  - {error}")

@cli.command()
def status():
    """Show system status and configuration"""
    click.echo("🔧 Image Generator Status")
    click.echo("=" * 50)
    
    # Project structure
    validation = validate_project_structure()
    click.echo(f"📁 Project structure: {'✅ OK' if all(validation.values()) else '❌ Issues'}")
    
    # API configuration
    api_key = FluxConfig.API_KEY
    click.echo(f"🔑 API Key: {'✅ Set' if api_key else '❌ Not set'}")
    
    # Directories
    click.echo(f"📂 Generated images: {ProjectPaths.GENERATED_IMAGES_DIR}")
    click.echo(f"📚 Examples: {ProjectPaths.EXAMPLES_DIR}")
    
    # Available options
    click.echo(f"🎨 Visual styles: {len(VisualStyleSelector.get_style_names())}")
    click.echo(f"🌈 Color palettes: {len(ColorPalettes.list_palettes())}")
    
    if not all(validation.values()):
        click.echo("\n⚠️ Issues detected:")
        for check, status in validation.items():
            if not status:
                click.echo(f"  - {check}: Missing")

# Image Editing Commands

@cli.command()
@click.argument('input_image', type=click.Path(exists=True))
@click.argument('edit_prompt', type=str)
@click.option('--output', '-o', type=click.Path(), help='Output directory')
@click.option('--filename', '-f', help='Custom filename')
@click.option('--aspect-ratio', '-ar', help='Aspect ratio for edited image')
@click.option('--seed', type=int, help='Seed for reproducibility')
@click.pass_context
def edit(ctx, input_image, edit_prompt, output, filename, aspect_ratio, seed):
    """
    Edit an existing image with a text prompt
    
    Example:
        python image_generator.py edit image.jpg "Change the car color to red"
    """
    try:
        # Initialize client
        client = FluxAPIClient(
            api_key=ctx.obj.get('api_key'),
            endpoint=ctx.obj.get('endpoint')
        )
        
        # Set output directory
        output_dir = Path(output) if output else ProjectPaths.GENERATED_IMAGES_DIR
        
        # Build editing parameters
        edit_params = {}
        if aspect_ratio:
            edit_params['aspect_ratio'] = aspect_ratio
        if seed:
            edit_params['seed'] = seed
        
        logger.info(f"Editing image: {input_image}")
        logger.info(f"Edit prompt: {edit_prompt}")
        
        # Edit and download image
        result = client.edit_and_download(
            prompt=edit_prompt,
            input_image=input_image,
            filename=filename,
            directory=output_dir,
            **edit_params
        )
        
        if result['status'] == 'completed':
            click.echo(f"✅ Image edited successfully!")
            click.echo(f"📁 Saved to: {result['local_path']}")
            click.echo(f"🔗 Original URL: {result['image_url']}")
        else:
            click.echo(f"❌ Editing failed: {result.get('error', 'Unknown error')}")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Image editing failed: {str(e)}")
        click.echo(f"❌ Error: {str(e)}")
        sys.exit(1)

@cli.command()
@click.argument('input_image', type=click.Path(exists=True))
@click.argument('template_name', type=str)
@click.option('--output', '-o', type=click.Path(), help='Output directory')
@click.option('--params', '-p', multiple=True, help='Template parameters (key=value)')
@click.pass_context
def edit_template(ctx, input_image, template_name, output, params):
    """
    Edit image using predefined templates
    
    Example:
        python image_generator.py edit-template image.jpg color_change -p object=car -p new_color=red
    """
    try:
        # Parse parameters
        template_params = {}
        for param in params:
            if '=' in param:
                key, value = param.split('=', 1)
                template_params[key.strip()] = value.strip()
        
        # Build edit prompt from template
        editor = get_editor()
        
        if template_name not in editor.list_templates():
            click.echo(f"❌ Template '{template_name}' not found")
            click.echo(f"Available templates: {', '.join(editor.list_templates())}")
            sys.exit(1)
        
        edit_prompt = editor.build_edit_prompt(template_name, **template_params)
        
        # Use the regular edit command
        ctx.invoke(edit, 
                  input_image=input_image, 
                  edit_prompt=edit_prompt, 
                  output=output)
        
    except Exception as e:
        logger.error(f"Template editing failed: {str(e)}")
        click.echo(f"❌ Error: {str(e)}")
        sys.exit(1)

@cli.command()
@click.argument('input_image', type=click.Path(exists=True))
@click.argument('original_text', type=str)
@click.argument('new_text', type=str)
@click.option('--output', '-o', type=click.Path(), help='Output directory')
@click.option('--preserve-style', is_flag=True, default=True, help='Preserve original text style')
@click.pass_context
def replace_text(ctx, input_image, original_text, new_text, output, preserve_style):
    """
    Replace text in an image
    
    Example:
        python image_generator.py replace-text image.jpg "Welcome" "Get Started"
    """
    try:
        editor = get_editor()
        edit_prompt = editor.optimize_text_replacement(
            original_text=original_text,
            new_text=new_text,
            preserve_style=preserve_style
        )
        
        # Use the regular edit command
        ctx.invoke(edit,
                  input_image=input_image,
                  edit_prompt=edit_prompt,
                  output=output)
        
    except Exception as e:
        logger.error(f"Text replacement failed: {str(e)}")
        click.echo(f"❌ Error: {str(e)}")
        sys.exit(1)

@cli.command()
@click.argument('input_image', type=click.Path(exists=True))
@click.argument('ad_copy', type=str)
@click.option('--output', '-o', type=click.Path(), help='Output directory')
@click.option('--apply-all', is_flag=True, help='Apply all suggested edits')
@click.option('--interactive', '-i', is_flag=True, help='Interactive selection of edits')
@click.pass_context
def smart_edit(ctx, input_image, ad_copy, output, apply_all, interactive):
    """
    Smart editing based on advertising copy analysis
    
    Example:
        python image_generator.py smart-edit image.jpg "Professional consulting services. Trusted by 500+ companies."
    """
    try:
        # Get edit suggestions
        suggestions = suggest_edits(ad_copy)
        
        if not suggestions:
            click.echo("ℹ️ No specific edit suggestions found for this copy")
            return
        
        click.echo(f"🔍 Found {len(suggestions)} edit suggestions:")
        
        selected_edits = []
        
        if interactive:
            # Interactive selection
            for i, suggestion in enumerate(suggestions):
                click.echo(f"\n{i+1}. {suggestion['description']} (Priority: {suggestion['priority']})")
                if click.confirm("Apply this edit?"):
                    selected_edits.append(suggestion)
        elif apply_all:
            # Apply all suggestions
            selected_edits = suggestions
        else:
            # Apply only high priority suggestions
            selected_edits = [s for s in suggestions if s['priority'] == 'high']
            click.echo(f"Applying {len(selected_edits)} high-priority edits...")
        
        if not selected_edits:
            click.echo("No edits selected.")
            return
        
        # Apply selected edits
        output_dir = Path(output) if output else ProjectPaths.GENERATED_IMAGES_DIR
        client = FluxAPIClient(
            api_key=ctx.obj.get('api_key'),
            endpoint=ctx.obj.get('endpoint')
        )
        
        current_image = input_image
        
        for i, edit_suggestion in enumerate(selected_edits):
            try:
                editor = get_editor()
                edit_prompt = editor.build_edit_prompt(
                    edit_suggestion['template'],
                    **edit_suggestion['parameters']
                )
                
                filename = f"smart_edit_{i+1:02d}_{edit_suggestion['template']}"
                
                result = client.edit_and_download(
                    prompt=edit_prompt,
                    input_image=current_image,
                    filename=filename,
                    directory=output_dir
                )
                
                if result['status'] == 'completed':
                    click.echo(f"✅ Applied edit {i+1}: {edit_suggestion['description']}")
                    current_image = result['local_path']  # Use edited image for next edit
                else:
                    click.echo(f"❌ Failed edit {i+1}: {result.get('error', 'Unknown error')}")
                
            except Exception as e:
                click.echo(f"❌ Error applying edit {i+1}: {str(e)}")
        
        click.echo(f"🎉 Smart editing completed! Final image: {current_image}")
        
    except Exception as e:
        logger.error(f"Smart editing failed: {str(e)}")
        click.echo(f"❌ Error: {str(e)}")
        sys.exit(1)

@cli.command()
@click.argument('input_image', type=click.Path(exists=True))
@click.argument('edits_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output directory')
@click.option('--iterative', is_flag=True, help='Apply edits iteratively (each edit builds on previous)')
@click.pass_context
def batch_edit(ctx, input_image, edits_file, output, iterative):
    """
    Apply multiple edits from a file
    
    Example edits.json:
    [
        "Change the background to white",
        "Add a professional logo in top right",
        "Make the text bold and blue"
    ]
    """
    try:
        edits_path = Path(edits_file)
        
        # Load edit prompts from file
        if edits_path.suffix.lower() == '.json':
            import json
            with open(edits_path, 'r', encoding='utf-8') as f:
                edit_prompts = json.load(f)
        else:
            # Assume text file with one edit per line
            with open(edits_path, 'r', encoding='utf-8') as f:
                edit_prompts = [line.strip() for line in f if line.strip()]
        
        if not edit_prompts:
            click.echo("❌ No edit prompts found in file")
            return
        
        output_dir = Path(output) if output else ProjectPaths.GENERATED_IMAGES_DIR / "batch_edit"
        output_dir.mkdir(exist_ok=True, parents=True)
        
        logger.info(f"Processing {len(edit_prompts)} edits from: {edits_path}")
        
        client = FluxAPIClient(
            api_key=ctx.obj.get('api_key'),
            endpoint=ctx.obj.get('endpoint')
        )
        
        if iterative:
            # Apply edits iteratively (each builds on previous)
            current_image = input_image
            results = []
            
            for i, edit_prompt in enumerate(edit_prompts):
                try:
                    filename = f"iterative_edit_{i+1:02d}"
                    result = client.edit_and_download(
                        prompt=edit_prompt,
                        input_image=current_image,
                        filename=filename,
                        directory=output_dir
                    )
                    
                    if result['status'] == 'completed':
                        results.append(result)
                        current_image = result['local_path']  # Use for next edit
                        click.echo(f"✅ Applied iterative edit {i+1}/{len(edit_prompts)}")
                    else:
                        click.echo(f"❌ Failed iterative edit {i+1}: {result.get('error', 'Unknown error')}")
                        break
                        
                except Exception as e:
                    click.echo(f"❌ Error in iterative edit {i+1}: {str(e)}")
                    break
            
            click.echo(f"🎉 Iterative editing completed! Final: {current_image}")
            
        else:
            # Apply edits independently (all from original)
            results = batch_edit_variations(input_image, edit_prompts, directory=output_dir)
            
            successful = [r for r in results if r['status'] == 'completed']
            failed = [r for r in results if r['status'] == 'failed']
            
            click.echo(f"✅ Batch editing completed: {len(successful)}/{len(results)} successful")
            
            if successful:
                click.echo(f"📁 Images saved to: {output_dir}")
            
            if failed:
                click.echo(f"❌ Failed edits: {len(failed)}")
        
    except Exception as e:
        logger.error(f"Batch editing failed: {str(e)}")
        click.echo(f"❌ Error: {str(e)}")
        sys.exit(1)

@cli.command()
def list_edit_templates():
    """List all available editing templates"""
    editor = get_editor()
    templates = editor.edit_templates
    
    click.echo("✂️ Available Editing Templates:")
    click.echo("=" * 50)
    
    for template_name, template in templates.items():
        click.echo(f"\n{template_name.upper()}:")
        click.echo(f"  Type: {template.edit_type.value}")
        click.echo(f"  Description: {template.description}")
        click.echo(f"  Template: {template.prompt_template}")
        
        if template.examples:
            click.echo(f"  Example: {template.examples[0]}")

@cli.command()
@click.argument('ad_copy', type=str)
def suggest_edits_cmd(ad_copy):
    """Suggest edits based on advertising copy"""
    try:
        suggestions = suggest_edits(ad_copy)
        
        if not suggestions:
            click.echo("ℹ️ No specific edit suggestions found for this copy")
            return
        
        click.echo("💡 Edit Suggestions:")
        click.echo("=" * 50)
        
        for i, suggestion in enumerate(suggestions, 1):
            click.echo(f"\n{i}. {suggestion['description']}")
            click.echo(f"   Priority: {suggestion['priority']}")
            click.echo(f"   Template: {suggestion['template']}")
            
            if suggestion.get('parameters'):
                click.echo("   Parameters:")
                for key, value in suggestion['parameters'].items():
                    click.echo(f"     {key}: {value}")
        
        click.echo(f"\n💡 Use 'smart-edit' command to apply these suggestions automatically!")
        
    except Exception as e:
        logger.error(f"Failed to suggest edits: {str(e)}")
        click.echo(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    cli()