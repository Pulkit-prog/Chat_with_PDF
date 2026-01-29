"""
Startup script for Assessment Chat RAG.
Validates environment and dependencies before launching Streamlit.
"""
import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version compatibility."""
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 9):
        print(f"❌ Python {major}.{minor} detected. Requires Python 3.9+")
        return False
    print(f"✅ Python {major}.{minor} - OK")
    return True

def check_dependencies():
    """Check if required packages are installed."""
    required = [
        ('streamlit', 'streamlit'),
        ('PyPDF2', 'PyPDF2'),
        ('faiss', 'faiss-cpu'),
        ('google.generativeai', 'google-generativeai'),
        ('groq', 'groq'),
        ('dotenv', 'python-dotenv'),
        ('numpy', 'numpy')
    ]
    
    missing = []
    for module_name, package_name in required:
        try:
            __import__(module_name)
            print(f"✅ {package_name} - OK")
        except ImportError:
            print(f"❌ {package_name} - MISSING")
            missing.append(package_name)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False
    
    return True

def check_environment():
    """Check environment configuration."""
    from dotenv import load_dotenv
    load_dotenv()
    
    groq_key = os.getenv('GROQ_API_KEY', '')
    gemini_key = os.getenv('GEMINI_API_KEY', '')
    
    if not groq_key:
        print("❌ GROQ_API_KEY not set in .env")
        return False
    print(f"✅ GROQ_API_KEY - OK (length: {len(groq_key)})")
    
    if not gemini_key:
        print("❌ GEMINI_API_KEY not set in .env")
        return False
    print(f"✅ GEMINI_API_KEY - OK (length: {len(gemini_key)})")
    
    return True

def check_directories():
    """Check if required directories exist."""
    from config import Config
    Config.load_from_env()
    
    dirs = [
        Config.DATA_DIR,
        Config.VECTORS_DIR,
        Config.MEMORY_DIR,
        Config.PDFS_DIR
    ]
    
    for directory in dirs:
        if directory.exists():
            print(f"✅ {directory.name}/ - OK")
        else:
            print(f"⚠️  {directory.name}/ - Creating...")
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✅ {directory.name}/ - Created")
    
    return True

def main():
    """Run all checks and start the app."""
    print("=" * 60)
    print("Assessment Chat RAG - Startup Verification")
    print("=" * 60)
    print()
    
    print("1. Checking Python Version...")
    if not check_python_version():
        sys.exit(1)
    print()
    
    print("2. Checking Dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print()
    
    print("3. Checking Environment Variables...")
    if not check_environment():
        print("\n⚠️  Please configure API keys in .env file")
        print("   Copy .env.sample to .env and add your keys:")
        print("   - GROQ_API_KEY=your_groq_key")
        print("   - GEMINI_API_KEY=your_gemini_key")
        sys.exit(1)
    print()
    
    print("4. Checking Data Directories...")
    if not check_directories():
        sys.exit(1)
    print()
    
    print("=" * 60)
    print("✅ All checks passed! Starting Streamlit app...")
    print("=" * 60)
    print()
    
    # Import streamlit and run the app
    import streamlit.web.cli as stcli
    sys.argv = ["streamlit", "run", "app.py"]
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()
