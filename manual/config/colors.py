"""
Ableton Live-adjacent color palette for technical manual.
Dark, high-contrast, professional broadcast aesthetic.
"""

# Primary palette (signal flow, primary components)
COLOR_DARK_BG = (0.08, 0.08, 0.08)      # Near-black background
COLOR_ACCENT_BLUE = (0.2, 0.6, 1.0)     # Signal input (iPad, Ableton)
COLOR_ACCENT_GREEN = (0.2, 0.9, 0.5)    # Active/healthy signal
COLOR_ACCENT_YELLOW = (1.0, 0.85, 0.2)  # Warning/attention
COLOR_ACCENT_RED = (1.0, 0.3, 0.3)      # Critical/failure
COLOR_ACCENT_PURPLE = (0.8, 0.3, 1.0)   # Secondary/processing

# Neutral layers
COLOR_WHITE = (1.0, 1.0, 1.0)            # Text, labels, high contrast
COLOR_GRAY_LIGHT = (0.7, 0.7, 0.7)       # Secondary text
COLOR_GRAY_MID = (0.5, 0.5, 0.5)         # Dividers, borders
COLOR_GRAY_DARK = (0.25, 0.25, 0.25)     # Subtle background divisions

# Semantic signal colors
COLOR_AUDIO = (0.2, 0.6, 1.0)            # Audio signals (blue)
COLOR_VIDEO = (0.2, 0.9, 0.5)            # Video signals (green)
COLOR_CONTROL = (0.8, 0.3, 1.0)          # Control/MIDI (purple)
COLOR_NETWORK = (1.0, 0.85, 0.2)         # Network/NDI (yellow)

# Component styling
COLOR_COMPONENT_BG = (0.12, 0.12, 0.12)  # Component box background
COLOR_COMPONENT_BORDER = (0.35, 0.35, 0.35)  # Component border

# Meter reference levels (dBFS)
METER_BG = (0.05, 0.05, 0.05)
METER_NOMINAL = COLOR_ACCENT_GREEN       # -18 dBFS nominal
METER_PEAK = COLOR_ACCENT_YELLOW         # -6 dBFS peak
METER_CLIP = COLOR_ACCENT_RED            # Clipping
METER_GRID = COLOR_GRAY_DARK             # Grid lines

# Typography
FONT_FAMILY = "Helvetica"
FONT_SIZE_TITLE = 24
FONT_SIZE_HEADING = 14
FONT_SIZE_LABEL = 10
FONT_SIZE_CALLOUT = 9
FONT_SIZE_TINY = 8

FONT_COLOR_PRIMARY = COLOR_WHITE
FONT_COLOR_SECONDARY = COLOR_GRAY_LIGHT
FONT_COLOR_MUTED = COLOR_GRAY_MID
