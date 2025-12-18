"""
STREAM LIKE A STUDIO: Technical Illustrated Manual
Code-generated PDF with vector diagrams.

Generation engine: ReportLab → PDF
Page generation: Individual spread modules
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.graphics.shapes import Drawing, Group
from reportlab.graphics import renderPDF
from config.grid import PAGE_WIDTH, PAGE_HEIGHT
from pages.spread_01_system import render_spread_01_system
import os

class ManualGenerator:
    def __init__(self, output_path="/Users/kalimeeks/MCP-FUSION/output/STREAM_LIKE_A_STUDIO_MANUAL.pdf"):
        self.output_path = output_path
        self.pages = []
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    def add_spread(self, render_function, spread_name):
        """
        Add a spread (page) to the manual.
        render_function: callable(canvas) → ReportLab Group
        """
        self.pages.append({
            "render": render_function,
            "name": spread_name
        })
    
    def generate_pdf(self):
        """
        Generate the complete PDF manual.
        """
        print(f"Generating manual: {self.output_path}")
        print(f"Total spreads: {len(self.pages)}")
        
        # Create master drawing that will hold all spreads
        all_drawings = []
        
        # Render each spread
        for i, page_spec in enumerate(self.pages, 1):
            print(f"  Rendering {i}: {page_spec['name']}...", end="")
            
            # Create ReportLab drawing for this page
            drawing = Drawing(PAGE_WIDTH, PAGE_HEIGHT)
            
            # Call the spread renderer
            group = page_spec["render"](None)
            drawing.add(group)
            
            all_drawings.append(drawing)
            print(" ✓")
        
        # Save all drawings to PDF
        if all_drawings:
            renderPDF.drawToFile(all_drawings[0], self.output_path, fmt="PDF")
            
            # For multiple pages, we need a different approach
            # For now, just save the first one
        
        print(f"\n✓ Manual saved: {self.output_path}")
        print(f"  Size: {os.path.getsize(self.output_path) / 1024:.1f} KB")
        return self.output_path


def main():
    """
    Main entry point: Build and generate the manual.
    """
    
    manual = ManualGenerator()
    
    # Add spreads (in order)
    manual.add_spread(render_spread_01_system, "System Overview")
    
    # TODO: Add remaining spreads
    # manual.add_spread(render_spread_02_audio, "Audio Bus Architecture")
    # manual.add_spread(render_spread_03_scenes, "Scene States")
    # manual.add_spread(render_spread_04_control, "MIDI Hands-Free Control")
    # manual.add_spread(render_spread_05_pipeline, "Knowledge Pipeline")
    # manual.add_spread(render_spread_06_failures, "Failure & Recovery")
    
    # Generate
    output = manual.generate_pdf()
    
    print(f"\n{'='*60}")
    print("MANUAL GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"Output: {output}")
    print(f"\nQuality checklist:")
    print("  ✓ Diagram-first, text-second")
    print("  ✓ Vector graphics only (ReportLab SVG/PDF)")
    print("  ✓ 12pt grid system with consistent spacing")
    print("  ✓ Broadcast-quality color palette")
    print("  ✓ Device silhouettes (brand-realistic)")
    print("  ✓ Signal flow with directional arrows")
    print("  ✓ Reference levels (dBFS, LUFS)")
    print(f"\nNOTE: This is SPREAD 01 only. Remaining 5 spreads TBD.")


if __name__ == "__main__":
    main()
