"""
YAML front matter parser for markdown files
"""

import yaml
from ..core.config import Config


class YAMLParser:
    """Parses YAML front matter from markdown content"""
    
    def __init__(self):
        self.student_info = {}
        self.document_info = {}
        self.university_info = {}
        self.table_labels = {}
        self.flags = {}
    
    def parse_yaml_frontmatter(self, content):
        """Parse YAML front matter from markdown content and return content without front matter"""
        lines = content.split('\n')
        
        # Check if content starts with YAML front matter
        if not lines or lines[0].strip() != '---':
            raise ValueError("YAML front matter is required! Please add a YAML header to your markdown file starting with '---'")
        
        # Find the end of YAML front matter
        yaml_end = None
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == '---':
                yaml_end = i
                break
        
        if yaml_end is None:
            raise ValueError("Malformed YAML front matter! Please ensure your YAML header ends with '---'")
        
        # Extract YAML content
        yaml_content = '\n'.join(lines[1:yaml_end])
        
        try:
            # Parse YAML
            yaml_data = yaml.safe_load(yaml_content)
            
            if not yaml_data:
                raise ValueError("Empty YAML front matter! Please provide student, document, and university information.")
            
            self._parse_student_info(yaml_data)
            self._parse_document_info(yaml_data)
            self._parse_university_info(yaml_data)
            self._parse_table_labels(yaml_data)
            self._parse_flags(yaml_data)
        
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML front matter: {e}")
        
        # Return content without YAML front matter
        return '\n'.join(lines[yaml_end + 1:])
    
    def _parse_student_info(self, yaml_data):
        """Parse student information from YAML data"""
        if 'student' not in yaml_data:
            raise ValueError("Missing 'student' section in YAML front matter!")
        
        student_data = yaml_data['student']
        
        for field in Config.REQUIRED_STUDENT_FIELDS:
            if field not in student_data:
                raise ValueError(f"Missing required student field: '{field}'")
            self.student_info[field] = str(student_data[field])
        
        for field in Config.OPTIONAL_STUDENT_FIELDS:
            if field in student_data and student_data[field] is not None:
                self.student_info[field] = str(student_data[field])
            else:
                self.student_info[field] = "UniTyLab (University Technology Lab)"  # Default
        
        print(f"📋 Loaded student info: {self.student_info['name']}")
    
    def _parse_document_info(self, yaml_data):
        """Parse document information from YAML data"""
        if 'document' not in yaml_data:
            raise ValueError("Missing 'document' section in YAML front matter!")
        
        doc_data = yaml_data['document']
        
        for field in Config.REQUIRED_DOC_FIELDS:
            if field not in doc_data:
                raise ValueError(f"Missing required document field: '{field}'")
            self.document_info[field] = str(doc_data[field])
        
        for field in Config.OPTIONAL_DOC_FIELDS:
            if field in doc_data and doc_data[field] is not None:
                self.document_info[field] = str(doc_data[field])
            else:
                self.document_info[field] = None
        
        # Handle boolean fields
        for field in Config.OPTIONAL_BOOL_FIELDS:
            if field in doc_data:
                raw_value = doc_data[field]
                self.document_info[field] = bool(raw_value)
            else:
                self.document_info[field] = False  # Default to False
        
        print(f"📄 Loaded document info: {self.document_info.get('title', 'Auto-detected')}")
    
    def _parse_flags(self, yaml_data):
        """Parse flags information from YAML data"""
        if 'flags' in yaml_data:
            flags_data = yaml_data['flags']
            
            for field in Config.OPTIONAL_FLAGS_FIELDS:
                if field in flags_data and flags_data[field] is not None:
                    self.flags[field] = bool(flags_data[field])
                else:
                    self.flags[field] = False  # Default to False
            
            print(f"🚩 Loaded flags: {sum(self.flags.values())} enabled")
            
            # Merge flags into document_info for backward compatibility
            for flag, value in self.flags.items():
                self.document_info[flag] = value
        else:
            # Initialize empty flags
            for field in Config.OPTIONAL_FLAGS_FIELDS:
                self.flags[field] = False
    
    def _parse_university_info(self, yaml_data):
        """Parse university information from YAML data"""
        if 'university' not in yaml_data:
            raise ValueError("Missing 'university' section in YAML front matter!")
        
        uni_data = yaml_data['university']
        
        for field in Config.REQUIRED_UNI_FIELDS:
            if field not in uni_data:
                raise ValueError(f"Missing required university field: '{field}'")
            self.university_info[field] = str(uni_data[field])
        
        for field in Config.OPTIONAL_UNI_FIELDS:
            if field in uni_data and uni_data[field] is not None:
                self.university_info[field] = str(uni_data[field])
            else:
                self.university_info[field] = None
        
        print(f"🏛️ Loaded university info: {self.university_info['name']}")
    
    def _parse_table_labels(self, yaml_data):
        """Parse table labels from YAML data"""
        if 'table_labels' in yaml_data:
            label_data = yaml_data['table_labels']
            
            self.table_labels = {}
            for field, default_label in Config.DEFAULT_TABLE_LABELS.items():
                if field in label_data and label_data[field] is not None:
                    self.table_labels[field] = str(label_data[field])
                else:
                    self.table_labels[field] = default_label
                    
            print(f"📋 Loaded custom table labels")
        else:
            # Use default labels
            self.table_labels = Config.DEFAULT_TABLE_LABELS.copy()