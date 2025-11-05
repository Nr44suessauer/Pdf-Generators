"""
Text utility functions
"""

import re


def create_anchor_name(text):
    """Create a clean anchor name from heading text"""
    # Remove special characters and replace spaces with underscores
    anchor = re.sub(r'[^\w\s-]', '', text)
    anchor = re.sub(r'[-\s]+', '_', anchor)
    return anchor.lower()