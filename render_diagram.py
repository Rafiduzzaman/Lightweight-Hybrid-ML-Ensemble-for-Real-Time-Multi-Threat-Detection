#!/usr/bin/env python3
import asyncio
import sys
from pathlib import Path

async def render_html_to_png():
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("Installing playwright...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "playwright"])
        from playwright.async_api import async_playwright
    
    html_file = Path(__file__).parent / "architecture_diagram.html"
    png_file = Path(__file__).parent / "architecture_diagram.png"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"file:///{html_file.absolute()}")
        
        # Wait for Mermaid to render
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(2000)
        
        # Take screenshot of the mermaid diagram
        mermaid_element = await page.query_selector(".mermaid")
        if mermaid_element:
            await mermaid_element.screenshot(path=str(png_file))
            print(f"✅ PNG created: {png_file}")
        else:
            print("❌ Could not find mermaid element")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(render_html_to_png())
