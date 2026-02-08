"""
Visual feedback overlay for the AccessAble application.
Renders real-time information on the video feed.
"""

import cv2
import numpy as np
from typing import Optional, Tuple
from config.constants import Constants


class OverlayRenderer:
    """
    Renders visual feedback on video frames.
    
    Provides users with real-time information about:
    - Detected gesture
    - Mapped action
    - Dwell time progress
    - System status
    """
    
    def __init__(
        self,
        frame_width: int = Constants.FRAME_WIDTH,
        frame_height: int = Constants.FRAME_HEIGHT
    ):
        """
        Initialize overlay renderer.
        
        Args:
            frame_width: Width of video frame
            frame_height: Height of video frame
        """
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.padding = Constants.OVERLAY_PADDING
        
        # Font configuration
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = Constants.TEXT_FONT_SCALE
        self.font_thickness = Constants.TEXT_THICKNESS
    
    def render_info_panel(
        self,
        frame: np.ndarray,
        gesture_name: Optional[str],
        action_name: Optional[str],
        confidence: float,
        dwell_progress: float,
        is_paused: bool = False,
        state_info: dict = None
    ) -> np.ndarray:
        """
        Render information panel on frame with state machine visualization.
        
        Args:
            frame: Video frame to draw on
            gesture_name: Name of detected gesture
            action_name: Name of mapped action
            confidence: Detection confidence [0, 1]
            dwell_progress: Dwell time progress [0, 1]
            is_paused: Whether system is paused
            state_info: State machine information (optional)
            
        Returns:
            Frame with overlay drawn
        """
        # Create semi-transparent background panel
        panel_height = 200 if state_info else 150
        panel = np.zeros((panel_height, self.frame_width, 3), dtype=np.uint8)
        panel[:] = Constants.COLOR_BACKGROUND
        
        # Blend panel with frame (transparency)
        y_offset = 0
        alpha = 0.7
        frame[y_offset:y_offset + panel_height] = cv2.addWeighted(
            frame[y_offset:y_offset + panel_height],
            1 - alpha,
            panel,
            alpha,
            0
        )
        
        # Render text information
        y_pos = self.padding + 25
        
        # System status with state machine state
        if is_paused:
            status_text = "PAUSED"
            status_color = Constants.COLOR_DANGER
        else:
            status_text = "ACTIVE"
            status_color = Constants.COLOR_PRIMARY
        
        # Add state machine state if available
        if state_info:
            state = state_info.get('state', 'none').upper()
            status_text += f" | {state}"
            
            # Color code by state
            if state == 'COOLDOWN':
                status_color = Constants.COLOR_DANGER
            elif state == 'CONFIRMED':
                status_color = Constants.COLOR_PRIMARY
            elif state == 'CANDIDATE':
                status_color = Constants.COLOR_SECONDARY
        
        cv2.putText(
            frame,
            f"Status: {status_text}",
            (self.padding, y_pos),
            self.font,
            self.font_scale,
            status_color,
            self.font_thickness
        )
        
        y_pos += 30
        
        # Gesture information
        if gesture_name:
            gesture_display = gesture_name.replace('_', ' ').title()
            cv2.putText(
                frame,
                f"Gesture: {gesture_display}",
                (self.padding, y_pos),
                self.font,
                self.font_scale,
                Constants.COLOR_INFO,
                self.font_thickness
            )
            
            y_pos += 30
            
            # Confidence score
            confidence_percent = int(confidence * 100)
            cv2.putText(
                frame,
                f"Confidence: {confidence_percent}%",
                (self.padding, y_pos),
                self.font,
                self.font_scale * 0.8,
                Constants.COLOR_TEXT,
                self.font_thickness - 1
            )
        else:
            cv2.putText(
                frame,
                "No gesture detected",
                (self.padding, y_pos),
                self.font,
                self.font_scale,
                Constants.COLOR_TEXT,
                self.font_thickness - 1
            )
        
        y_pos += 35
        
        # Action preview
        if action_name and action_name != 'none':
            action_display = action_name.replace('_', ' ').title()
            cv2.putText(
                frame,
                f"Action: {action_display}",
                (self.padding, y_pos),
                self.font,
                self.font_scale,
                Constants.COLOR_SECONDARY,
                self.font_thickness
            )
        
        y_pos += 30
        
        # State machine metrics
        if state_info:
            action_count = state_info.get('action_count', 0)
            cv2.putText(
                frame,
                f"Actions: {action_count}",
                (self.padding, y_pos),
                self.font,
                self.font_scale * 0.7,
                Constants.COLOR_TEXT,
                self.font_thickness - 1
            )
        
        # Dwell time progress bar
        if gesture_name and not is_paused and state_info:
            if state_info.get('state') == 'candidate':
                self._render_progress_bar(frame, dwell_progress, "Dwell Progress")
            elif state_info.get('state') == 'cooldown':
                cooldown_prog = state_info.get('cooldown_progress', 0.0)
                self._render_progress_bar(frame, cooldown_prog, "Cooldown", Constants.COLOR_DANGER)
        
        return frame
    
    def _render_progress_bar(
        self,
        frame: np.ndarray,
        progress: float,
        label: str = "Progress",
        base_color: Tuple[int, int, int] = None
    ) -> None:
        """
        Render progress bar with label.
        
        Args:
            frame: Frame to draw on
            progress: Progress value [0, 1]
            label: Label to display above bar
            base_color: Base color for bar (optional)
        """
        bar_x = self.frame_width - Constants.PROGRESS_BAR_WIDTH - self.padding
        bar_y = self.padding
        bar_width = Constants.PROGRESS_BAR_WIDTH
        bar_height = Constants.PROGRESS_BAR_HEIGHT
        
        # Background (unfilled portion)
        cv2.rectangle(
            frame,
            (bar_x, bar_y + 20),
            (bar_x + bar_width, bar_y + bar_height + 20),
            Constants.COLOR_TEXT,
            2
        )
        
        # Filled portion (progress)
        if progress > 0:
            fill_width = int(bar_width * progress)
            
            # Color changes based on progress
            if base_color:
                color = base_color
            elif progress < 0.5:
                color = Constants.COLOR_INFO
            elif progress < 0.9:
                color = Constants.COLOR_SECONDARY
            else:
                color = Constants.COLOR_PRIMARY
            
            cv2.rectangle(
                frame,
                (bar_x + 2, bar_y + 22),
                (bar_x + fill_width - 2, bar_y + bar_height + 18),
                color,
                -1  # Filled
            )
        
        # Progress percentage
        progress_percent = int(progress * 100)
        text = f"{progress_percent}%"
        text_size = cv2.getTextSize(
            text,
            self.font,
            self.font_scale * 0.6,
            self.font_thickness - 1
        )[0]
        
        text_x = bar_x + (bar_width - text_size[0]) // 2
        text_y = bar_y + 15
        
        cv2.putText(
            frame,
            text,
            (text_x, text_y),
            self.font,
            self.font_scale * 0.5,
            Constants.COLOR_TEXT,
            self.font_thickness - 1
        )
        
        # Label
        cv2.putText(
            frame,
            label,
            (bar_x, bar_y),
            self.font,
            self.font_scale * 0.5,
            Constants.COLOR_TEXT,
            self.font_thickness - 1
        )
    
    def render_help_text(self, frame: np.ndarray) -> np.ndarray:
        """
        Render help text with keyboard shortcuts.
        
        Args:
            frame: Frame to draw on
            
        Returns:
            Frame with help text
        """
        help_lines = [
            "ESC - Emergency Stop",
            "Q - Quit Application",
        ]
        
        y_pos = self.frame_height - self.padding - (len(help_lines) * 25)
        
        for line in help_lines:
            cv2.putText(
                frame,
                line,
                (self.padding, y_pos),
                self.font,
                self.font_scale * 0.6,
                Constants.COLOR_TEXT,
                self.font_thickness - 1
            )
            y_pos += 25
        
        return frame
    
    def render_notification(
        self,
        frame: np.ndarray,
        message: str,
        duration: float = 2.0,
        color: Tuple[int, int, int] = None
    ) -> np.ndarray:
        """
        Render temporary notification message.
        
        Args:
            frame: Frame to draw on
            message: Notification message
            duration: How long to display (not used here, managed by caller)
            color: Text color (BGR)
            
        Returns:
            Frame with notification
        """
        if color is None:
            color = Constants.COLOR_PRIMARY
        
        # Center the message
        text_size = cv2.getTextSize(
            message,
            self.font,
            self.font_scale,
            self.font_thickness
        )[0]
        
        text_x = (self.frame_width - text_size[0]) // 2
        text_y = self.frame_height // 2
        
        # Draw background rectangle
        padding = 15
        cv2.rectangle(
            frame,
            (text_x - padding, text_y - text_size[1] - padding),
            (text_x + text_size[0] + padding, text_y + padding),
            Constants.COLOR_BACKGROUND,
            -1
        )
        
        # Draw text
        cv2.putText(
            frame,
            message,
            (text_x, text_y),
            self.font,
            self.font_scale,
            color,
            self.font_thickness
        )
        
        return frame
