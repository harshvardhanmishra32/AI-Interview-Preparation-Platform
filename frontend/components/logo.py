"""Custom premium SVG logo renderer for the PREPAI platform."""
import streamlit as st

def get_logo_svg(height: int = 32, show_text: bool = True, font_size: int = 20) -> str:
    """Generate the raw SVG markup for the PREPAI logo with premium linear gradients."""
    gradient_id = "logo-grad"
    
    # We join all elements into a single flat line with zero indentation to prevent markdown preformatted block parsing
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {240 if show_text else 40} 40" height="{height}" style="vertical-align: middle;">',
        '<defs>',
        f'<linearGradient id="{gradient_id}" x1="0%" y1="0%" x2="100%" y2="100%">',
        '<stop offset="0%" stop-color="#2563EB" />',
        '<stop offset="100%" stop-color="#7C3AED" />',
        '</linearGradient>',
        '<filter id="glow" x="-20%" y="-20%" width="140%" height="140%">',
        '<feGaussianBlur stdDeviation="1.5" result="blur" />',
        '<feComposite in="SourceGraphic" in2="blur" operator="over" />',
        '</filter>',
        '</defs>',
        '<g transform="translate(0, 0)">',
        f'<polygon points="20,2 38,12 38,30 20,38 2,30 2,12" fill="none" stroke="url(#{gradient_id})" stroke-width="2.5" filter="url(#glow)"/>',
        f'<circle cx="20" cy="20" r="6" fill="url(#{gradient_id})" />',
        '<line x1="20" y1="20" x2="20" y2="8" stroke="rgba(255,255,255,0.7)" stroke-width="1.5" />',
        '<line x1="20" y1="20" x2="10" y2="26" stroke="rgba(255,255,255,0.7)" stroke-width="1.5" />',
        '<line x1="20" y1="20" x2="30" y2="26" stroke="rgba(255,255,255,0.7)" stroke-width="1.5" />',
        '<circle cx="20" cy="8" r="2" fill="#ffffff" />',
        '<circle cx="10" cy="26" r="2" fill="#ffffff" />',
        '<circle cx="30" cy="26" r="2" fill="#ffffff" />',
        '</g>'
    ]
    
    if show_text:
        svg_parts.append(
            f'<text x="52" y="27" font-family="\'Inter\', -apple-system, sans-serif" font-weight="800" font-size="{font_size}px" fill="var(--text)" letter-spacing="1.5px">'
            f'PREP<tspan fill="url(#{gradient_id})">AI</tspan>'
            '</text>'
        )
        
    svg_parts.append('</svg>')
    
    return "".join(svg_parts)

def render_logo(height: int = 32, show_text: bool = True, font_size: int = 20):
    """Render the PREPAI logo in Streamlit via HTML injection."""
    logo_html = get_logo_svg(height=height, show_text=show_text, font_size=font_size)
    st.markdown(
        f'<div class="logo-wrapper" style="display: inline-block; vertical-align: middle;">{logo_html}</div>', 
        unsafe_allow_html=True
    )
