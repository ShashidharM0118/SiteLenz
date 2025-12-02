#!/usr/bin/env python3
"""
Quick test script to verify PDF report generation setup
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate
        print("✓ reportlab imported successfully")
    except ImportError as e:
        print(f"✗ reportlab import failed: {e}")
        print("  Install with: pip install reportlab")
        return False
    
    try:
        from groq_helper import GroqClient
        print("✓ groq_helper imported successfully")
    except ImportError as e:
        print(f"✗ groq_helper import failed: {e}")
        return False
    
    try:
        from config_env import load_environment, get_api_key
        print("✓ config_env imported successfully")
    except ImportError as e:
        print(f"✗ config_env import failed: {e}")
        return False
    
    try:
        from pdf_report_generator import InspectionReportGenerator
        print("✓ pdf_report_generator imported successfully")
    except ImportError as e:
        print(f"✗ pdf_report_generator import failed: {e}")
        return False
    
    return True


def test_environment():
    """Test environment configuration"""
    print("\nTesting environment configuration...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("✗ .env file not found")
        print("  Create one with: cp .env.example .env")
        print("  Then add your GROQ_API_KEY")
        return False
    
    print("✓ .env file exists")
    
    # Try to load environment
    try:
        from config_env import load_environment, get_api_key
        load_environment()
        print("✓ Environment loaded")
        
        # Check for API key
        api_key = get_api_key('GROQ_API_KEY', required=False)
        if api_key:
            masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
            print(f"✓ GROQ_API_KEY found: {masked_key}")
            return True
        else:
            print("✗ GROQ_API_KEY not found in .env")
            print("  Add it with: echo 'GROQ_API_KEY=your_key' >> .env")
            return False
    except Exception as e:
        print(f"✗ Environment test failed: {e}")
        return False


def test_groq_api():
    """Test Groq API connection"""
    print("\nTesting Groq API connection...")
    try:
        from groq_helper import GroqClient
        from config_env import load_environment, get_api_key
        
        load_environment()
        api_key = get_api_key('GROQ_API_KEY', required=False)
        
        if not api_key:
            print("✗ Cannot test API without key")
            return False
        
        client = GroqClient(api_key)
        response = client.chat(
            message="Say 'test successful' in 3 words or less.",
            temperature=0.1,
            max_tokens=10
        )
        
        print(f"✓ Groq API connection successful")
        print(f"  Response: {response}")
        return True
        
    except Exception as e:
        print(f"✗ Groq API test failed: {e}")
        return False


def test_report_generation():
    """Test PDF report generation with minimal data"""
    print("\nTesting PDF report generation...")
    try:
        from pdf_report_generator import InspectionReportGenerator
        
        generator = InspectionReportGenerator(output_dir="test_reports")
        
        # Minimal test data
        test_defects = [
            {
                'type': 'major_crack',
                'confidence': 0.95,
                'location': 'Test Wall',
                'severity': 'high',
                'timestamp': '2025-12-02 14:30:00',
                'image_id': 'TEST_001.jpg'
            }
        ]
        
        test_site_info = {
            'site_name': 'Test Building',
            'location': 'Test Location',
            'inspector_name': 'Test Inspector',
        }
        
        print("  Generating test report (this may take 30-60 seconds)...")
        report_path = generator.generate_comprehensive_report(
            defects_data=test_defects,
            site_info=test_site_info,
            voice_transcripts=[]
        )
        
        if os.path.exists(report_path):
            file_size = os.path.getsize(report_path) / 1024
            print(f"✓ Report generated successfully: {report_path}")
            print(f"  File size: {file_size:.1f} KB")
            
            # Cleanup
            os.remove(report_path)
            if os.path.exists('test_reports') and not os.listdir('test_reports'):
                os.rmdir('test_reports')
            print("✓ Test report cleaned up")
            
            return True
        else:
            print("✗ Report file not found")
            return False
            
    except Exception as e:
        print(f"✗ Report generation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 70)
    print("SiteLenz PDF Report Generator - System Test")
    print("=" * 70)
    
    results = {
        'imports': False,
        'environment': False,
        'groq_api': False,
        'report_generation': False,
    }
    
    # Run tests
    results['imports'] = test_imports()
    
    if results['imports']:
        results['environment'] = test_environment()
    
    if results['environment']:
        results['groq_api'] = test_groq_api()
    
    if results['groq_api']:
        results['report_generation'] = test_report_generation()
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name.replace('_', ' ').title()}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ ALL TESTS PASSED - System is ready!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Run: python pdf_report_generator.py (for full example)")
        print("2. Integrate with your Flask app using api_report_endpoints.py")
        print("3. See PDF_REPORT_GUIDE.md for complete documentation")
        return 0
    else:
        print("✗ SOME TESTS FAILED - Please fix the issues above")
        print("=" * 70)
        print("\nCommon fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Create .env file: cp .env.example .env")
        print("3. Add Groq API key to .env file")
        print("4. Get free key at: https://console.groq.com/")
        return 1


if __name__ == "__main__":
    sys.exit(main())
