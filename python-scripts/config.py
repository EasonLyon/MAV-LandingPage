"""
Configuration settings for the Image Generation System
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class FluxConfig:
    """Flux API configuration settings"""
    
    # API Configuration
    API_KEY = os.getenv("BFL_API_KEY", "")
    
    # API Endpoints
    ENDPOINTS = {
        "global": "https://api.bfl.ai",
        "eu": "https://api.eu.bfl.ai", 
        "us": "https://api.us.bfl.ai",
        "eu_single": "https://api.eu1.bfl.ai",
        "us_single": "https://api.us1.bfl.ai"
    }
    
    # Model endpoints
    MODELS = {
        "flux_pro": "/v1/flux-pro-1.1",
        "flux_kontext": "/v1/flux-kontext-pro",
        "flux_dev": "/v1/flux-dev"
    }
    
    # Default settings
    DEFAULT_ENDPOINT = "global"
    DEFAULT_MODEL = "flux_kontext"
    DEFAULT_ASPECT_RATIO = "1:1"
    DEFAULT_OUTPUT_FORMAT = "jpeg"
    SAFETY_TOLERANCE = 2
    MAX_RETRIES = 3
    POLLING_INTERVAL = 0.5  # seconds
    REQUEST_TIMEOUT = 120  # seconds

class ImageConfig:
    """Image generation and processing settings"""
    
    # Canvas and sizing
    CANVAS_SIZE = "1024x1024"
    SAFE_ZONE_PERCENTAGE = 85  # Inner safe zone for text elements
    
    # Supported aspect ratios (from 3:7 to 7:3)
    ASPECT_RATIOS = [
        "3:7", "4:7", "1:2", "9:16", "2:3", "3:4", "1:1", 
        "4:3", "3:2", "16:9", "2:1", "7:4", "7:3"
    ]
    
    # Output formats
    OUTPUT_FORMATS = ["jpeg", "png"]
    
    # File naming
    TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"
    IMAGE_PREFIX = "generated_"

class ColorPalettes:
    """Pre-defined color combinations for high-impact visuals"""
    
    PALETTES = {
        "red_white": {"primary": "#FF0000", "secondary": "#FFFFFF", "description": "Bold, urgent, great for CTAs"},
        "black_yellow": {"primary": "#000000", "secondary": "#FFFF00", "description": "High-impact for alerts"},
        "cyan_magenta": {"primary": "#00FFFF", "secondary": "#FF00FF", "description": "Vibrant for youth or tech"},
        "deep_blue_orange": {"primary": "#003366", "secondary": "#FF6600", "description": "Pro yet energetic, suits B2B"},
        "hot_pink_lime": {"primary": "#FF1493", "secondary": "#32CD32", "description": "Trendy, grabs Gen Z"},
        "purple_neon_yellow": {"primary": "#800080", "secondary": "#FFFF00", "description": "Creative, electric vibe"},
        "navy_bright_coral": {"primary": "#000080", "secondary": "#FF7F50", "description": "Modern with a pop"},
        "black_neon_green": {"primary": "#000000", "secondary": "#00FF00", "description": "Bold, tech or gaming"},
        "white_red_orange": {"primary": "#FFFFFF", "secondary": "#FF4500", "description": "Clean urgency for sales"},
        "dark_teal_peach": {"primary": "#008080", "secondary": "#FFCBA4", "description": "Fresh, stylish for lifestyle"},
        "sky_navy_white": {"primary": "#87CEEB", "secondary": "#000080", "tertiary": "#FFFFFF", "description": "Clean healthcare feel"},
        "crimson_charcoal_silver": {"primary": "#DC143C", "secondary": "#36454F", "tertiary": "#C0C0C0", "description": "Bold automotive edge"},
        "emerald_ivory_gold": {"primary": "#50C878", "secondary": "#FFFFF0", "tertiary": "#FFD700", "description": "Upscale real-estate vibe"},
        "orange_teal_cream": {"primary": "#FFA500", "secondary": "#008080", "tertiary": "#F5F5DC", "description": "Friendly education tone"},
        "royal_blue_neon_pink": {"primary": "#4169E1", "secondary": "#FF1493", "tertiary": "#000000", "description": "Edgy esports flare"}
    }
    
    @classmethod
    def get_palette(cls, name):
        """Get color palette by name"""
        return cls.PALETTES.get(name, cls.PALETTES["red_white"])
    
    @classmethod
    def list_palettes(cls):
        """List all available color palettes"""
        return list(cls.PALETTES.keys())

class TypographyStyles:
    """Typography configurations for different styles"""
    
    STYLES = {
        "fashion": {
            "description": "Trendy, sleek lines",
            "characteristics": "clean lines, minimalist",
            "effect": "white on black"
        },
        "gothic": {
            "description": "Sharp and slender strokes",
            "characteristics": "strong contrast between thick and thin lines",
            "effect": "metallic text effect with highlights and shadows"
        },
        "curved": {
            "description": "Many curves, soft elegance", 
            "characteristics": "flowing, organic shapes",
            "effect": "gradient or soft glow"
        },
        "minimalist_sans": {
            "description": "Clean, modern handwritten touch",
            "characteristics": "simple strokes, geometric",
            "effect": "subtle shadow or emboss"
        },
        "futuristic": {
            "description": "Geometric, tech-inspired",
            "characteristics": "angular, digital aesthetic",
            "effect": "neon glow or circuit texture"
        },
        "bubble": {
            "description": "Inflated, bubbly shapes",
            "characteristics": "round, playful, candy-like",
            "effect": "glossy or translucent"
        }
    }

class ProjectPaths:
    """Project directory and file paths"""
    
    # Base directories
    PROJECT_ROOT = Path(__file__).parent.parent
    PYTHON_SCRIPTS_DIR = Path(__file__).parent
    GENERATED_IMAGES_DIR = PYTHON_SCRIPTS_DIR / "generated_images"
    EXAMPLES_DIR = PYTHON_SCRIPTS_DIR / "examples"
    
    # Landing page directories  
    MAV_DIR = PROJECT_ROOT / "MAV"
    READDY_AI_DIR = PROJECT_ROOT / "ReaddyAI"
    WORLD_MASTERCLASS_DIR = PROJECT_ROOT / "WorldMasterclass"
    TEMPLATE_DIR = PROJECT_ROOT / "Template"
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.GENERATED_IMAGES_DIR.mkdir(exist_ok=True, parents=True)
        cls.EXAMPLES_DIR.mkdir(exist_ok=True, parents=True)

# Scene types for different use cases
SCENE_TYPES = {
    "situational": "Problem-solution scenes for products that solve pain points",
    "studio": "Minimalist product scenes highlighting premium design", 
    "product_focused": "E-commerce and catalog-type product displays",
    "conceptual": "Abstract scenes for intangible services like finance/education"
}

# Visual elements
VISUAL_ELEMENTS = {
    "lines": {
        "solid": "Content division, establishing order",
        "curved": "Guide the eye, soften layout, convey friendliness", 
        "diagonal": "Create dynamism and tension, sports/trendy themes",
        "dashed": "Highlight paths or processes, infographics",
        "dotted": "Light division, maintains airy feel",
        "wave": "Playful, nature-themed, ocean/beverage",
        "neon_glow": "Cyberpunk, nightclub vibe, tech feel",
        "hand_drawn": "Personalization, artisanal or childlike"
    },
    "shapes": {
        "rectangle": "Content containers, button frames",
        "circle": "Profile images, tags, focus highlights", 
        "triangle": "Directional, dynamic, arrow guides",
        "polygon": "Tech, data visualization contexts",
        "organic": "Nature, health, eco-themed designs",
        "speech_bubble": "Highlight text or price tags",
        "icons_emoji": "Convey emotions, functions, fun factor"
    }
}

# Initialize directories on import
ProjectPaths.ensure_directories()