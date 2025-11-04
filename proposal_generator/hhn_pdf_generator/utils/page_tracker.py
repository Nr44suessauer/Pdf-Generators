"""
Custom flowables for page tracking
"""

from reportlab.platypus.flowables import Flowable


class AnchorTracker(Flowable):
    """A flowable that tracks where an anchor appears in the document"""
    
    def __init__(self, anchor_name, doc_template):
        Flowable.__init__(self)
        self.anchor_name = anchor_name
        self.doc_template = doc_template
        self.width = 0
        self.height = 0
    
    def draw(self):
        """Called when the flowable is drawn - track the page number"""
        if hasattr(self.doc_template, 'track_anchor'):
            self.doc_template.track_anchor(self.anchor_name)
    
    def wrap(self, aW, aH):
        """Return dimensions - this flowable takes no space"""
        return (0, 0)