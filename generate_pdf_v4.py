#!/usr/bin/env python3
"""
PDF Generator v4 - Magazine Quality with Playwright
Converts HTML template to professional PDF
"""

import asyncio
import os
import sys
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Playwright not installed. Installing...")
    os.system("pip install playwright -q")
    os.system("playwright install chromium")
    from playwright.async_api import async_playwright

async def generate_pdf():
    """Generate PDF from HTML template"""
    
    html_path = Path("pdf_template_v4.html").absolute()
    output_path = Path("pdf/Elternratgeber_PLUS_Lern_Erfolg_v4.pdf").absolute()
    
    # Ensure output directory exists
    output_path.parent.mkdir(exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Load HTML file
        await page.goto(f"file://{html_path}", wait_until="networkidle")
        
        # Wait for fonts to load
        await page.wait_for_timeout(2000)
        
        # Generate PDF
        await page.pdf(
            path=str(output_path),
            format="A4",
            margin={
                "top": "0",
                "right": "0", 
                "bottom": "0",
                "left": "0"
            },
            print_background=True,
            prefer_css_page_size=True
        )
        
        await browser.close()
        
        print(f"✅ PDF generated: {output_path}")
        print(f"📄 Size: {output_path.stat().st_size / 1024:.1f} KB")
        return output_path

if __name__ == "__main__":
    result = asyncio.run(generate_pdf())
    sys.exit(0 if result else 1)