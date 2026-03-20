"""
Vercel Serverless API endpoint for TikTok Dashboard
"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def handler(request, context):
    """Main handler for Vercel serverless"""
    
    response = {
        "status": "active",
        "dashboard": "TikTok System Dashboard",
        "version": "1.0.0",
        "endpoints": {
            "/api/stats": "Get dashboard statistics",
            "/api/health": "Health check"
        },
        "note": "Full Streamlit UI requires containerized deployment. Use 'streamlit run streamlit_dashboard.py' locally."
    }
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(response, indent=2)
    }
