import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Streamlit requires special handling on Vercel
# We'll create a simplified version that works with serverless

import streamlit.web.bootstrap as bootstrap
from streamlit.web.server import Server

def handler(request):
    """Vercel serverless handler"""
    # For now, return a simple status page
    # Full Streamlit integration requires containerized deployment
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": """
        <html>
        <head><title>TikTok Dashboard</title></head>
        <body>
        <h1>TikTok System Dashboard</h1>
        <p>Streamlit deployment requires container setup.</p>
        <p>Please check the main dashboard at the project repository.</p>
        </body>
        </html>
        """
    }

# For ASGI compatibility
try:
    from mangum import Mangum
    handler = Mangum(app)
except:
    pass
