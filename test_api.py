#!/usr/bin/env python3
"""
Test script to verify the API endpoints are properly configured.
This script checks that all endpoints exist and have correct methods.
"""

from main import app
import json


def test_endpoints_configured():
    """Test that all expected endpoints are configured"""
    routes = {}
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            path = route.path
            methods = sorted(route.methods - {'HEAD', 'OPTIONS'})  # Remove HEAD and OPTIONS
            if path not in routes:
                routes[path] = []
            routes[path].extend(methods)
    
    # Expected endpoints
    expected = {
        '/': ['GET'],
        '/health': ['GET'],
        '/notes/': ['GET', 'POST'],
        '/notes/{note_id}': ['DELETE', 'GET', 'PUT'],
        '/notes/{note_id}/versions': ['GET'],
        '/notes/{note_id}/versions/{version_number}': ['GET'],
    }
    
    print("Checking expected endpoints:")
    all_ok = True
    for path, methods in expected.items():
        if path in routes:
            actual_methods = sorted(set(routes[path]))
            expected_methods = sorted(methods)
            if actual_methods == expected_methods:
                print(f"  ✓ {path:50} {', '.join(expected_methods)}")
            else:
                print(f"  ✗ {path:50} Expected: {expected_methods}, Got: {actual_methods}")
                all_ok = False
        else:
            print(f"  ✗ {path:50} MISSING")
            all_ok = False
    
    return all_ok


def list_all_endpoints():
    """List all configured endpoints"""
    print("\n📋 All configured endpoints:")
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            # Filter out HEAD and OPTIONS for cleaner output
            methods = sorted(route.methods - {'HEAD', 'OPTIONS'})
            if methods:  # Only show if there are methods left
                methods_str = ', '.join(methods)
                print(f"  {methods_str:20} {route.path}")


def verify_app_metadata():
    """Verify FastAPI app metadata"""
    print("\n📝 API Metadata:")
    print(f"  Title: {app.title}")
    print(f"  Description: {app.description}")
    print(f"  Version: {app.version}")


def main():
    print("=" * 70)
    print("FastAPI Notes API - Endpoint Verification")
    print("=" * 70)
    print()
    
    verify_app_metadata()
    print()
    
    success = test_endpoints_configured()
    print()
    
    list_all_endpoints()
    
    print()
    print("=" * 70)
    if success:
        print("✅ All endpoint checks passed!")
    else:
        print("❌ Some endpoints are missing or misconfigured")
    print("=" * 70)
    print()
    print("Note: Database-dependent operations require PostgreSQL to be running.")
    print("See README.md for setup instructions.")


if __name__ == "__main__":
    main()
