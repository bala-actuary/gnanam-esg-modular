#!/usr/bin/env python3
"""
Integration Test Runner for Gnanam ESG Modular Platform

This script provides a command-line interface to run different types of
integration tests for the modular ESG platform.
"""

import asyncio
import argparse
import sys
import os
from datetime import datetime
from test_framework import IntegrationTestRunner, TestType

async def run_specific_test_type(test_type: str):
    """Run tests of a specific type"""
    runner = IntegrationTestRunner()
    
    print(f"🧪 Running {test_type} tests...")
    print("=" * 50)
    
    if test_type == "unit":
        results = await runner._run_unit_tests()
    elif test_type == "workflow":
        results = await runner._run_workflow_tests()
    elif test_type == "performance":
        results = await runner._run_performance_tests()
    elif test_type == "api":
        results = await runner._run_api_tests()
    else:
        print(f"❌ Unknown test type: {test_type}")
        return
    
    # Calculate summary
    summary = runner._calculate_summary(results)
    
    print(f"\n📊 {test_type.title()} Test Summary:")
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}")
    print(f"Success Rate: {summary['success_rate']:.1f}%")
    print(f"Total Duration: {summary['total_duration']:.2f}s")
    
    # Save results
    await runner._save_results(results, summary)
    
    if summary['failed'] == 0:
        print(f"\n✅ All {test_type} tests passed!")
    else:
        print(f"\n❌ {summary['failed']} {test_type} tests failed.")

async def run_all_tests():
    """Run all integration tests"""
    runner = IntegrationTestRunner()
    results = await runner.run_all_tests()
    
    summary = results["summary"]
    
    print(f"\n📊 Complete Test Summary:")
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}")
    print(f"Success Rate: {summary['success_rate']:.1f}%")
    print(f"Total Duration: {summary['total_duration']:.2f}s")
    
    if summary['failed'] == 0:
        print("\n🎉 All tests passed! Integration testing completed successfully.")
    else:
        print(f"\n⚠️  {summary['failed']} tests failed. Please review the results.")
    
    print(f"\n📁 Results saved to:")
    print(f"- test_results.json")
    print(f"- test_summary.md")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Gnanam ESG Integration Test Runner")
    parser.add_argument(
        "--test-type",
        choices=["unit", "workflow", "performance", "api", "all"],
        default="all",
        help="Type of tests to run (default: all)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    print("🚀 Gnanam ESG Integration Test Runner")
    print("=" * 50)
    print(f"Test Type: {args.test_type}")
    print(f"Timestamp: {datetime.utcnow().isoformat()}")
    print()
    
    try:
        if args.test_type == "all":
            asyncio.run(run_all_tests())
        else:
            asyncio.run(run_specific_test_type(args.test_type))
    except KeyboardInterrupt:
        print("\n⏹️  Test execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 