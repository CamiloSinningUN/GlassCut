class GlassCutException(Exception):
    """GlassCut custom exception main class"""

class SlidePropertyError(GlassCutException):
    """Raised when a required slide property is not available."""
    
class BackendError(GlassCutException):
    """Raised when there's an issue with the slide backend."""
    

class MagnificationError(GlassCutException):
    """Raised when requested magnification is not available."""

class TileSizeOrCoordinatesError(GlassCutException):
    """Raised when tile size or coordinates are invalid."""
    
class FilterCompositionError(GlassCutException):
    """Raised when a filter composition for the class is not available"""
