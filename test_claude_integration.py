#!/usr/bin/env python3
"""
Claude Integration Demo Script
Tests the Claude API integration with a small sample
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_claude_integration():
    """Test Claude API integration with minimal sample"""
    print("🤖 Testing Claude API Integration")
    print("=" * 40)
    
    # Check API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found in .env")
        return False
    
    print("✅ API key found")
    
    # Test imports
    try:
        sys.path.append('src')
        from claude_analyzer import ClaudeAnalyzer
        from data_loader import load_aidev
        print("✅ Dependencies imported")
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test data loading
    try:
        df = load_aidev(sample_size=10)  # Very small sample for testing
        print(f"✅ Data loaded: {len(df)} records")
    except Exception as e:
        print(f"❌ Data loading error: {e}")
        return False
    
    # Test Claude analyzer
    try:
        analyzer = ClaudeAnalyzer()
        print("✅ Claude analyzer initialized")
    except Exception as e:
        print(f"❌ Claude analyzer error: {e}")
        return False
    
    # Test single PR classification
    try:
        sample_pr = df.iloc[0]
        result = analyzer.classify_pr_type(
            title=sample_pr['title'],
            description=str(sample_pr['body'])
        )
        
        print(f"✅ API test successful!")
        print(f"   Sample PR: {sample_pr['title'][:50]}...")
        print(f"   Classification: {result['type']}")
        print(f"   Confidence: {result['confidence']:.2f}")
        print(f"   Reasoning: {result['reasoning'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    """Run the demo"""
    success = test_claude_integration()
    
    if success:
        print("\n🎉 Claude integration working perfectly!")
        print("\n📋 Next steps:")
        print("   1. Run: python run_claude_analysis.py")
        print("   2. Or: jupyter notebook Claude_Enhanced_Analysis.ipynb")
        print("   3. Or: python run_all.py --include-claude")
        
    else:
        print("\n❌ Claude integration test failed")
        print("\n🔧 Troubleshooting:")
        print("   1. Check ANTHROPIC_API_KEY in .env file")
        print("   2. Ensure: pip install -r requirements.txt")
        print("   3. Verify internet connection")
        
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)