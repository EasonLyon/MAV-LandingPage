"""
Utility functions for file management, validation, and HTML parsing
"""
import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Union, Any
import logging

from bs4 import BeautifulSoup
from PIL import Image
import requests

from config import ProjectPaths, ImageConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileManager:
    """File management utilities"""
    
    @staticmethod
    def ensure_directory(path: Union[str, Path]) -> Path:
        """
        Ensure directory exists, create if it doesn't
        
        Args:
            path: Directory path
            
        Returns:
            Path object of the directory
        """
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @staticmethod
    def generate_filename(prefix: str = "", 
                         suffix: str = "",
                         extension: str = "jpg",
                         timestamp: bool = True) -> str:
        """
        Generate unique filename with optional timestamp
        
        Args:
            prefix: Filename prefix
            suffix: Filename suffix
            extension: File extension
            timestamp: Whether to include timestamp
            
        Returns:
            Generated filename
        """
        parts = []
        
        if prefix:
            parts.append(prefix)
        
        if timestamp:
            ts = datetime.now().strftime(ImageConfig.TIMESTAMP_FORMAT)
            parts.append(ts)
        
        if suffix:
            parts.append(suffix)
        
        filename = "_".join(parts)
        return f"{filename}.{extension}"
    
    @staticmethod
    def clean_filename(filename: str) -> str:
        """
        Clean filename by removing invalid characters
        
        Args:
            filename: Original filename
            
        Returns:
            Cleaned filename
        """
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove excessive spaces and underscores
        filename = re.sub(r'[_\s]+', '_', filename)
        # Remove leading/trailing underscores
        filename = filename.strip('_')
        return filename
    
    @staticmethod
    def get_file_size_mb(file_path: Union[str, Path]) -> float:
        """
        Get file size in megabytes
        
        Args:
            file_path: Path to file
            
        Returns:
            File size in MB
        """
        path = Path(file_path)
        if path.exists():
            return path.stat().st_size / (1024 * 1024)
        return 0.0
    
    @staticmethod
    def copy_file_with_backup(source: Union[str, Path], 
                            destination: Union[str, Path],
                            backup: bool = True) -> Path:
        """
        Copy file with optional backup of existing destination
        
        Args:
            source: Source file path
            destination: Destination file path
            backup: Whether to backup existing destination
            
        Returns:
            Path to copied file
        """
        source = Path(source)
        destination = Path(destination)
        
        # Create backup if destination exists
        if backup and destination.exists():
            backup_path = destination.with_suffix(f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}{destination.suffix}")
            shutil.copy2(destination, backup_path)
            logger.info(f"Backup created: {backup_path}")
        
        # Copy file
        shutil.copy2(source, destination)
        logger.info(f"File copied: {source} -> {destination}")
        
        return destination

class HTMLParser:
    """HTML parsing utilities for landing page content extraction"""
    
    @staticmethod
    def extract_text_from_html(html_file: Union[str, Path]) -> Dict[str, Any]:
        """
        Extract relevant text content from HTML landing page
        
        Args:
            html_file: Path to HTML file
            
        Returns:
            Dictionary with extracted content
        """
        html_file = Path(html_file)
        
        if not html_file.exists():
            raise FileNotFoundError(f"HTML file not found: {html_file}")
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract different content types
        extracted = {
            "title": HTMLParser._extract_title(soup),
            "headings": HTMLParser._extract_headings(soup),
            "paragraphs": HTMLParser._extract_paragraphs(soup),
            "cta_buttons": HTMLParser._extract_cta_buttons(soup),
            "testimonials": HTMLParser._extract_testimonials(soup),
            "features": HTMLParser._extract_features(soup),
            "pricing": HTMLParser._extract_pricing(soup),
            "meta_description": HTMLParser._extract_meta_description(soup)
        }
        
        return extracted
    
    @staticmethod
    def _extract_title(soup: BeautifulSoup) -> str:
        """Extract page title"""
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()
        
        # Fallback to h1
        h1_tag = soup.find('h1')
        if h1_tag:
            return h1_tag.get_text().strip()
        
        return ""
    
    @staticmethod
    def _extract_headings(soup: BeautifulSoup) -> List[str]:
        """Extract all headings (h1-h6)"""
        headings = []
        for level in range(1, 7):
            tags = soup.find_all(f'h{level}')
            for tag in tags:
                text = tag.get_text().strip()
                if text:
                    headings.append(text)
        return headings
    
    @staticmethod
    def _extract_paragraphs(soup: BeautifulSoup) -> List[str]:
        """Extract paragraph content"""
        paragraphs = []
        p_tags = soup.find_all('p')
        for tag in p_tags:
            text = tag.get_text().strip()
            if text and len(text) > 20:  # Filter out very short paragraphs
                paragraphs.append(text)
        return paragraphs
    
    @staticmethod
    def _extract_cta_buttons(soup: BeautifulSoup) -> List[str]:
        """Extract call-to-action button text"""
        cta_buttons = []
        
        # Look for buttons and links with CTA-like text
        button_selectors = ['button', 'a[href]', '.btn', '.button', '.cta']
        
        for selector in button_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text().strip()
                if text and any(keyword in text.lower() for keyword in 
                              ['get', 'start', 'sign', 'join', 'buy', 'order', 'download', 'contact']):
                    cta_buttons.append(text)
        
        return list(set(cta_buttons))  # Remove duplicates
    
    @staticmethod
    def _extract_testimonials(soup: BeautifulSoup) -> List[str]:
        """Extract testimonial content"""
        testimonials = []
        
        # Look for testimonial sections
        testimonial_selectors = [
            '.testimonial', '.review', '.quote', 
            '[class*="testimonial"]', '[class*="review"]'
        ]
        
        for selector in testimonial_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text().strip()
                if text and len(text) > 30:
                    testimonials.append(text)
        
        return testimonials
    
    @staticmethod
    def _extract_features(soup: BeautifulSoup) -> List[str]:
        """Extract feature lists"""
        features = []
        
        # Look for feature lists
        feature_selectors = [
            '.feature', '.benefit', '.advantage',
            '[class*="feature"]', '[class*="benefit"]',
            'ul li', 'ol li'
        ]
        
        for selector in feature_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text().strip()
                if text and 10 < len(text) < 200:  # Reasonable feature length
                    features.append(text)
        
        return features
    
    @staticmethod
    def _extract_pricing(soup: BeautifulSoup) -> List[str]:
        """Extract pricing information"""
        pricing = []
        
        # Look for pricing elements
        price_patterns = [
            r'\$\d+(?:\.\d{2})?',  # $99.99
            r'\d+\s*(?:dollar|usd|€|£)',  # 99 dollars
            r'free',  # Free
            r'\d+%\s*off'  # 50% off
        ]
        
        text_content = soup.get_text()
        for pattern in price_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            pricing.extend(matches)
        
        return list(set(pricing))
    
    @staticmethod
    def _extract_meta_description(soup: BeautifulSoup) -> str:
        """Extract meta description"""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            return meta_desc.get('content', '').strip()
        return ""
    
    @staticmethod
    def consolidate_content_for_prompt(extracted_content: Dict[str, Any]) -> str:
        """
        Consolidate extracted HTML content into advertising copy for prompt generation
        
        Args:
            extracted_content: Dictionary from extract_text_from_html()
            
        Returns:
            Consolidated advertising copy text
        """
        ad_copy_parts = []
        
        # Add title/main heading
        if extracted_content.get("title"):
            ad_copy_parts.append(extracted_content["title"])
        
        # Add primary headings
        headings = extracted_content.get("headings", [])
        if headings:
            ad_copy_parts.extend(headings[:3])  # Top 3 headings
        
        # Add key paragraphs (shorter ones likely to be value props)
        paragraphs = extracted_content.get("paragraphs", [])
        key_paragraphs = [p for p in paragraphs if 50 < len(p) < 300][:2]
        ad_copy_parts.extend(key_paragraphs)
        
        # Add features/benefits
        features = extracted_content.get("features", [])
        if features:
            ad_copy_parts.append("Key benefits: " + "; ".join(features[:5]))
        
        # Add CTA
        cta_buttons = extracted_content.get("cta_buttons", [])
        if cta_buttons:
            ad_copy_parts.append(f"Call to action: {cta_buttons[0]}")
        
        # Add pricing if available
        pricing = extracted_content.get("pricing", [])
        if pricing:
            ad_copy_parts.append(f"Pricing: {', '.join(pricing[:3])}")
        
        return " ".join(ad_copy_parts)

class ImageValidator:
    """Image validation and processing utilities"""
    
    @staticmethod
    def validate_image(image_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Validate image file and return metadata
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with validation results and metadata
        """
        image_path = Path(image_path)
        
        result = {
            "valid": False,
            "path": str(image_path),
            "exists": image_path.exists(),
            "size_mb": 0.0,
            "dimensions": None,
            "format": None,
            "errors": []
        }
        
        if not image_path.exists():
            result["errors"].append("File does not exist")
            return result
        
        try:
            # Get file size
            result["size_mb"] = FileManager.get_file_size_mb(image_path)
            
            # Open and validate image
            with Image.open(image_path) as img:
                result["dimensions"] = img.size
                result["format"] = img.format
                result["mode"] = img.mode
                
                # Check if dimensions match expected size
                if img.size == (1024, 1024):
                    result["correct_size"] = True
                else:
                    result["correct_size"] = False
                    result["errors"].append(f"Expected 1024x1024, got {img.size}")
                
                # Check file size (reasonable range for 1024x1024)
                if result["size_mb"] > 10:
                    result["errors"].append(f"File size too large: {result['size_mb']:.2f}MB")
                
                result["valid"] = len(result["errors"]) == 0
                
        except Exception as e:
            result["errors"].append(f"Image validation error: {str(e)}")
        
        return result
    
    @staticmethod
    def resize_image(image_path: Union[str, Path], 
                    target_size: tuple = (1024, 1024),
                    output_path: Union[str, Path] = None,
                    quality: int = 85) -> Path:
        """
        Resize image to target dimensions
        
        Args:
            image_path: Source image path
            target_size: Target dimensions (width, height)
            output_path: Output path (defaults to modified original)
            quality: JPEG quality (1-100)
            
        Returns:
            Path to resized image
        """
        image_path = Path(image_path)
        
        if not output_path:
            output_path = image_path.parent / f"{image_path.stem}_resized{image_path.suffix}"
        else:
            output_path = Path(output_path)
        
        with Image.open(image_path) as img:
            # Resize with high-quality resampling
            resized = img.resize(target_size, Image.Resampling.LANCZOS)
            
            # Save with appropriate format and quality
            if output_path.suffix.lower() in ['.jpg', '.jpeg']:
                resized.save(output_path, 'JPEG', quality=quality, optimize=True)
            else:
                resized.save(output_path, optimize=True)
        
        logger.info(f"Image resized: {image_path} -> {output_path} ({target_size})")
        return output_path

class ConfigManager:
    """Configuration management utilities"""
    
    @staticmethod
    def load_config_file(config_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Load configuration from JSON file
        
        Args:
            config_path: Path to config file
            
        Returns:
            Configuration dictionary
        """
        config_path = Path(config_path)
        
        if not config_path.exists():
            logger.warning(f"Config file not found: {config_path}")
            return {}
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {str(e)}")
            return {}
    
    @staticmethod
    def save_config_file(config: Dict[str, Any], config_path: Union[str, Path]) -> bool:
        """
        Save configuration to JSON file
        
        Args:
            config: Configuration dictionary
            config_path: Path to save config
            
        Returns:
            True if successful, False otherwise
        """
        config_path = Path(config_path)
        
        try:
            # Ensure directory exists
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Config saved: {config_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save config: {str(e)}")
            return False
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        Basic validation of API key format
        
        Args:
            api_key: API key to validate
            
        Returns:
            True if format appears valid
        """
        if not api_key or not isinstance(api_key, str):
            return False
        
        # Basic format checks
        if len(api_key) < 10:
            return False
        
        # Check for common patterns (this is basic validation)
        if api_key.startswith(('sk-', 'bfl-')):
            return True
        
        # Allow other formats but warn
        logger.warning("API key format not recognized but proceeding")
        return True

class ProgressTracker:
    """Progress tracking for batch operations"""
    
    def __init__(self, total: int, description: str = "Processing"):
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = datetime.now()
    
    def update(self, increment: int = 1):
        """Update progress by increment"""
        self.current = min(self.current + increment, self.total)
        self._log_progress()
    
    def _log_progress(self):
        """Log current progress"""
        percentage = (self.current / self.total) * 100 if self.total > 0 else 0
        elapsed = datetime.now() - self.start_time
        
        if self.current < self.total and self.current > 0:
            # Estimate remaining time
            time_per_item = elapsed.total_seconds() / self.current
            remaining_items = self.total - self.current
            eta_seconds = time_per_item * remaining_items
            eta = f" (ETA: {int(eta_seconds)}s)"
        else:
            eta = ""
        
        logger.info(f"{self.description}: {self.current}/{self.total} ({percentage:.1f}%){eta}")
    
    def finish(self):
        """Mark as finished"""
        self.current = self.total
        elapsed = datetime.now() - self.start_time
        logger.info(f"{self.description} completed in {elapsed.total_seconds():.1f}s")

# Convenience functions
def extract_landing_page_content(html_file: Union[str, Path]) -> str:
    """
    Quick function to extract and consolidate landing page content
    
    Args:
        html_file: Path to HTML landing page
        
    Returns:
        Consolidated advertising copy
    """
    extracted = HTMLParser.extract_text_from_html(html_file)
    return HTMLParser.consolidate_content_for_prompt(extracted)

def validate_project_structure() -> Dict[str, bool]:
    """
    Validate that project structure is correct
    
    Returns:
        Dictionary with validation results
    """
    checks = {
        "python_scripts_dir": ProjectPaths.PYTHON_SCRIPTS_DIR.exists(),
        "generated_images_dir": ProjectPaths.GENERATED_IMAGES_DIR.exists(),
        "examples_dir": ProjectPaths.EXAMPLES_DIR.exists(),
        "project_root": ProjectPaths.PROJECT_ROOT.exists(),
        "config_readable": True,  # Basic check
    }
    
    # Check if critical files exist
    critical_files = [
        "config.py", "visual_styles.py", "flux_api_client.py", 
        "prompt_generator.py", "requirements.txt"
    ]
    
    for file in critical_files:
        file_path = ProjectPaths.PYTHON_SCRIPTS_DIR / file
        checks[f"{file}_exists"] = file_path.exists()
    
    return checks