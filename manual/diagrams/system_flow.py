"""
SYSTEM FLOW DIAGRAM
iPad Pro → Ableton Live → NDI → OBS → Dell Encoder → Stream / Archive

This is the heart of the streaming pipeline.
Diagram-first, text-second.
"""

from reportlab.graphics.shapes import Group, Rect, String, Line
from reportlab.lib import colors as rl_colors
from config.colors import *
from config.grid import *
from components.primitives import (
    device_silhouette, signal_arrow, component_box, 
    callout_box, rgb_to_hex
)

def render_system_flow(canvas):
    """
    Render full-page system flow diagram.
    Returns ReportLab Group ready to add to canvas.
    """
    group = Group()
    
    # Background
    bg = Rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT,
              fillColor=rl_colors.HexColor(rgb_to_hex(COLOR_DARK_BG)),
              strokeWidth=0)
    group.add(bg)
    
    # Page margin boundaries
    content_x = MARGIN_OUTER
    content_y = MARGIN_OUTER
    content_w = CONTENT_WIDTH
    content_h = CONTENT_HEIGHT
    
    # HEADER / SPREAD LABEL
    spread_label = String(content_x, PAGE_HEIGHT - 30,
                         "SPREAD 01: SYSTEM OVERVIEW",
                         fontSize=FONT_SIZE_HEADING,
                         fillColor=rl_colors.HexColor(rgb_to_hex(COLOR_GRAY_MID)),
                         fontName=FONT_FAMILY)
    group.add(spread_label)
    
    # TITLE
    title = String(content_x, PAGE_HEIGHT - 60,
                  "STREAMING SIGNAL FLOW",
                  fontSize=FONT_SIZE_TITLE,
                  fillColor=rl_colors.HexColor(rgb_to_hex(COLOR_WHITE)),
                  fontName=FONT_FAMILY)
    group.add(title)
    
    # DEVICE ROW (left to right: iPad, Ableton, NDI, OBS, Encoder)
    device_y = PAGE_HEIGHT - 240
    device_spacing = 130
    
    devices = [
        ("ipad_pro", "iPad Pro\n(Host Control)"),
        ("ableton_live", "Ableton Live\n(Audio Mix)"),
        ("obs", "OBS Studio\n(Compose)"),
        ("encoder", "NDI Encoder\n(Compress)"),
    ]
    
    device_xs = []
    for i, (device_type, label) in enumerate(devices):
        x = content_x + (i * device_spacing) + 20
        device_xs.append(x)
        
        # Device silhouette
        dev = device_silhouette(x, device_y, device_type, scale=0.8)
        group.add(dev)
    
    # SIGNAL ARROWS between devices
    arrow_y = device_y - 60
    
    # iPad → Ableton (MIDI control)
    arrow1 = signal_arrow(device_xs[0] + 80, arrow_y + 20,
                         device_xs[1] + 20, arrow_y + 20,
                         signal_type="control")
    group.add(arrow1)
    label1 = String(device_xs[0] + 120, arrow_y + 35,
                   "MIDI / OSC",
                   fontSize=FONT_SIZE_LABEL,
                   fillColor=rl_colors.HexColor(rgb_to_hex(COLOR_CONTROL)),
                   fontName=FONT_FAMILY)
    group.add(label1)
    
    # Ableton → NDI (Audio via NDI encoder)
    arrow2 = signal_arrow(device_xs[1] + 70, arrow_y + 20,
                         device_xs[2] + 30, arrow_y + 20,
                         signal_type="network")
    group.add(arrow2)
    label2 = String(device_xs[1] + 80, arrow_y + 35,
                   "NDI Audio",
                   fontSize=FONT_SIZE_LABEL,
                   fillColor=rl_colors.HexColor(rgb_to_hex(COLOR_NETWORK)),
                   fontName=FONT_FAMILY)
    group.add(label2)
    
    # OBS → Encoder (Video + Audio)
    arrow3 = signal_arrow(device_xs[2] + 80, arrow_y + 20,
                         device_xs[3] + 20, arrow_y + 20,
                         signal_type="video")
    group.add(arrow3)
    label3 = String(device_xs[2] + 100, arrow_y + 35,
                   "RTMP / UDP",
                   fontSize=FONT_SIZE_LABEL,
                   fillColor=rl_colors.HexColor(rgb_to_hex(COLOR_VIDEO)),
                   fontName=FONT_FAMILY)
    group.add(label3)
    
    # DETAILED SIGNAL PATH BOXES
    # Below the device row, show the audio/video breakdown
    
    detail_y = device_y - 160
    
    # Audio Bus Section
    audio_box = component_box(content_x, detail_y, COL_WIDTH - GUTTER_H/2, 80,
                             "AUDIO BUS\nMUSIC / VOICE / PROGRAM",
                             color_border=COLOR_AUDIO)
    group.add(audio_box)
    
    # Video Composition Section
    video_x = content_x + COL_WIDTH + GUTTER_H/2
    video_box = component_box(video_x, detail_y, COL_WIDTH - GUTTER_H/2, 80,
                             "VIDEO COMPOSITION\nMULTI-SOURCE BLEND",
                             color_border=COLOR_VIDEO)
    group.add(video_box)
    
    # Output/Archive Section
    output_x = video_x + COL_WIDTH + GUTTER_H/2
    output_box = component_box(output_x, detail_y, COL_WIDTH - GUTTER_H/2, 80,
                              "OUTPUT\nLIVE STREAM + ARCHIVE",
                              color_border=COLOR_ACCENT_GREEN)
    group.add(output_box)
    
    # SIGNAL FLOW FROM BUSES
    # Audio bus → Encoder (downward arrow)
    arrow_audio = signal_arrow(content_x + (COL_WIDTH - GUTTER_H/2)/2, detail_y,
                              content_x + (COL_WIDTH - GUTTER_H/2)/2, detail_y - 40,
                              signal_type="audio")
    group.add(arrow_audio)
    
    # Video comp → Encoder
    arrow_video = signal_arrow(video_x + (COL_WIDTH - GUTTER_H/2)/2, detail_y,
                              video_x + (COL_WIDTH - GUTTER_H/2)/2, detail_y - 40,
                              signal_type="video")
    group.add(arrow_video)
    
    # CRITICAL CALLOUT: Limiter at Program Bus
    callout_y = detail_y - 120
    callout = callout_box(content_x + 20, callout_y, CONTENT_WIDTH - 40, 50,
                         "CRITICAL: Final Limiter on Program Bus (-1 dBTP ceiling). Protects encoder & archive.",
                         color_accent=COLOR_ACCENT_RED)
    group.add(callout)
    
    # BOTTOM SECTION: Scene State Indicators
    state_y = callout_y - 100
    
    state_label = String(content_x, state_y + 40,
                        "ACTIVE SCENE STATE",
                        fontSize=FONT_SIZE_HEADING,
                        fillColor=rl_colors.HexColor(rgb_to_hex(COLOR_GRAY_MID)),
                        fontName=FONT_FAMILY)
    group.add(state_label)
    
    # Three scene modes
    scenes = [
        ("TALK", "VOICE dominant\nMUSIC muted"),
        ("PRODUCTION", "MUSIC + VOICE\nBalanced mix"),
        ("PERFORMANCE", "MUSIC dominant\nVOICE reduced"),
    ]
    
    scene_width = (CONTENT_WIDTH - (GUTTER_H * 2)) / 3
    for i, (mode, desc) in enumerate(scenes):
        scene_x = content_x + (i * (scene_width + GUTTER_H))
        scene_box = component_box(scene_x, state_y - 60, scene_width, 40,
                                 mode,
                                 color_border=COLOR_ACCENT_YELLOW if i == 1 else COLOR_GRAY_MID)
        group.add(scene_box)
        
        # Description callout
        desc_text = String(scene_x + scene_width/2, state_y - 75,
                          desc,
                          textAnchor="middle",
                          fontSize=FONT_SIZE_CALLOUT,
                          fillColor=rl_colors.HexColor(rgb_to_hex(FONT_COLOR_SECONDARY)),
                          fontName=FONT_FAMILY)
        group.add(desc_text)
    
    return group


# Export for PDF generation
DIAGRAM_NAME = "System Flow"
DIAGRAM_FUNCTION = render_system_flow
