"""
Configuration and constants for HHN PDF Generator
"""

from reportlab.lib.colors import Color

class Config:
    """Configuration class for HHN PDF Generator"""
    
    # Logo URLs
    HHN_LOGO_URL = "https://cdn.hs-heilbronn.de/047cbc98bf14b729/7113c7508128/v/4c6377dc113e/HHN_Logo_E_oS_RGB_300_jpg.jpg?nowebp=1"
    UNITYLAB_LOGO_URL = "https://cdn.hs-heilbronn.de/8d41ec60cab88cb6/5ee0c1617b9e/v/95877e4a7a51/8d41ec60cab88cb6-1cdc02db2ba3-UniTyLab_Logo.png"
    
    # Color scheme
    COLORS = {
        'primary': Color(0.0, 0.2, 0.4),      # HHN Dark blue
        'secondary': Color(0.6, 0.6, 0.6),    # Gray
        'accent': Color(0.0, 0.4, 0.8),       # Bright blue
        'light_gray': Color(0.9, 0.9, 0.9),   # Very light gray
        'unity_blue': Color(0.0, 0.3, 0.6)    # UniTyLab blue
    }
    
    # Default table labels
    DEFAULT_TABLE_LABELS = {
        'author': 'Author:',
        'student_id': 'Student ID:',
        'program': 'Program:',
        'faculty': 'Faculty:',
        'specialization': 'Studiengang:',
        'research_lab': 'Research Lab:',
        'supervisor': 'Supervisor:',
        'co_supervisor': 'Co-Supervisor:',
        'academic_year': 'Academic Year:',
        'submission_date': 'Submission Date:'
    }
    
    # Required YAML fields
    REQUIRED_STUDENT_FIELDS = ['name', 'student_id', 'program', 'specialization', 'supervisor', 'co_supervisor', 'academic_year']
    OPTIONAL_STUDENT_FIELDS = ['research_lab']
    REQUIRED_DOC_FIELDS = ['type', 'submission_date']
    OPTIONAL_DOC_FIELDS = ['title', 'subtitle']
    OPTIONAL_BOOL_FIELDS = ['toc_on_title_page']
    REQUIRED_UNI_FIELDS = ['name', 'subtitle', 'faculty']
    OPTIONAL_UNI_FIELDS = ['department']