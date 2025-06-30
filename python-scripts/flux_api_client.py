"""
Flux API Client with proper polling, error handling, image management, and editing capabilities
"""
import requests
import time
import os
import logging
import base64
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, Union
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO

from config import FluxConfig, ImageConfig, ProjectPaths

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FluxAPIError(Exception):
    """Custom exception for Flux API errors"""
    pass

class FluxAPIClient:
    """
    Complete Flux API client with robust error handling and image management
    """
    
    def __init__(self, api_key: str = None, endpoint: str = None):
        """
        Initialize Flux API client
        
        Args:
            api_key: BFL API key (defaults to config)
            endpoint: API endpoint to use (defaults to global)
        """
        self.api_key = api_key or FluxConfig.API_KEY
        self.endpoint = endpoint or FluxConfig.DEFAULT_ENDPOINT
        
        if not self.api_key:
            raise FluxAPIError("API key is required. Set BFL_API_KEY environment variable or pass api_key parameter.")
        
        self.base_url = FluxConfig.ENDPOINTS[self.endpoint]
        self.session = requests.Session()
        self.session.headers.update({
            'accept': 'application/json',
            'x-key': self.api_key,
            'Content-Type': 'application/json'
        })
        
        logger.info(f"Initialized Flux API client with endpoint: {self.endpoint}")

    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Make HTTP request with retry logic and proper error handling
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL
            **kwargs: Additional request parameters
            
        Returns:
            Response object
            
        Raises:
            FluxAPIError: On API errors or network issues
        """
        for attempt in range(FluxConfig.MAX_RETRIES):
            try:
                response = self.session.request(method, url, timeout=FluxConfig.REQUEST_TIMEOUT, **kwargs)
                
                if response.status_code == 429:
                    # Rate limit exceeded - exponential backoff
                    wait_time = 2 ** attempt
                    logger.warning(f"Rate limit exceeded. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                    
                elif response.status_code == 402:
                    raise FluxAPIError("Insufficient credits. Please add credits to your account.")
                    
                elif response.status_code >= 400:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                    raise FluxAPIError(error_msg)
                
                return response
                
            except requests.exceptions.RequestException as e:
                if attempt == FluxConfig.MAX_RETRIES - 1:
                    raise FluxAPIError(f"Request failed after {FluxConfig.MAX_RETRIES} attempts: {str(e)}")
                
                wait_time = 2 ** attempt
                logger.warning(f"Request failed (attempt {attempt + 1}), retrying in {wait_time}s: {str(e)}")
                time.sleep(wait_time)
        
        raise FluxAPIError(f"Failed after {FluxConfig.MAX_RETRIES} attempts")

    def generate_image(self, 
                      prompt: str,
                      model: str = None,
                      aspect_ratio: str = None,
                      seed: int = None,
                      output_format: str = None,
                      safety_tolerance: int = None,
                      prompt_upsampling: bool = False,
                      webhook_url: str = None) -> Dict[str, Any]:
        """
        Generate image using Flux API
        
        Args:
            prompt: Text description of desired image
            model: Model to use (defaults to flux_kontext)
            aspect_ratio: Image aspect ratio (defaults to 1:1)
            seed: Seed for reproducibility
            output_format: Image format (jpeg/png)
            safety_tolerance: Moderation level (0-6)
            prompt_upsampling: Whether to perform prompt upsampling
            webhook_url: URL for async completion notification
            
        Returns:
            Generation result with image URL or error details
        """
        model = model or FluxConfig.DEFAULT_MODEL
        model_endpoint = FluxConfig.MODELS.get(model, FluxConfig.MODELS["flux_kontext"])
        url = urljoin(self.base_url, model_endpoint)
        
        # Build request payload
        payload = {"prompt": prompt}
        
        if aspect_ratio:
            if aspect_ratio not in ImageConfig.ASPECT_RATIOS:
                raise FluxAPIError(f"Invalid aspect ratio. Supported: {ImageConfig.ASPECT_RATIOS}")
            payload["aspect_ratio"] = aspect_ratio
        
        if seed is not None:
            payload["seed"] = seed
            
        if output_format:
            if output_format not in ImageConfig.OUTPUT_FORMATS:
                raise FluxAPIError(f"Invalid output format. Supported: {ImageConfig.OUTPUT_FORMATS}")
            payload["output_format"] = output_format
            
        if safety_tolerance is not None:
            if not 0 <= safety_tolerance <= 6:
                raise FluxAPIError("Safety tolerance must be between 0-6")
            payload["safety_tolerance"] = safety_tolerance
            
        if prompt_upsampling:
            payload["prompt_upsampling"] = True
            
        if webhook_url:
            payload["webhook_url"] = webhook_url
        
        logger.info(f"Generating image with model: {model}")
        logger.debug(f"Request payload: {payload}")
        
        # Make initial request
        response = self._make_request("POST", url, json=payload)
        result = response.json()
        
        request_id = result.get("id")
        polling_url = result.get("polling_url")
        
        if not request_id or not polling_url:
            raise FluxAPIError(f"Invalid API response: {result}")
        
        logger.info(f"Request submitted. ID: {request_id}")
        
        # Poll for completion
        return self._poll_for_result(polling_url, request_id)

    def _poll_for_result(self, polling_url: str, request_id: str) -> Dict[str, Any]:
        """
        Poll for generation result using provided polling URL
        
        Args:
            polling_url: URL for polling status
            request_id: Request ID for tracking
            
        Returns:
            Final result with image URL or error
        """
        logger.info(f"Polling for result: {request_id}")
        
        while True:
            time.sleep(FluxConfig.POLLING_INTERVAL)
            
            try:
                response = self._make_request("GET", polling_url, params={'id': request_id})
                result = response.json()
                
                status = result.get('status')
                logger.debug(f"Status: {status}")
                
                if status == 'Ready':
                    logger.info("Generation completed successfully")
                    return result
                    
                elif status in ['Error', 'Failed']:
                    error_msg = result.get('error', 'Generation failed')
                    raise FluxAPIError(f"Generation failed: {error_msg}")
                    
                elif status in ['Pending', 'Running']:
                    # Continue polling
                    continue
                    
                else:
                    logger.warning(f"Unknown status: {status}")
                    continue
                    
            except Exception as e:
                logger.error(f"Polling error: {str(e)}")
                raise FluxAPIError(f"Polling failed: {str(e)}")

    def download_image(self, image_url: str, filename: str = None, directory: Path = None) -> Path:
        """
        Download generated image from delivery URL
        
        Args:
            image_url: URL of generated image
            filename: Custom filename (auto-generated if None)
            directory: Directory to save to (defaults to generated_images)
            
        Returns:
            Path to downloaded image file
        """
        if not image_url:
            raise FluxAPIError("Image URL is required")
        
        # Set default directory and filename
        directory = directory or ProjectPaths.GENERATED_IMAGES_DIR
        directory.mkdir(exist_ok=True, parents=True)
        
        if not filename:
            timestamp = datetime.now().strftime(ImageConfig.TIMESTAMP_FORMAT)
            extension = "jpg" if "jpeg" in image_url.lower() else "png"
            filename = f"{ImageConfig.IMAGE_PREFIX}{timestamp}.{extension}"
        
        file_path = directory / filename
        
        logger.info(f"Downloading image to: {file_path}")
        
        try:
            # Download image data
            response = requests.get(image_url, timeout=60)
            response.raise_for_status()
            
            # Save to file
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Image downloaded successfully: {file_path}")
            return file_path
            
        except Exception as e:
            raise FluxAPIError(f"Failed to download image: {str(e)}")

    def generate_and_download(self, 
                            prompt: str,
                            filename: str = None,
                            directory: Path = None,
                            **generation_kwargs) -> Dict[str, Any]:
        """
        Generate image and automatically download it
        
        Args:
            prompt: Text description of desired image
            filename: Custom filename for downloaded image
            directory: Directory to save image
            **generation_kwargs: Additional arguments for generate_image()
            
        Returns:
            Dictionary with generation result and local file path
        """
        try:
            # Generate image
            result = self.generate_image(prompt, **generation_kwargs)
            
            if result['status'] != 'Ready':
                raise FluxAPIError(f"Generation not ready: {result}")
            
            image_url = result['result']['sample']
            
            # Download image
            local_path = self.download_image(image_url, filename, directory)
            
            # Return complete result
            return {
                'status': 'completed',
                'generation_result': result,
                'local_path': str(local_path),
                'image_url': image_url,
                'prompt': prompt
            }
            
        except Exception as e:
            logger.error(f"Generation and download failed: {str(e)}")
            return {
                'status': 'failed',
                'error': str(e),
                'prompt': prompt
            }

    def encode_image_to_base64(self, image_path: Union[str, Path]) -> str:
        """
        Encode image file to base64 string for API requests
        
        Args:
            image_path: Path to image file
            
        Returns:
            Base64 encoded image string
        """
        image_path = Path(image_path)
        
        if not image_path.exists():
            raise FluxAPIError(f"Image file not found: {image_path}")
        
        try:
            # Open and validate image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary (for JPEG compatibility)
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Save to bytes buffer
                buffered = BytesIO()
                
                # Determine format based on file extension
                format = 'JPEG' if image_path.suffix.lower() in ['.jpg', '.jpeg'] else 'PNG'
                img.save(buffered, format=format, quality=90 if format == 'JPEG' else None)
                
                # Encode to base64
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                logger.debug(f"Image encoded to base64: {image_path} ({len(img_str)} chars)")
                return img_str
                
        except Exception as e:
            raise FluxAPIError(f"Failed to encode image: {str(e)}")

    def edit_image(self,
                  prompt: str,
                  input_image: Union[str, Path],
                  aspect_ratio: str = None,
                  seed: int = None,
                  output_format: str = None,
                  safety_tolerance: int = None,
                  prompt_upsampling: bool = False,
                  webhook_url: str = None) -> Dict[str, Any]:
        """
        Edit image using Flux Kontext with advanced editing capabilities
        
        Args:
            prompt: Text description of the edit to apply
            input_image: Path to input image or base64 string
            aspect_ratio: Image aspect ratio (defaults to 1:1)
            seed: Seed for reproducibility
            output_format: Image format (jpeg/png)
            safety_tolerance: Moderation level (0-2)
            prompt_upsampling: Whether to perform prompt upsampling
            webhook_url: URL for async completion notification
            
        Returns:
            Editing result with image URL or error details
        """
        model_endpoint = FluxConfig.MODELS["flux_kontext"]
        url = urljoin(self.base_url, model_endpoint)
        
        # Encode input image if it's a file path
        if isinstance(input_image, (str, Path)) and Path(input_image).exists():
            input_image_b64 = self.encode_image_to_base64(input_image)
        else:
            # Assume it's already base64 encoded
            input_image_b64 = str(input_image)
        
        # Build request payload
        payload = {
            "prompt": prompt,
            "input_image": input_image_b64
        }
        
        if aspect_ratio:
            if aspect_ratio not in ImageConfig.ASPECT_RATIOS:
                raise FluxAPIError(f"Invalid aspect ratio. Supported: {ImageConfig.ASPECT_RATIOS}")
            payload["aspect_ratio"] = aspect_ratio
        
        if seed is not None:
            payload["seed"] = seed
            
        if output_format:
            if output_format not in ImageConfig.OUTPUT_FORMATS:
                raise FluxAPIError(f"Invalid output format. Supported: {ImageConfig.OUTPUT_FORMATS}")
            payload["output_format"] = output_format
            
        if safety_tolerance is not None:
            if not 0 <= safety_tolerance <= 2:
                raise FluxAPIError("Safety tolerance must be between 0-2 for editing")
            payload["safety_tolerance"] = safety_tolerance
            
        if prompt_upsampling:
            payload["prompt_upsampling"] = True
            
        if webhook_url:
            payload["webhook_url"] = webhook_url
        
        logger.info(f"Editing image with prompt: {prompt[:100]}...")
        logger.debug(f"Request payload keys: {list(payload.keys())}")
        
        # Make initial request
        response = self._make_request("POST", url, json=payload)
        result = response.json()
        
        request_id = result.get("id")
        polling_url = result.get("polling_url")
        
        if not request_id or not polling_url:
            raise FluxAPIError(f"Invalid API response: {result}")
        
        logger.info(f"Edit request submitted. ID: {request_id}")
        
        # Poll for completion
        return self._poll_for_result(polling_url, request_id)

    def edit_and_download(self,
                         prompt: str,
                         input_image: Union[str, Path],
                         filename: str = None,
                         directory: Path = None,
                         **editing_kwargs) -> Dict[str, Any]:
        """
        Edit image and automatically download the result
        
        Args:
            prompt: Text description of the edit
            input_image: Path to input image
            filename: Custom filename for edited image
            directory: Directory to save edited image
            **editing_kwargs: Additional arguments for edit_image()
            
        Returns:
            Dictionary with editing result and local file path
        """
        try:
            # Edit image
            result = self.edit_image(prompt, input_image, **editing_kwargs)
            
            if result['status'] != 'Ready':
                raise FluxAPIError(f"Editing not ready: {result}")
            
            image_url = result['result']['sample']
            
            # Generate filename if not provided
            if not filename:
                input_path = Path(input_image) if isinstance(input_image, (str, Path)) else Path("edited_image")
                timestamp = datetime.now().strftime(ImageConfig.TIMESTAMP_FORMAT)
                filename = f"{input_path.stem}_edited_{timestamp}{input_path.suffix}"
            
            # Download edited image
            local_path = self.download_image(image_url, filename, directory)
            
            # Return complete result
            return {
                'status': 'completed',
                'editing_result': result,
                'local_path': str(local_path),
                'image_url': image_url,
                'prompt': prompt,
                'input_image': str(input_image)
            }
            
        except Exception as e:
            logger.error(f"Image editing and download failed: {str(e)}")
            return {
                'status': 'failed',
                'error': str(e),
                'prompt': prompt,
                'input_image': str(input_image)
            }

    def batch_generate(self, 
                      prompts: list,
                      output_directory: Path = None,
                      **generation_kwargs) -> list:
        """
        Generate multiple images in batch
        
        Args:
            prompts: List of prompt strings or prompt dictionaries
            output_directory: Directory for batch output
            **generation_kwargs: Common generation parameters
            
        Returns:
            List of generation results
        """
        output_directory = output_directory or ProjectPaths.GENERATED_IMAGES_DIR / "batch"
        output_directory.mkdir(exist_ok=True, parents=True)
        
        results = []
        
        for i, prompt_data in enumerate(prompts):
            if isinstance(prompt_data, str):
                prompt = prompt_data
                kwargs = generation_kwargs.copy()
            else:
                prompt = prompt_data.get('prompt', '')
                kwargs = {**generation_kwargs, **prompt_data}
                kwargs.pop('prompt', None)  # Remove prompt from kwargs
            
            try:
                filename = f"batch_{i+1:03d}_{datetime.now().strftime('%H%M%S')}"
                result = self.generate_and_download(
                    prompt=prompt,
                    filename=filename,
                    directory=output_directory,
                    **kwargs
                )
                results.append(result)
                logger.info(f"Batch {i+1}/{len(prompts)} completed")
                
            except Exception as e:
                error_result = {
                    'status': 'failed',
                    'error': str(e),
                    'prompt': prompt,
                    'batch_index': i
                }
                results.append(error_result)
                logger.error(f"Batch {i+1}/{len(prompts)} failed: {str(e)}")
        
        logger.info(f"Batch generation completed. Results: {len(results)}")
        return results

    def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information (if endpoint supports it)
        
        Returns:
            Account information dictionary
        """
        # This would need to be implemented based on available endpoints
        # Currently a placeholder for future functionality
        logger.warning("Account info endpoint not yet implemented")
        return {"status": "not_implemented"}

# Convenience functions for common use cases
def quick_generate(prompt: str, style: str = None, **kwargs) -> Dict[str, Any]:
    """
    Quick image generation with automatic download
    
    Args:
        prompt: Image description
        style: Visual style to apply (optional)
        **kwargs: Additional generation parameters
        
    Returns:
        Generation result with local path
    """
    client = FluxAPIClient()
    
    # Apply style modifications to prompt if specified
    if style:
        from visual_styles import VisualStyleSelector
        style_info = VisualStyleSelector.get_style(style)
        if style_info:
            # Enhance prompt with style elements
            enhanced_prompt = f"{prompt}, {style_info['formula'].lower()}"
            prompt = enhanced_prompt
    
    return client.generate_and_download(prompt, **kwargs)

def batch_generate_styles(base_prompt: str, styles: list = None, **kwargs) -> list:
    """
    Generate same prompt in multiple visual styles
    
    Args:
        base_prompt: Base image description
        styles: List of style names to apply
        **kwargs: Additional generation parameters
        
    Returns:
        List of generation results for each style
    """
    from visual_styles import VisualStyleSelector
    
    if not styles:
        styles = VisualStyleSelector.get_style_names()
    
    client = FluxAPIClient()
    prompts = []
    
    for style in styles:
        style_info = VisualStyleSelector.get_style(style)
        if style_info:
            enhanced_prompt = f"{base_prompt}, {style_info['formula'].lower()}"
            prompts.append({
                'prompt': enhanced_prompt,
                'style': style,
                **kwargs
            })
    
    return client.batch_generate(prompts)

# Convenience functions for image editing
def quick_edit(input_image: Union[str, Path], prompt: str, **kwargs) -> Dict[str, Any]:
    """
    Quick image editing with automatic download
    
    Args:
        input_image: Path to input image
        prompt: Edit description
        **kwargs: Additional editing parameters
        
    Returns:
        Editing result with local path
    """
    client = FluxAPIClient()
    return client.edit_and_download(prompt, input_image, **kwargs)

def batch_edit_variations(input_image: Union[str, Path], 
                         edit_prompts: list, 
                         **kwargs) -> list:
    """
    Apply multiple edits to the same base image
    
    Args:
        input_image: Path to input image
        edit_prompts: List of edit descriptions
        **kwargs: Additional editing parameters
        
    Returns:
        List of editing results
    """
    client = FluxAPIClient()
    results = []
    
    for i, prompt in enumerate(edit_prompts):
        try:
            filename = f"edit_variation_{i+1:02d}"
            result = client.edit_and_download(
                prompt=prompt,
                input_image=input_image,
                filename=filename,
                **kwargs
            )
            results.append(result)
            logger.info(f"Edit variation {i+1}/{len(edit_prompts)} completed")
            
        except Exception as e:
            error_result = {
                'status': 'failed',
                'error': str(e),
                'prompt': prompt,
                'input_image': str(input_image),
                'variation_index': i
            }
            results.append(error_result)
            logger.error(f"Edit variation {i+1}/{len(edit_prompts)} failed: {str(e)}")
    
    return results