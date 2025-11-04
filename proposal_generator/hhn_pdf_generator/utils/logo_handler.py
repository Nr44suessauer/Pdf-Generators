"""
Logo download and processing utilities
"""

import os
import requests
import tempfile
from PIL import Image as PILImage
from ..core.config import Config


class LogoHandler:
    """Handles logo download and processing"""
    
    def __init__(self):
        self.hhn_logo_path = None
        self.unitylab_logo_path = None
    
    def download_logos(self):
        """Download HHN and UniTyLab logos"""
        print("Downloading logos...")
        
        # Download HHN logo
        try:
            response = requests.get(Config.HHN_LOGO_URL, timeout=10)
            response.raise_for_status()
            
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            temp_file.write(response.content)
            temp_file.close()
            self.hhn_logo_path = temp_file.name
            print("✓ HHN logo downloaded")
            
        except Exception as e:
            print(f"⚠ Warning: Could not download HHN logo: {e}")
            self.hhn_logo_path = None
        
        # Download UniTyLab logo
        try:
            response = requests.get(Config.UNITYLAB_LOGO_URL, timeout=10)
            response.raise_for_status()
            
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            temp_file.write(response.content)
            temp_file.close()
            
            # Process the UniTyLab logo to add white background
            self.unitylab_logo_path = self._process_unitylab_logo(temp_file.name)
            
            # Clean up original temp file
            os.unlink(temp_file.name)
            print("✓ UniTyLab logo downloaded and processed")
            
        except Exception as e:
            print(f"⚠ Warning: Could not download UniTyLab logo: {e}")
            print("  Creating text-based UniTyLab placeholder...")
            self.unitylab_logo_path = None
    
    def _process_unitylab_logo(self, logo_path):
        """Process UniTyLab logo to add white background"""
        try:
            # Open the PNG image
            img = PILImage.open(logo_path)
            
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Create a white background
            white_bg = PILImage.new('RGBA', img.size, (255, 255, 255, 255))
            
            # Composite the logo onto the white background
            composite = PILImage.alpha_composite(white_bg, img)
            
            # Convert back to RGB (removes transparency)
            final_img = composite.convert('RGB')
            
            # Save to a new temp file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            final_img.save(temp_file.name, 'PNG')
            temp_file.close()
            
            return temp_file.name
            
        except Exception as e:
            print(f"⚠ Warning: Could not process UniTyLab logo: {e}")
            return logo_path  # Return original if processing fails
    
    def cleanup_logos(self):
        """Clean up downloaded logo files"""
        if self.hhn_logo_path and os.path.exists(self.hhn_logo_path):
            os.unlink(self.hhn_logo_path)
        if self.unitylab_logo_path and os.path.exists(self.unitylab_logo_path):
            os.unlink(self.unitylab_logo_path)