"""Register route wrapper for the unified authentication page."""
from views.auth import render_auth_page


def render_register_page():
    """Render the shared auth page with account creation selected."""
    render_auth_page(default_mode="register")
