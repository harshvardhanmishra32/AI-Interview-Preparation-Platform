"""Login route wrapper for the unified authentication page."""
from views.auth import render_auth_page


def render_login_page():
    """Render the shared auth page with login selected."""
    render_auth_page(default_mode="login")
