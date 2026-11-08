"""
SolAgent - One-Click Application Launcher
Runs the FastAPI server and serves the frontend dashboard at http://127.0.0.1:8000.
"""

import uvicorn
import webbrowser
import os
import sys

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    port = int(os.environ.get("PORT", 8000))
    url = f"http://127.0.0.1:{port}"
    print("=" * 60)
    print("  🚀 SolAgent - Autonomous Solana AI Copilot & Sentinel")
    print("  🏆 Built for MLH Solana Hackathon (AI Track & DeFi Track)")
    print(f"  🌐 Dashboard running at: {url}")
    print("=" * 60)

    # Launch browser automatically
    try:
        webbrowser.open(url)
    except Exception:
        pass

    # Start FastAPI / Uvicorn server
    uvicorn.run("backend.app:app", host="127.0.0.1", port=port, reload=False, log_level="info")

if __name__ == "__main__":
    main()
