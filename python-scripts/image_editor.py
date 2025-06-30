"""
Advanced Image Editing Templates and Helpers for Landing Page Images
Specialized editing functions for common landing page image modifications
"""
import re
from typing import Dict, List, Optional, Union, Any
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

class EditType(Enum):
    """Common types of image edits for landing pages"""
    OBJECT_MODIFICATION = "object_modification"
    TEXT_REPLACEMENT = "text_replacement"
    COLOR_CHANGE = "color_change"
    BACKGROUND_CHANGE = "background_change"
    STYLE_TRANSFER = "style_transfer"
    BRAND_ADDITION = "brand_addition"
    MOOD_ADJUSTMENT = "mood_adjustment"
    CHARACTER_CONSISTENCY = "character_consistency"

@dataclass
class EditTemplate:
    """Template for structured image editing"""
    name: str
    edit_type: EditType
    prompt_template: str
    description: str
    examples: List[str]
    best_practices: List[str]

class LandingPageImageEditor:
    """
    Specialized image editor for landing page enhancements
    """
    
    def __init__(self):
        self.edit_templates = self._initialize_templates()
    
    def _initialize_templates(self) -> Dict[str, EditTemplate]:
        """Initialize all editing templates"""
        templates = {}
        
        # Object Modification Templates
        templates["color_change"] = EditTemplate(
            name="Color Change",
            edit_type=EditType.COLOR_CHANGE,
            prompt_template="Change the {object} color to {new_color}",
            description="Change the color of specific objects in the image",
            examples=[
                "Change the car color to red",
                "Change the shirt color to blue",
                "Change the background color to white"
            ],
            best_practices=[
                "Be specific about which object to change",
                "Use standard color names or hex codes",
                "Consider color harmony with rest of image"
            ]
        )
        
        templates["background_replacement"] = EditTemplate(
            name="Background Replacement",
            edit_type=EditType.BACKGROUND_CHANGE,
            prompt_template="Replace the background with {new_background}",
            description="Replace or modify the background setting",
            examples=[
                "Replace the background with a modern office",
                "Replace the background with a clean white studio",
                "Replace the background with a professional conference room"
            ],
            best_practices=[
                "Ensure lighting matches the subject",
                "Maintain consistent perspective",
                "Choose backgrounds that support the message"
            ]
        )
        
        # Text Editing Templates
        templates["text_replacement"] = EditTemplate(
            name="Text Replacement",
            edit_type=EditType.TEXT_REPLACEMENT,
            prompt_template="Replace '{original_text}' with '{new_text}'",
            description="Replace text elements in images like signs, labels, titles",
            examples=[
                "Replace 'Welcome' with 'Get Started'",
                "Replace 'Product Name' with 'AI Solution'",
                "Replace '50% OFF' with 'LIMITED TIME'"
            ],
            best_practices=[
                "Use quotation marks around text to be replaced",
                "Match the original text case and style",
                "Keep text length similar to original"
            ]
        )
        
        templates["cta_enhancement"] = EditTemplate(
            name="CTA Enhancement",
            edit_type=EditType.TEXT_REPLACEMENT,
            prompt_template="Replace the call-to-action text with '{new_cta}' in bold, prominent style",
            description="Enhance or replace call-to-action elements",
            examples=[
                "Replace the call-to-action text with 'Start Free Trial' in bold, prominent style",
                "Replace the call-to-action text with 'Get Instant Access' in bold, prominent style",
                "Replace the call-to-action text with 'Book Consultation' in bold, prominent style"
            ],
            best_practices=[
                "Make CTAs visually prominent",
                "Use action-oriented language",
                "Ensure high contrast with background"
            ]
        )
        
        # Brand Addition Templates
        templates["logo_addition"] = EditTemplate(
            name="Logo Addition",
            edit_type=EditType.BRAND_ADDITION,
            prompt_template="Add a {logo_description} logo in the {position} corner",
            description="Add company logos or brand elements",
            examples=[
                "Add a modern tech company logo in the top right corner",
                "Add a medical clinic logo in the bottom left corner",
                "Add a consulting firm logo in the top left corner"
            ],
            best_practices=[
                "Place logos in non-intrusive locations",
                "Ensure logo size is appropriate",
                "Maintain brand consistency"
            ]
        )
        
        templates["brand_colors"] = EditTemplate(
            name="Brand Color Application",
            edit_type=EditType.COLOR_CHANGE,
            prompt_template="Apply brand colors: change {elements} to match {brand_color_scheme}",
            description="Apply brand color schemes to image elements",
            examples=[
                "Apply brand colors: change buttons and accents to match blue and orange theme",
                "Apply brand colors: change headers and highlights to match green and white theme",
                "Apply brand colors: change borders and text to match red and black theme"
            ],
            best_practices=[
                "Maintain visual hierarchy",
                "Ensure sufficient contrast",
                "Apply colors consistently"
            ]
        )
        
        # Mood and Style Templates
        templates["professional_enhancement"] = EditTemplate(
            name="Professional Enhancement",
            edit_type=EditType.MOOD_ADJUSTMENT,
            prompt_template="Make the image more professional and business-like: {specific_changes}",
            description="Enhance images to appear more professional",
            examples=[
                "Make the image more professional and business-like: cleaner background, formal attire",
                "Make the image more professional and business-like: better lighting, corporate setting",
                "Make the image more professional and business-like: remove casual elements, add business accessories"
            ],
            best_practices=[
                "Focus on clean, uncluttered aesthetics",
                "Use neutral, professional colors",
                "Ensure good lighting and composition"
            ]
        )
        
        templates["trust_building"] = EditTemplate(
            name="Trust Building Elements",
            edit_type=EditType.BRAND_ADDITION,
            prompt_template="Add trust indicators: {trust_elements}",
            description="Add elements that build trust and credibility",
            examples=[
                "Add trust indicators: security badges, certification logos",
                "Add trust indicators: customer testimonial quotes, 5-star ratings",
                "Add trust indicators: award badges, industry certifications"
            ],
            best_practices=[
                "Use recognizable trust symbols",
                "Place in prominent but non-intrusive locations",
                "Ensure authenticity and accuracy"
            ]
        )
        
        # Technical Enhancement Templates
        templates["lighting_improvement"] = EditTemplate(
            name="Lighting Improvement",
            edit_type=EditType.MOOD_ADJUSTMENT,
            prompt_template="Improve the lighting to be {lighting_style}",
            description="Enhance lighting for better visual appeal",
            examples=[
                "Improve the lighting to be bright and professional",
                "Improve the lighting to be warm and inviting",
                "Improve the lighting to be dramatic and attention-grabbing"
            ],
            best_practices=[
                "Match lighting to brand personality",
                "Ensure subject is well-lit",
                "Avoid harsh shadows on faces"
            ]
        )
        
        templates["resolution_enhancement"] = EditTemplate(
            name="Resolution Enhancement",
            edit_type=EditType.OBJECT_MODIFICATION,
            prompt_template="Enhance image quality and sharpness, make details crisp and clear",
            description="Improve overall image quality and clarity",
            examples=[
                "Enhance image quality and sharpness, make details crisp and clear",
                "Improve image resolution and remove any blur or noise",
                "Sharpen the image and enhance fine details"
            ],
            best_practices=[
                "Focus on key subject areas",
                "Maintain natural appearance",
                "Don't over-sharpen"
            ]
        )
        
        return templates
    
    def get_template(self, template_name: str) -> Optional[EditTemplate]:
        """Get editing template by name"""
        return self.edit_templates.get(template_name)
    
    def list_templates(self) -> List[str]:
        """List all available template names"""
        return list(self.edit_templates.keys())
    
    def get_templates_by_type(self, edit_type: EditType) -> List[EditTemplate]:
        """Get all templates of a specific type"""
        return [template for template in self.edit_templates.values() 
                if template.edit_type == edit_type]
    
    def build_edit_prompt(self, 
                         template_name: str, 
                         **kwargs) -> str:
        """
        Build edit prompt from template
        
        Args:
            template_name: Name of the editing template
            **kwargs: Variables to fill in the template
            
        Returns:
            Formatted editing prompt
        """
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found")
        
        try:
            return template.prompt_template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required parameter for template '{template_name}': {e}")
    
    def suggest_edits_for_copy(self, ad_copy: str) -> List[Dict[str, Any]]:
        """
        Suggest appropriate edits based on advertising copy
        
        Args:
            ad_copy: Advertising copy text
            
        Returns:
            List of suggested edit configurations
        """
        suggestions = []
        ad_copy_lower = ad_copy.lower()
        
        # Brand-focused suggestions
        if any(brand_word in ad_copy_lower for brand_word in ['brand', 'company', 'business']):
            suggestions.append({
                'template': 'logo_addition',
                'description': 'Add company logo for brand recognition',
                'priority': 'high',
                'parameters': {
                    'logo_description': 'professional company',
                    'position': 'top right'
                }
            })
        
        # Professional service suggestions
        if any(prof_word in ad_copy_lower for prof_word in ['professional', 'expert', 'consultant', 'service']):
            suggestions.append({
                'template': 'professional_enhancement',
                'description': 'Enhance professional appearance',
                'priority': 'high',
                'parameters': {
                    'specific_changes': 'formal attire, clean background, professional lighting'
                }
            })
        
        # Trust-building suggestions
        if any(trust_word in ad_copy_lower for trust_word in ['trusted', 'guaranteed', 'certified', 'secure']):
            suggestions.append({
                'template': 'trust_building',
                'description': 'Add trust indicators',
                'priority': 'medium',
                'parameters': {
                    'trust_elements': 'security badges, certification logos, testimonial quotes'
                }
            })
        
        # CTA enhancement suggestions
        if any(cta_word in ad_copy_lower for cta_word in ['get', 'start', 'join', 'buy', 'contact']):
            # Extract potential CTA text
            cta_patterns = [
                r'(get\s+\w+(?:\s+\w+)?)', r'(start\s+\w+(?:\s+\w+)?)',
                r'(join\s+\w+(?:\s+\w+)?)', r'(contact\s+\w+(?:\s+\w+)?)'
            ]
            
            for pattern in cta_patterns:
                match = re.search(pattern, ad_copy_lower)
                if match:
                    cta_text = match.group(1).title()
                    suggestions.append({
                        'template': 'cta_enhancement',
                        'description': f'Enhance CTA: {cta_text}',
                        'priority': 'high',
                        'parameters': {
                            'new_cta': cta_text
                        }
                    })
                    break
        
        # Color scheme suggestions based on industry
        industry_colors = self._detect_industry_from_copy(ad_copy_lower)
        if industry_colors:
            suggestions.append({
                'template': 'brand_colors',
                'description': f'Apply {industry_colors["industry"]} color scheme',
                'priority': 'medium',
                'parameters': {
                    'elements': 'buttons, headers, and accents',
                    'brand_color_scheme': industry_colors['colors']
                }
            })
        
        return suggestions
    
    def _detect_industry_from_copy(self, ad_copy: str) -> Optional[Dict[str, str]]:
        """Detect industry and suggest appropriate colors"""
        industry_mapping = {
            'healthcare': {
                'keywords': ['health', 'medical', 'doctor', 'clinic', 'wellness'],
                'colors': 'blue and white medical theme'
            },
            'technology': {
                'keywords': ['tech', 'software', 'app', 'digital', 'ai'],
                'colors': 'blue and orange tech theme'
            },
            'finance': {
                'keywords': ['finance', 'money', 'investment', 'bank', 'financial'],
                'colors': 'dark blue and gold financial theme'
            },
            'education': {
                'keywords': ['learn', 'course', 'education', 'training', 'teach'],
                'colors': 'orange and teal educational theme'
            },
            'creative': {
                'keywords': ['creative', 'design', 'art', 'agency', 'marketing'],
                'colors': 'purple and yellow creative theme'
            }
        }
        
        for industry, data in industry_mapping.items():
            if any(keyword in ad_copy for keyword in data['keywords']):
                return {
                    'industry': industry,
                    'colors': data['colors']
                }
        
        return None
    
    def create_iterative_edit_sequence(self, 
                                     base_edits: List[str],
                                     character_consistency: bool = True) -> List[str]:
        """
        Create a sequence of edits that build upon each other
        
        Args:
            base_edits: List of base edit descriptions
            character_consistency: Whether to maintain character consistency
            
        Returns:
            List of edit prompts designed for iterative application
        """
        sequence = []
        
        if character_consistency:
            # Add character consistency instruction to first edit
            if base_edits:
                first_edit = base_edits[0]
                enhanced_first = f"{first_edit}. Maintain character appearance and facial features for consistency in future edits."
                sequence.append(enhanced_first)
                
                # Add remaining edits with consistency reminders
                for edit in base_edits[1:]:
                    enhanced_edit = f"{edit}. Keep the same character appearance and style as previous image."
                    sequence.append(enhanced_edit)
            
        else:
            sequence = base_edits.copy()
        
        return sequence
    
    def optimize_text_replacement(self, 
                                original_text: str, 
                                new_text: str,
                                preserve_style: bool = True) -> str:
        """
        Optimize text replacement prompt for best results
        
        Args:
            original_text: Text to be replaced
            new_text: New text to insert
            preserve_style: Whether to preserve original text style
            
        Returns:
            Optimized replacement prompt
        """
        # Clean and format text
        original_clean = original_text.strip()
        new_clean = new_text.strip()
        
        # Build replacement prompt
        if preserve_style:
            prompt = f"Replace '{original_clean}' with '{new_clean}' while maintaining the same font style, size, and formatting"
        else:
            prompt = f"Replace '{original_clean}' with '{new_clean}'"
        
        # Add case matching if applicable
        if original_clean.isupper():
            prompt += f". Make '{new_clean}' uppercase to match original formatting"
        elif original_clean.istitle():
            prompt += f". Make '{new_clean}' title case to match original formatting"
        
        return prompt

class ImageEditingWorkflows:
    """Pre-defined workflows for common landing page image editing scenarios"""
    
    @staticmethod
    def brand_consistency_workflow(brand_colors: str, 
                                 logo_description: str) -> List[Dict[str, Any]]:
        """
        Workflow for applying brand consistency to images
        
        Args:
            brand_colors: Description of brand color scheme
            logo_description: Description of brand logo
            
        Returns:
            List of edit steps
        """
        return [
            {
                'step': 1,
                'template': 'brand_colors',
                'parameters': {
                    'elements': 'buttons, headers, and key elements',
                    'brand_color_scheme': brand_colors
                },
                'description': 'Apply brand color scheme'
            },
            {
                'step': 2,
                'template': 'logo_addition',
                'parameters': {
                    'logo_description': logo_description,
                    'position': 'top right'
                },
                'description': 'Add brand logo'
            },
            {
                'step': 3,
                'template': 'professional_enhancement',
                'parameters': {
                    'specific_changes': 'clean layout, consistent typography'
                },
                'description': 'Professional polish'
            }
        ]
    
    @staticmethod
    def cta_optimization_workflow(current_cta: str, 
                                new_cta: str,
                                emphasis_level: str = "high") -> List[Dict[str, Any]]:
        """
        Workflow for optimizing call-to-action elements
        
        Args:
            current_cta: Current CTA text
            new_cta: New CTA text
            emphasis_level: Level of emphasis (low, medium, high)
            
        Returns:
            List of edit steps
        """
        emphasis_styles = {
            'low': 'subtle highlighting',
            'medium': 'bold text with color accent',
            'high': 'bold, prominent style with high contrast background'
        }
        
        return [
            {
                'step': 1,
                'template': 'text_replacement',
                'parameters': {
                    'original_text': current_cta,
                    'new_text': new_cta
                },
                'description': 'Replace CTA text'
            },
            {
                'step': 2,
                'template': 'cta_enhancement',
                'parameters': {
                    'new_cta': f"{new_cta} with {emphasis_styles[emphasis_level]}"
                },
                'description': 'Enhance CTA visibility'
            }
        ]
    
    @staticmethod
    def professional_upgrade_workflow() -> List[Dict[str, Any]]:
        """
        Workflow for upgrading images to appear more professional
        
        Returns:
            List of edit steps
        """
        return [
            {
                'step': 1,
                'template': 'lighting_improvement',
                'parameters': {
                    'lighting_style': 'bright and professional'
                },
                'description': 'Improve lighting'
            },
            {
                'step': 2,
                'template': 'background_replacement',
                'parameters': {
                    'new_background': 'clean, modern office environment'
                },
                'description': 'Professional background'
            },
            {
                'step': 3,
                'template': 'professional_enhancement',
                'parameters': {
                    'specific_changes': 'formal attire, clean composition, business accessories'
                },
                'description': 'Professional styling'
            },
            {
                'step': 4,
                'template': 'resolution_enhancement',
                'parameters': {},
                'description': 'Enhance image quality'
            }
        ]

# Convenience functions
def get_editor() -> LandingPageImageEditor:
    """Get a configured image editor instance"""
    return LandingPageImageEditor()

def suggest_edits(ad_copy: str) -> List[Dict[str, Any]]:
    """Quick function to get edit suggestions from ad copy"""
    editor = get_editor()
    return editor.suggest_edits_for_copy(ad_copy)

def build_edit_prompt(template_name: str, **kwargs) -> str:
    """Quick function to build edit prompt from template"""
    editor = get_editor()
    return editor.build_edit_prompt(template_name, **kwargs)