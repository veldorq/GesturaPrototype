"""
Configuration validation utilities.
Ensures configuration values are valid before application startup.
"""

from typing import Any, Dict, List, Tuple
from dataclasses import fields


class ConfigValidationError(Exception):
    """Raised when configuration validation fails."""
    pass


class ConfigValidator:
    """
    Validates configuration values to prevent runtime errors.
    """
    
    @staticmethod
    def validate_constants(constants_class: Any) -> List[str]:
        """
        Validate all constants in the Constants dataclass.
        
        Args:
            constants_class: The Constants dataclass to validate
            
        Returns:
            List of validation warnings (empty if all valid)
            
        Raises:
            ConfigValidationError: If critical validation fails
        """
        warnings = []
        
        # Get all fields from dataclass
        const_fields = {f.name: f.type for f in fields(constants_class)}
        
        # Validate camera configuration
        if constants_class.CAMERA_INDEX < 0:
            raise ConfigValidationError("CAMERA_INDEX must be non-negative")
        
        if constants_class.FRAME_WIDTH < 320 or constants_class.FRAME_HEIGHT < 240:
            raise ConfigValidationError("Frame dimensions too small (minimum 320x240)")
        
        if constants_class.TARGET_FPS < 1 or constants_class.TARGET_FPS > 120:
            warnings.append("TARGET_FPS outside typical range (1-120)")
        
        # Validate detection configuration
        if not (0.0 <= constants_class.MIN_DETECTION_CONFIDENCE <= 1.0):
            raise ConfigValidationError("MIN_DETECTION_CONFIDENCE must be between 0 and 1")
        
        if not (0.0 <= constants_class.MIN_TRACKING_CONFIDENCE <= 1.0):
            raise ConfigValidationError("MIN_TRACKING_CONFIDENCE must be between 0 and 1")
        
        if constants_class.MAX_NUM_HANDS < 1:
            raise ConfigValidationError("MAX_NUM_HANDS must be at least 1")
        
        # Validate gesture recognition configuration
        if not (0.0 <= constants_class.GESTURE_CONFIDENCE_THRESHOLD <= 1.0):
            raise ConfigValidationError("GESTURE_CONFIDENCE_THRESHOLD must be between 0 and 1")
        
        if constants_class.DWELL_TIME_SECONDS < 0:
            raise ConfigValidationError("DWELL_TIME_SECONDS must be non-negative")
        
        if constants_class.DWELL_TIME_SECONDS < 0.5:
            warnings.append("DWELL_TIME_SECONDS very low - may cause accidental triggers")
        
        if constants_class.STABILIZATION_WINDOW < 1:
            raise ConfigValidationError("STABILIZATION_WINDOW must be at least 1")
        
        if constants_class.STABILIZATION_WINDOW > 20:
            warnings.append("STABILIZATION_WINDOW very high - may cause lag")
        
        if constants_class.DEBOUNCE_COOLDOWN_SECONDS < 0:
            raise ConfigValidationError("DEBOUNCE_COOLDOWN_SECONDS must be non-negative")
        
        # Validate UI configuration
        if constants_class.OVERLAY_PADDING < 0:
            warnings.append("OVERLAY_PADDING is negative")
        
        if constants_class.TEXT_FONT_SCALE <= 0:
            raise ConfigValidationError("TEXT_FONT_SCALE must be positive")
        
        if constants_class.TEXT_THICKNESS < 1:
            raise ConfigValidationError("TEXT_THICKNESS must be at least 1")
        
        # Validate action configuration
        if constants_class.SCROLL_AMOUNT <= 0:
            raise ConfigValidationError("SCROLL_AMOUNT must be positive")
        
        if constants_class.CLICK_DURATION <= 0:
            raise ConfigValidationError("CLICK_DURATION must be positive")
        
        return warnings
    
    @staticmethod
    def validate_file_paths(*paths: str) -> Tuple[bool, List[str]]:
        """
        Validate that file paths have reasonable names.
        
        Args:
            *paths: File paths to validate
            
        Returns:
            Tuple of (all_valid, errors)
        """
        errors = []
        
        for path in paths:
            if not path:
                errors.append("Empty file path")
                continue
            
            if '..' in path:
                errors.append(f"Path contains '..': {path}")
            
            if path.startswith('/') or path.startswith('\\'):
                errors.append(f"Path is absolute: {path}")
        
        return len(errors) == 0, errors
