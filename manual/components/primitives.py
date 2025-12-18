"""
Primitive drawing components: boxes, labels, signal paths, meters.
All functions return ReportLab drawing instructions (x, y, width, height, color, etc).
"""

from reportlab.lib import colors as rl_colors
from reportlab.graphics.shapes import Group, Rect, Line, Circle, Polygon, String
from config.colors import *
from config.grid import *

def component_box(x, y, width, height, label, color_border=COLOR_COMPONENT_BORDER):
    """
    Draw a labeled component box.
    Returns a ReportLab Group.
    """
    group = Group()
    
    # Background rectangle
    bg = Rect(x, y, width, height, 
              fillColor=rl_colors.HexColor(rgb_to_hex(COLOR_COMPONENT_BG)),
              strokeColor=rl_colors.HexColor(rgb_to_hex(color_border)),
              strokeWidth=BOX_BORDER_WIDTH)
    group.add(bg)
    
    # Label text (centered)
    text = String(x + width/2, y + height/2, label,
                  textAnchor="middle",
                  fontSize=FONT_SIZE_LABEL,
                  fillColor=rl_colors.HexColor(rgb_to_hex(FONT_COLOR_PRIMARY)),
                  fontName=FONT_FAMILY)
    group.add(text)
    
    return group

def signal_arrow(x1, y1, x2, y2, signal_type="audio", width=LINE_WIDTH_THIN):
    """
    Draw a directional arrow representing signal flow.
    signal_type: "audio" (blue), "video" (green), "control" (purple), "network" (yellow)
    """
    color_map = {
        "audio": COLOR_AUDIO,
        "video": COLOR_VIDEO,
        "control": COLOR_CONTROL,
        "network": COLOR_NETWORK
    }
    color = color_map.get(signal_type, COLOR_AUDIO)
    
    group = Group()
    
    # Line from start to end
    line = Line(x1, y1, x2, y2,
                strokeColor=rl_colors.HexColor(rgb_to_hex(color)),
                strokeWidth=width)
    group.add(line)
    
    # Arrowhead
    import math
    dx = x2 - x1
    dy = y2 - y1
    dist = math.sqrt(dx**2 + dy**2)
    if dist > 0:
        # Unit direction vector
        ux, uy = dx / dist, dy / dist
        # Perpendicular (rotated 90 degrees)
        px, py = -uy, ux
        # Arrowhead size
        arrow_len = 8
        arrow_width = 4
        # Arrow tip at (x2, y2)
        # Base is arrow_len units back
        base_x = x2 - ux * arrow_len
        base_y = y2 - uy * arrow_len
        left_x = base_x + px * arrow_width
        left_y = base_y + py * arrow_width
        right_x = base_x - px * arrow_width
        right_y = base_y - py * arrow_width
        
        arrow = Polygon([x2, y2, left_x, left_y, right_x, right_y],
                       fillColor=rl_colors.HexColor(rgb_to_hex(color)),
                       strokeColor=rl_colors.HexColor(rgb_to_hex(color)))
        group.add(arrow)
    
    return group

def callout_box(x, y, width, height, text, color_accent=COLOR_ACCENT_YELLOW):
    """
    Draw an annotation callout with colored left border.
    """
    group = Group()
    
    # Background
    bg = Rect(x, y, width, height,
              fillColor=rl_colors.HexColor(rgb_to_hex(COLOR_GRAY_DARK)),
              strokeColor=rl_colors.HexColor(rgb_to_hex(color_accent)),
              strokeWidth=BOX_BORDER_WIDTH)
    group.add(bg)
    
    # Left accent border
    accent = Rect(x, y, 4, height,
                  fillColor=rl_colors.HexColor(rgb_to_hex(color_accent)),
                  strokeWidth=0)
    group.add(accent)
    
    # Text (wrapped, left-aligned with padding)
    text_obj = String(x + BOX_PADDING + 4, y + height - BOX_PADDING,
                      text,
                      fontSize=FONT_SIZE_CALLOUT,
                      fillColor=rl_colors.HexColor(rgb_to_hex(FONT_COLOR_PRIMARY)),
                      fontName=FONT_FAMILY)
    group.add(text_obj)
    
    return group

def audio_meter(x, y, width, height, db_value=-18, peak_db=-6, label="AUDIO"):
    """
    Draw an audio level meter with plausible dBFS values.
    db_value: average level (typically -18 to -12 dBFS)
    peak_db: peak hold (typically -6 dBFS)
    """
    group = Group()
    
    # Meter background
    bg = Rect(x, y, width, height,
              fillColor=rl_colors.HexColor(rgb_to_hex(METER_BG)),
              strokeColor=rl_colors.HexColor(rgb_to_hex(COLOR_GRAY_MID)),
              strokeWidth=0.5)
    group.add(bg)
    
    # Meter scale: -60 dBFS (left) to 0 dBFS (right)
    meter_range = 60  # dB from -60 to 0
    scale_width = width - (BOX_PADDING * 2)
    
    # Draw level bar (green, nominal)
    db_pos = (db_value + 60) / meter_range  # Convert to 0-1 position
    bar_width = scale_width * db_pos
    bar = Rect(x + BOX_PADDING, y + height - 6, bar_width, 4,
               fillColor=rl_colors.HexColor(rgb_to_hex(METER_NOMINAL)),
               strokeWidth=0)
    group.add(bar)
    
    # Peak indicator (yellow vertical line)
    peak_pos = (peak_db + 60) / meter_range
    peak_x = x + BOX_PADDING + (scale_width * peak_pos)
    peak = Line(peak_x, y + 2, peak_x, y + height - 2,
                strokeColor=rl_colors.HexColor(rgb_to_hex(METER_PEAK)),
                strokeWidth=1.5)
    group.add(peak)
    
    # Grid lines at -30, -18, -12, -6, 0 dBFS
    grid_marks = [-30, -18, -12, -6, 0]
    for mark in grid_marks:
        mark_pos = (mark + 60) / meter_range
        mark_x = x + BOX_PADDING + (scale_width * mark_pos)
        mark_line = Line(mark_x, y + 1, mark_x, y + height - 1,
                        strokeColor=rl_colors.HexColor(rgb_to_hex(METER_GRID)),
                        strokeWidth=0.5)
        group.add(mark_line)
    
    # Label
    label_text = String(x + BOX_PADDING, y + height + 4,
                       label,
                       fontSize=FONT_SIZE_TINY,
                       fillColor=rl_colors.HexColor(rgb_to_hex(FONT_COLOR_SECONDARY)),
                       fontName=FONT_FAMILY)
    group.add(label_text)
    
    return group

def rgb_to_hex(rgb_tuple):
    """Convert (r, g, b) in 0-1 range to hex string with # prefix."""
    r, g, b = rgb_tuple
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

def device_silhouette(x, y, device_type, scale=1.0):
    """
    Draw brand-realistic device silhouettes.
    device_type: "ipad_pro", "ableton_live", "obs", "encoder", "footswitch"
    """
    group = Group()
    
    if device_type == "ipad_pro":
        # iPad Pro landscape (3:2 aspect ratio)
        width, height = 200 * scale, 150 * scale
        bg = Rect(x, y, width, height,
                  fillColor=rl_colors.HexColor("#1a1a1a"),
                  strokeColor=rl_colors.HexColor("#444444"),
                  strokeWidth=2)
        group.add(bg)
        
        # Home button (centered bottom)
        button = Circle(x + width/2, y + 12, 4,
                       fillColor=rl_colors.HexColor("#555555"))
        group.add(button)
        
        # Screen content area (dark blue tint)
        screen = Rect(x + 6, y + 6, width - 12, height - 18,
                     fillColor=rl_colors.HexColor("#0a1929"),
                     strokeWidth=0)
        group.add(screen)
        
        # Label
        label = String(x + width/2, y - 16,
                      "iPad Pro",
                      textAnchor="middle",
                      fontSize=FONT_SIZE_LABEL,
                      fillColor=rl_colors.HexColor(rgb_to_hex(FONT_COLOR_PRIMARY)),
                      fontName=FONT_FAMILY)
        group.add(label)
    
    elif device_type == "ableton_live":
        # Ableton Live logo/icon (simplified)
        width, height = 140 * scale, 140 * scale
        bg = Rect(x, y, width, height,
                  fillColor=rl_colors.HexColor("#0f0f0f"),
                  strokeColor=rl_colors.HexColor("#ffff00"),
                  strokeWidth=1.5)
        group.add(bg)
        
        # Ableton grid pattern (simplified)
        grid_size = 14
        for i in range(0, int(width), grid_size):
            for j in range(0, int(height), grid_size):
                cell = Rect(x + i, y + j, grid_size - 1, grid_size - 1,
                           fillColor=rl_colors.HexColor("#1a1a1a"),
                           strokeColor=rl_colors.HexColor("#333333"),
                           strokeWidth=0.5)
                group.add(cell)
        
        # Label
        label = String(x + width/2, y - 16,
                      "Ableton Live",
                      textAnchor="middle",
                      fontSize=FONT_SIZE_LABEL,
                      fillColor=rl_colors.HexColor(rgb_to_hex(FONT_COLOR_PRIMARY)),
                      fontName=FONT_FAMILY)
        group.add(label)
    
    elif device_type == "obs":
        # OBS Studio (rectangular interface)
        width, height = 160 * scale, 100 * scale
        bg = Rect(x, y, width, height,
                  fillColor=rl_colors.HexColor("#17191d"),
                  strokeColor=rl_colors.HexColor("#26a869"),
                  strokeWidth=1.5)
        group.add(bg)
        
        # OBS "window" elements
        title = Rect(x, y, width, 18,
                    fillColor=rl_colors.HexColor("#262e38"),
                    strokeWidth=0)
        group.add(title)
        
        # Label
        label = String(x + width/2, y - 16,
                      "OBS Studio",
                      textAnchor="middle",
                      fontSize=FONT_SIZE_LABEL,
                      fillColor=rl_colors.HexColor(rgb_to_hex(FONT_COLOR_PRIMARY)),
                      fontName=FONT_FAMILY)
        group.add(label)
    
    elif device_type == "encoder":
        # Hardware encoder (Dell, Telestream, etc)
        width, height = 140 * scale, 80 * scale
        bg = Rect(x, y, width, height,
                  fillColor=rl_colors.HexColor("#1a1a1a"),
                  strokeColor=rl_colors.HexColor("#cc0000"),
                  strokeWidth=1.5)
        group.add(bg)
        
        # Indicator lights
        for i in range(3):
            light = Circle(x + 20 + (i * 30), y + height/2, 3,
                          fillColor=rl_colors.HexColor("#cc0000"))
            group.add(light)
        
        # Label
        label = String(x + width/2, y - 16,
                      "Encoder",
                      textAnchor="middle",
                      fontSize=FONT_SIZE_LABEL,
                      fillColor=rl_colors.HexColor(rgb_to_hex(FONT_COLOR_PRIMARY)),
                      fontName=FONT_FAMILY)
        group.add(label)
    
    return group
