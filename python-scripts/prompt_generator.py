"""
Advanced Prompt Generator for Landing Page Images
Implements the comprehensive prompt generation framework from the provided documentation
"""
import re
import random
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from enum import Enum

from config import ColorPalettes, TypographyStyles, VISUAL_ELEMENTS, SCENE_TYPES
from visual_styles import VisualStyleSelector, TextEffects

class ImagePurpose(Enum):
    """Different purposes for landing page images"""
    OFFERING_BOLD = "bold_offering"
    PAIN_ATTENTION = "pain_attention"
    END_RESULT = "end_result"
    PRODUCT_PRICING = "product_pricing"
    CLICK_BAIT = "click_bait"

@dataclass
class PromptComponents:
    """Structure for organizing prompt components"""
    offering: str
    image_purpose: ImagePurpose
    visual_style: str
    composition: Dict[str, Any]
    colors: Dict[str, Any]
    typography: Dict[str, Any]
    texture_effects: List[str]
    text_content: Dict[str, str]

class AdvancedPromptGenerator:
    """
    Advanced prompt generator that transforms advertising copy into 
    comprehensive image generation prompts following the detailed guidelines
    """
    
    def __init__(self):
        self.asian_demographics = [
            "Chinese", "Malay", "Indian", "Japanese", "Korean", 
            "Thai", "Vietnamese", "Filipino", "Indonesian"
        ]
    
    def analyze_advertising_copy(self, ad_copy: str) -> Dict[str, Any]:
        """
        Analyze advertising copy to extract key components
        
        Args:
            ad_copy: The advertising copy text to analyze
            
        Returns:
            Dictionary with analyzed components
        """
        analysis = {
            "value_proposition": self._extract_value_proposition(ad_copy),
            "target_audience": self._identify_target_audience(ad_copy),
            "pain_points": self._extract_pain_points(ad_copy),
            "benefits": self._extract_benefits(ad_copy),
            "offering_type": self._classify_offering(ad_copy),
            "emotional_tone": self._analyze_emotional_tone(ad_copy),
            "call_to_action": self._extract_cta(ad_copy)
        }
        return analysis
    
    def _extract_value_proposition(self, text: str) -> str:
        """Extract the main value proposition from ad copy"""
        # Look for key value indicators
        value_patterns = [
            r"save\s+\$?\d+", r"increase\s+\w+\s+by\s+\d+%",
            r"reduce\s+\w+\s+by\s+\d+%", r"get\s+\d+x\s+\w+",
            r"boost\s+your\s+\w+", r"achieve\s+\w+\s+in\s+\d+"
        ]
        
        for pattern in value_patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group()
        
        # Fallback to first sentence
        sentences = text.split('.')
        return sentences[0].strip() if sentences else text[:100]
    
    def _identify_target_audience(self, text: str) -> str:
        """Identify target audience from ad copy"""
        audience_keywords = {
            "business": ["business", "entrepreneur", "company", "enterprise", "B2B"],
            "professional": ["professional", "career", "workplace", "corporate"],
            "personal": ["personal", "individual", "family", "lifestyle"],
            "students": ["student", "learning", "education", "course"],
            "health": ["health", "fitness", "wellness", "medical"],
            "tech": ["tech", "software", "digital", "app", "platform"]
        }
        
        text_lower = text.lower()
        for audience, keywords in audience_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return audience
        
        return "general"
    
    def _extract_pain_points(self, text: str) -> List[str]:
        """Extract pain points mentioned in ad copy"""
        pain_indicators = [
            "struggle", "difficult", "hard", "challenge", "problem",
            "frustrating", "time-consuming", "expensive", "complicated",
            "stressed", "overwhelmed", "confused", "stuck"
        ]
        
        pain_points = []
        text_lower = text.lower()
        
        for indicator in pain_indicators:
            if indicator in text_lower:
                # Extract sentence containing the pain point
                sentences = text.split('.')
                for sentence in sentences:
                    if indicator in sentence.lower():
                        pain_points.append(sentence.strip())
                        break
        
        return pain_points
    
    def _extract_benefits(self, text: str) -> List[str]:
        """Extract benefits from ad copy"""
        benefit_indicators = [
            "achieve", "get", "receive", "gain", "improve", "increase",
            "boost", "enhance", "optimize", "maximize", "save", "reduce"
        ]
        
        benefits = []
        text_lower = text.lower()
        
        for indicator in benefit_indicators:
            pattern = rf"{indicator}\s+[\w\s]+(?:[.!?]|$)"
            matches = re.findall(pattern, text_lower)
            benefits.extend(matches)
        
        return benefits
    
    def _classify_offering(self, text: str) -> str:
        """Classify the type of offering"""
        offering_types = {
            "software": ["software", "app", "platform", "tool", "system"],
            "service": ["service", "consulting", "coaching", "done-for-you"],
            "course": ["course", "training", "education", "masterclass"],
            "product": ["product", "device", "equipment", "supplement"],
            "membership": ["membership", "community", "access", "subscription"]
        }
        
        text_lower = text.lower()
        for offering_type, keywords in offering_types.items():
            if any(keyword in text_lower for keyword in keywords):
                return offering_type
        
        return "service"
    
    def _analyze_emotional_tone(self, text: str) -> str:
        """Analyze emotional tone of the ad copy"""
        emotional_indicators = {
            "urgent": ["now", "today", "limited time", "hurry", "urgent", "immediate"],
            "aspirational": ["dream", "achieve", "success", "transform", "breakthrough"],
            "fear": ["miss out", "behind", "struggle", "failure", "lose"],
            "excitement": ["amazing", "incredible", "revolutionary", "game-changing"],
            "trust": ["proven", "guaranteed", "trusted", "verified", "secure"]
        }
        
        text_lower = text.lower()
        tone_scores = {}
        
        for tone, keywords in emotional_indicators.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            tone_scores[tone] = score
        
        return max(tone_scores, key=tone_scores.get) if tone_scores else "neutral"
    
    def _extract_cta(self, text: str) -> str:
        """Extract call-to-action from ad copy"""
        cta_patterns = [
            r"click\s+\w+", r"get\s+\w+\s+now", r"start\s+\w+",
            r"join\s+\w+", r"sign\s+up", r"download\s+\w+",
            r"book\s+\w+", r"schedule\s+\w+", r"contact\s+\w+"
        ]
        
        for pattern in cta_patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group()
        
        return ""
    
    def determine_image_purpose(self, analysis: Dict[str, Any]) -> ImagePurpose:
        """
        Determine the primary purpose of the image based on analysis
        
        Args:
            analysis: Analyzed advertising copy components
            
        Returns:
            ImagePurpose enum value
        """
        offering_type = analysis.get("offering_type", "service")
        emotional_tone = analysis.get("emotional_tone", "neutral")
        
        # Decision logic for image purpose
        if offering_type in ["product", "software"] and "pricing" in str(analysis):
            return ImagePurpose.PRODUCT_PRICING
        elif emotional_tone == "fear" or analysis.get("pain_points"):
            return ImagePurpose.PAIN_ATTENTION
        elif emotional_tone in ["aspirational", "excitement"]:
            return ImagePurpose.END_RESULT
        elif emotional_tone == "urgent" or "click" in analysis.get("call_to_action", ""):
            return ImagePurpose.CLICK_BAIT
        else:
            return ImagePurpose.OFFERING_BOLD
    
    def select_visual_style(self, 
                          analysis: Dict[str, Any], 
                          purpose: ImagePurpose,
                          preferred_style: str = None) -> str:
        """
        Select appropriate visual style based on analysis and purpose
        
        Args:
            analysis: Analyzed advertising copy
            purpose: Determined image purpose
            preferred_style: Override style selection
            
        Returns:
            Selected visual style name
        """
        if preferred_style and preferred_style in VisualStyleSelector.get_style_names():
            return preferred_style
        
        # Style selection logic based on purpose and analysis
        style_mapping = {
            ImagePurpose.OFFERING_BOLD: ["high_contrast", "eye_contact"],
            ImagePurpose.PAIN_ATTENTION: ["cute_creepy", "incongruous"],
            ImagePurpose.END_RESULT: ["high_contrast", "negative_space"],
            ImagePurpose.PRODUCT_PRICING: ["high_contrast", "hand_drawn"],
            ImagePurpose.CLICK_BAIT: ["incongruous", "cute_creepy"]
        }
        
        audience = analysis.get("target_audience", "general")
        
        # Audience-specific adjustments
        if audience in ["students", "personal"]:
            return "hand_drawn"
        elif audience in ["tech", "business"]:
            return "high_contrast"
        elif audience == "health":
            return "negative_space"
        
        # Default to purpose-based selection
        possible_styles = style_mapping.get(purpose, ["high_contrast"])
        return random.choice(possible_styles)
    
    def select_color_palette(self, 
                           analysis: Dict[str, Any], 
                           style: str,
                           preferred_palette: str = None) -> Dict[str, Any]:
        """
        Select appropriate color palette
        
        Args:
            analysis: Analyzed advertising copy
            style: Selected visual style
            preferred_palette: Override palette selection
            
        Returns:
            Selected color palette configuration
        """
        if preferred_palette and preferred_palette in ColorPalettes.list_palettes():
            return ColorPalettes.get_palette(preferred_palette)
        
        # Industry-specific palette selection
        audience = analysis.get("target_audience", "general")
        emotional_tone = analysis.get("emotional_tone", "neutral")
        
        palette_mapping = {
            "business": ["deep_blue_orange", "navy_bright_coral", "crimson_charcoal_silver"],
            "tech": ["cyan_magenta", "black_neon_green", "royal_blue_neon_pink"],
            "health": ["sky_navy_white", "dark_teal_peach", "emerald_ivory_gold"],
            "personal": ["hot_pink_lime", "purple_neon_yellow", "orange_teal_cream"]
        }
        
        # Emotional tone adjustments
        if emotional_tone == "urgent":
            return ColorPalettes.get_palette("red_white")
        elif emotional_tone == "trust":
            return ColorPalettes.get_palette("sky_navy_white")
        elif emotional_tone == "excitement":
            return ColorPalettes.get_palette("hot_pink_lime")
        
        # Audience-based selection
        possible_palettes = palette_mapping.get(audience, ["red_white", "black_yellow"])
        palette_name = random.choice(possible_palettes)
        return ColorPalettes.get_palette(palette_name)
    
    def select_typography(self, 
                         analysis: Dict[str, Any],
                         style: str) -> Dict[str, Any]:
        """
        Select typography style based on analysis and visual style
        
        Args:
            analysis: Analyzed advertising copy
            style: Selected visual style
            
        Returns:
            Typography configuration
        """
        audience = analysis.get("target_audience", "general")
        emotional_tone = analysis.get("emotional_tone", "neutral")
        
        # Typography mapping
        typography_mapping = {
            "business": "minimalist_sans",
            "tech": "futuristic",
            "personal": "curved",
            "students": "bubble",
            "health": "minimalist_sans"
        }
        
        # Style-specific adjustments
        if style == "hand_drawn":
            return TypographyStyles.STYLES["curved"]
        elif style == "cute_creepy":
            return TypographyStyles.STYLES["bubble"]
        elif style == "high_contrast":
            return TypographyStyles.STYLES["futuristic"]
        
        # Audience-based selection
        typography_name = typography_mapping.get(audience, "minimalist_sans")
        return TypographyStyles.STYLES.get(typography_name, TypographyStyles.STYLES["fashion"])
    
    def generate_text_content(self, 
                            analysis: Dict[str, Any],
                            purpose: ImagePurpose) -> Dict[str, str]:
        """
        Generate text content for the image based on analysis and purpose
        
        Args:
            analysis: Analyzed advertising copy
            purpose: Image purpose
            
        Returns:
            Dictionary with different text elements
        """
        offering = analysis.get("value_proposition", "")
        
        text_content = {
            "title": self._generate_title(analysis, purpose),
            "sub_headline": self._generate_sub_headline(analysis, purpose),
            "cta": analysis.get("call_to_action", "Get Started"),
            "trust_element": self._generate_trust_element(analysis)
        }
        
        return text_content
    
    def _generate_title(self, analysis: Dict[str, Any], purpose: ImagePurpose) -> str:
        """Generate main title based on offering and purpose"""
        value_prop = analysis.get("value_proposition", "")
        
        if purpose == ImagePurpose.OFFERING_BOLD:
            return value_prop or "Transform Your Business"
        elif purpose == ImagePurpose.PAIN_ATTENTION:
            pain_points = analysis.get("pain_points", [])
            if pain_points:
                return f"Stop {pain_points[0].split()[0]}..."
            return "End Your Struggles"
        elif purpose == ImagePurpose.END_RESULT:
            return "Achieve Success"
        elif purpose == ImagePurpose.PRODUCT_PRICING:
            return f"{value_prop} - Limited Time"
        else:  # CLICK_BAIT
            return "This Changes Everything"
    
    def _generate_sub_headline(self, analysis: Dict[str, Any], purpose: ImagePurpose) -> str:
        """Generate sub-headline based on benefits and features"""
        benefits = analysis.get("benefits", [])
        
        if benefits:
            return benefits[0][:50] + "..." if len(benefits[0]) > 50 else benefits[0]
        
        # Fallback based on purpose
        if purpose == ImagePurpose.PAIN_ATTENTION:
            return "Finally, a solution that works"
        elif purpose == ImagePurpose.END_RESULT:
            return "Join thousands who already succeeded"
        else:
            return "Proven system for guaranteed results"
    
    def _generate_trust_element(self, analysis: Dict[str, Any]) -> str:
        """Generate trust/social proof element"""
        trust_elements = [
            "30-Day Money Back Guarantee",
            "Join 10,000+ Happy Customers",
            "Trusted by Industry Leaders",
            "Verified Results",
            "Risk-Free Trial"
        ]
        return random.choice(trust_elements)
    
    def ensure_asian_appearance(self, prompt: str, style: str) -> str:
        """
        Ensure human subjects have Asian appearance as specified
        
        Args:
            prompt: Current prompt text
            style: Visual style being used
            
        Returns:
            Modified prompt with Asian appearance specification
        """
        # Check if prompt involves human subjects
        human_indicators = ["person", "woman", "man", "girl", "boy", "child", "face", "portrait"]
        
        if any(indicator in prompt.lower() for indicator in human_indicators):
            asian_demo = random.choice(self.asian_demographics)
            age_gender = random.choice(["young woman", "young man", "child", "adult"])
            
            # Insert Asian appearance specification
            asian_spec = f"{asian_demo} {age_gender}"
            
            # Replace generic human references
            for indicator in human_indicators:
                if indicator in prompt.lower():
                    prompt = re.sub(rf'\b{indicator}\b', asian_spec, prompt, count=1, flags=re.IGNORECASE)
                    break
        
        return prompt
    
    def generate_comprehensive_prompt(self, 
                                    ad_copy: str,
                                    preferred_style: str = None,
                                    preferred_palette: str = None,
                                    include_text: bool = True,
                                    custom_elements: Dict[str, Any] = None) -> str:
        """
        Generate comprehensive image prompt from advertising copy
        
        Args:
            ad_copy: The advertising copy to analyze
            preferred_style: Override style selection
            preferred_palette: Override color palette
            include_text: Whether to include text elements in image
            custom_elements: Custom elements to include
            
        Returns:
            Complete image generation prompt
        """
        # Step 1: Analyze advertising copy
        analysis = self.analyze_advertising_copy(ad_copy)
        
        # Step 2: Determine image purpose
        purpose = self.determine_image_purpose(analysis)
        
        # Step 3: Select visual style
        style = self.select_visual_style(analysis, purpose, preferred_style)
        
        # Step 4: Select color palette
        color_palette = self.select_color_palette(analysis, style, preferred_palette)
        
        # Step 5: Select typography
        typography = self.select_typography(analysis, style)
        
        # Step 6: Generate text content
        text_content = self.generate_text_content(analysis, purpose) if include_text else {}
        
        # Step 7: Build comprehensive prompt
        prompt_parts = []
        
        # Add offering description
        offering = analysis.get("value_proposition", "business solution")
        prompt_parts.append(f"**The Offering:** {offering}")
        
        # Add image description with purpose
        purpose_descriptions = {
            ImagePurpose.OFFERING_BOLD: "Bold presentation of the offering",
            ImagePurpose.PAIN_ATTENTION: "Attention-grabbing focus on audience's pain points",
            ImagePurpose.END_RESULT: "Direct visualization of desired end results",
            ImagePurpose.PRODUCT_PRICING: "Product showcase with pricing emphasis",
            ImagePurpose.CLICK_BAIT: "Click-bait trigger to generate interest"
        }
        
        image_desc = purpose_descriptions[purpose]
        prompt_parts.append(f"**Image Description:** This image illustrates the offering through {image_desc}")
        
        # Add visual style
        style_info = VisualStyleSelector.get_style(style)
        if style_info:
            prompt_parts.append(f"**Visual Style:** {style_info['name']}")
            prompt_parts.append(f"Style Formula: {style_info['formula']}")
        
        # Add composition details
        prompt_parts.append("**Composition Details:**")
        prompt_parts.append("- Canvas Size: Exactly 1024x1024 pixels (1:1 square aspect ratio)")
        prompt_parts.append("- Visual Hierarchy: Balanced design with focal points centered")
        prompt_parts.append("- Safe Zones: Key text elements within inner 85% of frame")
        
        # Add color instructions
        prompt_parts.append(f"**Color Instructions:** {color_palette['description']}")
        prompt_parts.append(f"Primary: {color_palette['primary']}, Secondary: {color_palette['secondary']}")
        if 'tertiary' in color_palette:
            prompt_parts.append(f"Tertiary: {color_palette['tertiary']}")
        
        # Add typography and text
        if include_text and text_content:
            prompt_parts.append("**Typography & Text Placement:**")
            prompt_parts.append(f"Typography Style: {typography['description']}")
            prompt_parts.append("**Text to Include:**")
            
            for text_type, content in text_content.items():
                if content:
                    prompt_parts.append(f"- {text_type.replace('_', ' ').title()}: {content}")
        
        # Add texture & effects
        if style in ["high_contrast", "cute_creepy"]:
            effects = ["glow", "3d", "metal"]
        elif style == "hand_drawn":
            effects = ["cartoon", "blur"]
        else:
            effects = ["gradient", "embossed"]
        
        prompt_parts.append("**Texture & Effects:**")
        prompt_parts.append(f"Apply {', '.join(effects)} effects aligned with the offering's style")
        
        # Combine all parts
        full_prompt = "\n\n".join(prompt_parts)
        
        # Ensure Asian appearance for human subjects
        full_prompt = self.ensure_asian_appearance(full_prompt, style)
        
        # Add custom elements if provided
        if custom_elements:
            custom_section = "\n\n**Custom Elements:**\n"
            for key, value in custom_elements.items():
                custom_section += f"- {key}: {value}\n"
            full_prompt += custom_section
        
        return full_prompt

# Convenience functions
def quick_prompt_from_copy(ad_copy: str, style: str = None) -> str:
    """
    Quick prompt generation from advertising copy
    
    Args:
        ad_copy: Advertising copy text
        style: Preferred visual style (optional)
        
    Returns:
        Generated prompt string
    """
    generator = AdvancedPromptGenerator()
    return generator.generate_comprehensive_prompt(ad_copy, preferred_style=style)

def analyze_copy_only(ad_copy: str) -> Dict[str, Any]:
    """
    Analyze advertising copy without generating prompt
    
    Args:
        ad_copy: Advertising copy text
        
    Returns:
        Analysis results dictionary
    """
    generator = AdvancedPromptGenerator()
    return generator.analyze_advertising_copy(ad_copy)