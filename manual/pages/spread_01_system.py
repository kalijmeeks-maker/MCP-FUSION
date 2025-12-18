"""
SPREAD 01: System Overview
Full-page diagram implementation.
"""

from reportlab.graphics.shapes import Group, Rect, String, Line
from reportlab.lib import colors as rl_colors
from config.colors import *
from config.grid import *
from components.primitives import (
    device_silhouette, signal_arrow, component_box, 
    callout_box, audio_meter, rgb_to_hex
)

def render_spread_01_system(canvas):
    """
    Full-page system overview spread.
    iPad Pro → Ableton Live → NDI → OBS → Encoder → Stream + Archive
    
    Layout:
    - Top: Title & spread label
    - Middle (70%): Device chain with signal paths
    - Middle-lower: Audio/Video bus breakdowns
    - Bottom: Scene states, meters, critical callouts
    
    canvas parameter: unused (kept for interface compatibility)
    """
    
    group = Group()
    
    # BACKGROUND
    bg = Rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT,
              fillColor=rl_colors.HexColor(rgb_to_hex(COLOR_DARK_BG)),
              strokeWidth=0)
    group.add(bg)
    
    # ============================================================
    # TOP SECTION: Title & Navigation
    # ============================================================
    
    margin = MARGIN_OUTER
    content_y = PAGE_HEIGHT - margin
    
    # Spread marker (top-left)
    spread_num = String(margin, content_y - 20,
                       "SPREAD 01",
                       fontSize=FONT_SIZE_LABEL,
                       fillColor=rl_colors.HexColor(rgb_to_hex(COLOR_GRAY_MID)),
                       fontName=FONT_FAMILY)
    group.add(spread_num)
    
    # Main title (centered)
    title = String(PAGE_WIDTH / 2, content_y - 20,
                  "STREAMING SIGNAL FLOW",
                  textAnchor="middle",
                  fontSize=FONT_SIZE_TITLE,
                  fillColor=rl_colors.HexColor(rgb_to_hex(COLOR_WHITE)),
                  fontName=FONT_FAMILY)
    group.add(title)
    
    # Subtitle / description
    subtitle = String(PAGE_WIDTH / 2, content_y - 45,
                     "Complete signal path: source → mixing → composition → encoding → delivery",
                     textAnchor="middle",
                     fontSize=FONT_SIZE_CALLOUT,
                     fillColor=rl_colors.HexColor(rgb_to_hex(COLOR_GRAY_LIGHT)),
                     fontName=FONT_FAMILY)
    group.add(subtitle)
    
    # ============================================================
    # MAIN DIAGRAM: Device Chain (horizontal)
    # ============================================================
    
    device_row_y = content_y - 140
    
    # Device specifications
    devices = [
        {
            "type": "ipad_pro",
            "label": "iPad Pro",
            "role": "Host Control",
            "color": COLOR_ACCENT_BLUE,
        },
        {
            "type": "ableton_live",
            "label": "Ableton Live",
            "role": "Audio Mixing",
            "color": COLOR_AUDIO,
        },
        {
            "type": "obs",
            "label": "OBS Studio",
            "role": "Video Composition",
            "color": COLOR_VIDEO,
        },
        {
            "type": "encoder",
            "label": "NDI Encoder",
            "role": "Compression",
            "color": COLOR_NETWORK,
        },
    ]
    
    device_width = 120
    device_height = 100
    device_spacing = (CONTENT_WIDTH - (device_width * len(devices))) / (len(devices) - 1)
    
    device_positions = []
    
    for i, device_spec in enumerate(devices):
        # Horizontal position
        x = margin + (i * (device_width + device_spacing))
        device_positions.append((x, device_row_y))
        
        # Device silhouette
        silhouette = device_silhouette(x, device_row_y, device_spec["type"], scale=0.7)
        group.add(silhouette)
        
        # Role label below device
        role_label = String(x + device_width/2, device_row_y - 30,
                           device_spec["role"],
                           textAnchor="middle",
                           fontSize=FONT_SIZE_LABEL,
                           fillColor=rl_colors.HexColor(rgb_to_hex(device_spec["color"])),
                           fontName=FONT_FAMILY)
        group.add(role_label)
    
    # SIGNAL PATHS between devices
    signal_path_y = device_row_y + 50
    
    signal_specs = [
        {"from": 0, "to": 1, "type": "control", "label": "MIDI / OSC"},
        {"from": 1, "to": 2, "type": "network", "label": "NDI Audio"},
        {"from": 2, "to": 3, "type": "video", "label": "RTMP"},
    ]
    
    for sig in signal_specs:
        from_x = device_positions[sig["from"]][0] + device_width
        to_x = device_positions[sig["to"]][0]
        
        arrow = signal_arrow(from_x, signal_path_y, to_x, signal_path_y,
                            signal_type=sig["type"], width=LINE_WIDTH_THICK)
        group.add(arrow)
        
        # Label above arrow
        mid_x = (from_x + to_x) / 2
        label = String(mid_x, signal_path_y + 15,
                      sig["label"],
                      textAnchor="middle",
                      fontSize=FONT_SIZE_LABEL,
                      fillColor=rl_colors.HexColor(rgb_to_hex(devices[sig["from"]]["color"])),
                      fontName=FONT_FAMILY)
        group.add(label)
    
    # ============================================================
    # MIDDLE SECTION: Bus Architecture & Output Paths
    # ============================================================
    
    bus_section_y = device_row_y - 180
    
    # Three-column layout: Audio Buses | Video Sources | Output Destination
    col1_x = margin
    col2_x = margin + CONTENT_WIDTH / 3 + GUTTER_H
    col3_x = margin + (2 * CONTENT_WIDTH / 3) + (2 * GUTTER_H)
    col_width = CONTENT_WIDTH / 3 - GUTTER_H
    
    # COLUMN 1: Audio Bus Architecture
    audio_header = String(col1_x, bus_section_y + 40,
                         "AUDIO BUSES",
                         fontSize=FONT_SIZE_HEADING,
                         fillColor=rl_colors.HexColor(rgb_to_hex(COLOR_AUDIO)),
                         fontName=FONT_FAMILY)
    group.add(audio_header)
    
    bus_specs = [
        ("MUSIC", "Background track, instrumental"),
        ("VOICE", "Host dialogue, announcements"),
        ("PROGRAM", "Final mix, limiter applied"),
    ]
    
    bus_y = bus_section_y
    for bus_name, bus_desc in bus_specs:
        bus_box = component_box(col1_x, bus_y - 20, col_width - 10, 30,
                               bus_name,
                               color_border=COLOR_AUDIO)
        group.add(bus_box)
        
        bus_desc_text = String(col1_x, bus_y - 55,
                              bus_desc,
                              fontSize=FONT_SIZE_CALLOUT,
                              fillColor=rl_colors.HexColor(rgb_to_hex(COLOR_GRAY_LIGHT)),
                              fontName=FONT_FAMILY)
        group.add(bus_desc_text)
        
        bus_y -= 60
    
    # COLUMN 2: Video Sources
    video_header = String(col2_x, bus_section_y + 40,
                         "VIDEO SOURCES",
                         fontSize=FONT_SIZE_HEADING,
                         fillColor=rl_colors.HexColor(rgb_to_hex(COLOR_VIDEO)),
                         fontName=FONT_FAMILY)
    group.add(video_header)
    
    video_specs = [
        ("Camera", "Primary capture"),
        ("Desktop", "Screen share / content"),
        ("Graphics", "Titles, lower-thirds"),
    ]
    
    video_y = bus_section_y
    for video_name, video_desc in video_specs:
        video_box = component_box(col2_x, video_y - 20, col_width - 10, 30,
                                 video_name,
                                 color_border=COLOR_VIDEO)
        group.add(video_box)
        
        video_desc_text = String(col2_x, video_y - 55,
                                video_desc,
                                fontSize=FONT_SIZE_CALLOUT,
                                fillColor=rl_colors.HexColor(rgb_to_hex(COLOR_GRAY_LIGHT)),
                                fontName=FONT_FAMILY)
        group.add(video_desc_text)
        
        video_y -= 60
    
    # COLUMN 3: Output Destination
    output_header = String(col3_x, bus_section_y + 40,
                          "OUTPUT",
                          fontSize=FONT_SIZE_HEADING,
                          fillColor=rl_colors.HexColor(rgb_to_hex(COLOR_ACCENT_GREEN)),
                          fontName=FONT_FAMILY)
    group.add(output_header)
    
    output_specs = [
        ("LIVE STREAM", "CDN delivery (YouTube, Twitch)"),
        ("ARCHIVE", "Local MP4, cloud storage"),
        ("MONITORING", "Return to iPad / OBS"),
    ]
    
    output_y = bus_section_y
    for output_name, output_desc in output_specs:
        output_box = component_box(col3_x, output_y - 20, col_width - 10, 30,
                                  output_name,
                                  color_border=COLOR_ACCENT_GREEN)
        group.add(output_box)
        
        output_desc_text = String(col3_x, output_y - 55,
                                 output_desc,
                                 fontSize=FONT_SIZE_CALLOUT,
                                 fillColor=rl_colors.HexColor(rgb_to_hex(COLOR_GRAY_LIGHT)),
                                 fontName=FONT_FAMILY)
        group.add(output_desc_text)
        
        output_y -= 60
    
    # ============================================================
    # BOTTOM SECTION: Critical Limits & Monitoring
    # ============================================================
    
    bottom_y = bus_section_y - 280
    
    # CRITICAL LIMIT CALLOUT
    critical_callout = callout_box(margin, bottom_y, CONTENT_WIDTH, 50,
                                  "CRITICAL: Final Limiter on Program Bus (-1 dBTP ceiling). Prevents encoder saturation and archive clipping.",
                                  color_accent=COLOR_ACCENT_RED)
    group.add(critical_callout)
    
    # REFERENCE LEVELS
    ref_y = bottom_y - 80
    ref_header = String(margin, ref_y + 20,
                       "REFERENCE LEVELS (BROADCAST STANDARD)",
                       fontSize=FONT_SIZE_HEADING,
                       fillColor=rl_colors.HexColor(rgb_to_hex(COLOR_GRAY_MID)),
                       fontName=FONT_FAMILY)
    group.add(ref_header)
    
    # Three meters: Nominal, Peak, Integrated
    meter_specs = [
        ("Nominal Mix", -18),
        ("Peak Hold", -6),
        ("Integrated LUFS", -16),
    ]
    
    meter_x = margin
    meter_spacing = CONTENT_WIDTH / 3 - 10
    
    for meter_label, meter_value in meter_specs:
        meter = audio_meter(meter_x, ref_y - 50, 100, 30, db_value=meter_value, label=meter_label)
        group.add(meter)
        meter_x += meter_spacing
    
    # ============================================================
    # FOOTER: Page number
    # ============================================================
    
    footer_y = margin - 10
    page_num = String(PAGE_WIDTH / 2, footer_y,
                     "1",
                     textAnchor="middle",
                     fontSize=FONT_SIZE_LABEL,
                     fillColor=rl_colors.HexColor(rgb_to_hex(COLOR_GRAY_MID)),
                     fontName=FONT_FAMILY)
    group.add(page_num)
    
    return group


# Export
SPREAD_NAME = "System Overview"
SPREAD_FUNCTION = render_spread_01_system
