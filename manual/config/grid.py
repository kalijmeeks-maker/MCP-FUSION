"""
12pt baseline grid system for consistent layout.
All dimensions are in points (1/72 inch).
"""

# Page dimensions (US Letter, landscape)
PAGE_WIDTH = 11 * 72   # 11 inches = 792 points
PAGE_HEIGHT = 8.5 * 72 # 8.5 inches = 612 points

# Grid
GRID_BASE = 12         # 12pt baseline grid
GRID_UNIT = GRID_BASE  # 12 points = 1 grid unit

# Spacing (multiples of GRID_UNIT)
MARGIN_OUTER = GRID_UNIT * 2      # 24pt margins
MARGIN_INNER = GRID_UNIT           # 12pt inner spacing
GUTTER_H = GRID_UNIT               # 12pt horizontal gutter between columns
GUTTER_V = GRID_UNIT               # 12pt vertical gutter between rows

# Working area (subtract margins)
CONTENT_WIDTH = PAGE_WIDTH - (MARGIN_OUTER * 2)
CONTENT_HEIGHT = PAGE_HEIGHT - (MARGIN_OUTER * 2)

# Column layout (3-column for flexibility)
NUM_COLS = 3
COL_WIDTH = (CONTENT_WIDTH - (GUTTER_H * (NUM_COLS - 1))) / NUM_COLS

# Row layout (4-row for vertical rhythm)
NUM_ROWS = 4
ROW_HEIGHT = (CONTENT_HEIGHT - (GUTTER_V * (NUM_ROWS - 1))) / NUM_ROWS

# Helper function to convert grid units to points
def grid_units_to_points(units):
    return units * GRID_UNIT

# Common dimensions
BOX_PADDING = GRID_UNIT              # 12pt padding inside components
BOX_BORDER_WIDTH = 1.5               # 1.5pt border
LINE_WIDTH_THIN = 0.75               # For signal paths
LINE_WIDTH_THICK = 1.5               # For emphasis

# Text line height (1.4x font size is standard)
def line_height(font_size):
    return font_size * 1.4
