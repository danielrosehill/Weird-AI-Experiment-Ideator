#!/usr/bin/env python3
"""Quick test to verify the system is properly configured."""
import os
import sys

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        import crewai
        print("✓ crewai imported successfully")

        from langchain_openai import ChatOpenAI
        print("✓ langchain_openai imported successfully")

        from src.config import OPENROUTER_API_KEY, NUM_IDEAS
        print(f"✓ Configuration loaded (NUM_IDEAS={NUM_IDEAS})")

        from src.agents import create_generator_agent
        print("✓ Agent modules loaded")

        from src.tasks import create_generation_task
        print("✓ Task modules loaded")

        from src.crew import create_ideation_crew
        print("✓ Crew module loaded")

        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_key():
    """Test that API key is configured."""
    print("\nTesting API key configuration...")
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        print("✗ OPENROUTER_API_KEY not found in environment")
        print("  Please copy .env.example to .env and add your API key")
        return False

    if api_key == "your_api_key_here":
        print("✗ OPENROUTER_API_KEY is still set to placeholder value")
        print("  Please update .env with your actual API key")
        return False

    print(f"✓ API key configured (length: {len(api_key)} chars)")
    return True


def test_agent_creation():
    """Test that agents can be created."""
    print("\nTesting agent creation...")
    try:
        from src.agents import create_generator_agent
        agent = create_generator_agent()
        print(f"✓ Generator agent created: {agent.role}")
        return True
    except Exception as e:
        print(f"✗ Agent creation error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 80)
    print("Weird AI Experiment Ideator - Setup Test")
    print("=" * 80)

    results = []

    results.append(("Module Imports", test_imports()))
    results.append(("API Key Configuration", test_api_key()))

    # Only test agent creation if imports worked
    if results[0][1]:
        results.append(("Agent Creation", test_agent_creation()))

    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)

    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")

    all_passed = all(result[1] for result in results)

    if all_passed:
        print("\n🎉 All tests passed! The system is ready to use.")
        print("\nTo run an ideation session:")
        print("  python main.py")
    else:
        print("\n❌ Some tests failed. Please fix the issues above before running.")
        sys.exit(1)


if __name__ == "__main__":
    main()
