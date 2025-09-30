#!/usr/bin/env python3
"""
Simple test script to verify the API endpoints work correctly
"""
import requests
import json

def test_health_endpoint():
    """Test the health check endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Health check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_match_vaga_endpoint():
    """Test the single job matching endpoint"""
    try:
        data = {"descricao": "Engenheiro Civil Junior com conhecimento em AutoCAD e inglês"}
        response = requests.post("http://localhost:8000/match_vaga", data=data)
        print(f"Match vaga: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Top candidatos: {len(result.get('top_candidatos', []))}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Match vaga test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing API endpoints...")
    print("Make sure to run: uvicorn app:app --reload")
    print()
    
    health_ok = test_health_endpoint()
    match_ok = test_match_vaga_endpoint()
    
    if health_ok and match_ok:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")