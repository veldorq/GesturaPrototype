"""
Configuration Validation for Gesture Recognition System
========================================================
Author: Senior Python Accessibility Engineer
Date: February 9, 2026

Purpose:
    Prevent silent bugs from misconfigured thresholds and parameters.
    Use pydantic for runtime validation with helpful error messages.

Integration:
    Optional layer - gracefully degrades if pydantic unavailable.

Safety:
    - Validates ranges (e.g., 0 < confidence < 1)
    - Checks logical consistency (e.g., min < max)
    - Provides clear error messages
"""

try:
    from pydantic import BaseModel, Field, ValidationError
    try:
        # Pydantic v2 (recommended)
        from pydantic import field_validator
        PYDANTIC_V2 = True
    except ImportError:
        # Pydantic v1 (legacy support)
        from pydantic import validator as field_validator
        PYDANTIC_V2 = False
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    PYDANTIC_V2 = False
    print("WARNING: pydantic not installed - config validation disabled")
    print("   Install with: pip install pydantic")


if PYDANTIC_AVAILABLE:
    class GestureRecognitionConfig(BaseModel):
        """
        Validated configuration for gesture recognition.
        
        All parameters validated at runtime with range checks and logic constraints.
        """
        
        # Camera settings
        camera_index: int = Field(default=0, ge=0, description="Camera device index")
        frame_width: int = Field(default=1280, ge=320, le=3840, description="Frame width")
        frame_height: int = Field(default=720, ge=240, le=2160, description="Frame height")
        fps_target: int = Field(default=30, ge=10, le=60, description="Target FPS")
        
        # Hand detection settings
        min_detection_confidence: float = Field(default=0.7, ge=0.0, le=1.0, 
                                               description="MediaPipe detection confidence")
        min_tracking_confidence: float = Field(default=0.7, ge=0.0, le=1.0,
                                              description="MediaPipe tracking confidence")
        max_num_hands: int = Field(default=1, ge=1, le=2, description="Maximum hands to detect")
        
        # Gesture stabilization
        gesture_buffer_size: int = Field(default=5, ge=3, le=15, 
                                        description="Gesture buffer size (frames)")
        debounce_time: float = Field(default=0.5, ge=0.1, le=2.0,
                                     description="Debounce time (seconds)")
        confidence_threshold: float = Field(default=0.6, ge=0.5, le=0.95,
                                           description="Gesture confidence threshold")
        
        # CNN settings
        cnn_min_confidence: float = Field(default=0.80, ge=0.5, le=0.99,
                                         description="CNN minimum confidence")
        cnn_high_confidence: float = Field(default=0.88, ge=0.5, le=0.99,
                                          description="CNN high confidence threshold")
        cnn_voting_window: int = Field(default=7, ge=3, le=15,
                                      description="CNN voting window size")
        cnn_voting_consistency: float = Field(default=0.85, ge=0.5, le=1.0,
                                             description="CNN voting consistency threshold")
        
        # State machine settings
        candidate_confirmation_frames: int = Field(default=5, ge=3, le=10,
                                                  description="Frames required for confirmation")
        candidate_timeout: float = Field(default=1.0, ge=0.5, le=3.0,
                                        description="Candidate timeout (seconds)")
        cooldown_duration: float = Field(default=0.6, ge=0.1, le=2.0,
                                        description="Default cooldown duration")
        
        # Swipe detection
        swipe_threshold: float = Field(default=0.20, ge=0.05, le=0.5,
                                      description="Horizontal swipe threshold")
        swipe_vertical_threshold: float = Field(default=0.18, ge=0.05, le=0.5,
                                               description="Vertical swipe threshold")
        swipe_direction_dominance_ratio: float = Field(default=2.5, ge=1.5, le=5.0,
                                                      description="Swipe direction dominance")
        swipe_confirmation_frames: int = Field(default=3, ge=2, le=7,
                                              description="Swipe confirmation frames")
        
        # Smoothing settings
        kalman_process_variance: float = Field(default=0.01, ge=0.001, le=0.1,
                                              description="Kalman process noise")
        kalman_measurement_variance: float = Field(default=0.1, ge=0.01, le=1.0,
                                                  description="Kalman measurement noise")
        savgol_window_length: int = Field(default=5, ge=3, le=11,
                                         description="Savitzky-Golay window (must be odd)")
        savgol_polyorder: int = Field(default=2, ge=1, le=5,
                                     description="Savitzky-Golay polynomial order")
        coordinate_smoothing_alpha: float = Field(default=0.3, ge=0.1, le=0.9,
                                                 description="Coordinate smoothing factor")
        
        @field_validator('cnn_high_confidence')
        @classmethod
        def validate_cnn_confidence_ordering(cls, v, info=None):
            """Ensure high_confidence >= min_confidence"""
            # Pydantic v2 uses info.data, v1 uses values parameter
            values = info.data if (info and hasattr(info, 'data')) else (info or {})
            if 'cnn_min_confidence' in values and v < values['cnn_min_confidence']:
                raise ValueError(
                    f"cnn_high_confidence ({v}) must be >= cnn_min_confidence ({values['cnn_min_confidence']})"
                )
            return v
        
        @field_validator('savgol_window_length')
        @classmethod
        def validate_savgol_window_odd(cls, v):
            """Ensure Savitzky-Golay window is odd"""
            if v % 2 == 0:
                raise ValueError(f"savgol_window_length must be odd, got {v}")
            return v
        
        @field_validator('savgol_polyorder')
        @classmethod
        def validate_savgol_polyorder(cls, v, info=None):
            """Ensure polyorder < window_length"""
            # Pydantic v2 uses info.data, v1 uses values parameter
            values = info.data if (info and hasattr(info, 'data')) else (info or {})
            if 'savgol_window_length' in values and v >= values['savgol_window_length']:
                raise ValueError(
                    f"savgol_polyorder ({v}) must be < savgol_window_length ({values['savgol_window_length']})"
                )
            return v
        
        if PYDANTIC_V2:
            # Pydantic v2 configuration
            model_config = {
                'validate_assignment': True,
                'extra': 'forbid'
            }
        else:
            # Pydantic v1 configuration
            class Config:
                validate_assignment = True
                extra = 'forbid'
    
    
    def validate_config(config_dict):
        """
        Validate configuration dictionary.
        
        Args:
            config_dict: Dictionary of configuration values
        
        Returns:
            Validated config object or None if validation fails
        """
        try:
            validated = GestureRecognitionConfig(**config_dict)
            print("[SUCCESS] Configuration validated successfully")
            return validated
        except ValidationError as e:
            print("[ERROR] Configuration Validation Errors:")
            for error in e.errors():
                field = '.'.join(str(loc) for loc in error['loc'])
                print(f"   - {field}: {error['msg']}")
            return None
    
    
    def export_validated_config(config_obj, format='dict'):
        """
        Export validated config.
        
        Args:
            config_obj: Validated config object
            format: 'dict' or 'json'
        
        Returns:
            Configuration in requested format
        """
        if format == 'dict':
            # Pydantic v2 uses model_dump(), v1 uses dict()
            return config_obj.model_dump() if PYDANTIC_V2 else config_obj.dict()
        elif format == 'json':
            # Pydantic v2 uses model_dump_json(), v1 uses json()
            return config_obj.model_dump_json(indent=2) if PYDANTIC_V2 else config_obj.json(indent=2)
        else:
            raise ValueError(f"Unknown format: {format}")

else:
    # Fallback if pydantic not available
    class GestureRecognitionConfig:
        """Dummy config class (no validation)"""
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    def validate_config(config_dict):
        """No-op validation"""
        print("WARNING: Config validation skipped (pydantic not available)")
        return GestureRecognitionConfig(**config_dict)
    
    def export_validated_config(config_obj, format='dict'):
        """No-op export"""
        return vars(config_obj)


def test_validation():
    """Test configuration validation"""
    print("\n" + "="*70)
    print("  CONFIGURATION VALIDATION TEST")
    print("="*70 + "\n")
    
    if not PYDANTIC_AVAILABLE:
        print("[SKIP] pydantic not available - skipping tests")
        return
    
    # Test 1: Valid configuration
    print("Test 1: Valid configuration")
    valid_config = {
        'cnn_min_confidence': 0.80,
        'cnn_high_confidence': 0.88,
        'savgol_window_length': 5,
        'savgol_polyorder': 2
    }
    validated = validate_config(valid_config)
    print(f"   Result: {'[PASS]' if validated else '[FAIL]'}\n")
    
    # Test 2: Invalid - high < min
    print("Test 2: Invalid - high_confidence < min_confidence")
    invalid_config = {
        'cnn_min_confidence': 0.85,
        'cnn_high_confidence': 0.80  # INVALID: lower than min
    }
    validated = validate_config(invalid_config)
    print(f"   Result: {'[FAIL - Should reject]' if validated else '[PASS - Correctly rejected]'}\n")
    
    # Test 3: Invalid - even window length
    print("Test 3: Invalid - even Savitzky-Golay window")
    invalid_config = {
        'savgol_window_length': 6,  # INVALID: must be odd
        'savgol_polyorder': 2
    }
    validated = validate_config(invalid_config)
    print(f"   Result: {'[FAIL - Should reject]' if validated else '[PASS - Correctly rejected]'}\n")
    
    # Test 4: Invalid - polyorder >= window
    print("Test 4: Invalid - polyorder >= window_length")
    invalid_config = {
        'savgol_window_length': 5,
        'savgol_polyorder': 5  # INVALID: must be < window
    }
    validated = validate_config(invalid_config)
    print(f"   Result: {'[FAIL - Should reject]' if validated else '[PASS - Correctly rejected]'}\n")
    
    # Test 5: Out of range
    print("Test 5: Invalid - confidence out of range")
    invalid_config = {
        'cnn_min_confidence': 1.5  # INVALID: > 1.0
    }
    validated = validate_config(invalid_config)
    print(f"   Result: {'[FAIL - Should reject]' if validated else '[PASS - Correctly rejected]'}\n")


if __name__ == "__main__":
    test_validation()
