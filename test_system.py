#!/usr/bin/env python3
"""
PharmaGuard System Test Script
Tests backend functionality and schema compliance
"""

import requests
import json
import sys
from pathlib import Path

# Configuration
BACKEND_URL = "http://localhost:5000"
SAMPLE_VCF_DIR = Path("sample_vcfs")

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(msg):
    print(f"{GREEN}✓ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}✗ {msg}{RESET}")

def print_info(msg):
    print(f"{BLUE}ℹ {msg}{RESET}")

def print_warning(msg):
    print(f"{YELLOW}⚠ {msg}{RESET}")

def test_health_endpoint():
    """Test /health endpoint"""
    print_info("Testing /health endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'ok':
                print_success("Health check passed")
                return True
        print_error(f"Health check failed: {response.status_code}")
        return False
    except Exception as e:
        print_error(f"Health check failed: {str(e)}")
        return False

def test_drugs_endpoint():
    """Test /drugs endpoint"""
    print_info("Testing /drugs endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/drugs", timeout=5)
        if response.status_code == 200:
            data = response.json()
            drugs = data.get('supported_drugs', [])
            expected = ['CODEINE', 'WARFARIN', 'CLOPIDOGREL', 'SIMVASTATIN', 'AZATHIOPRINE', 'FLUOROURACIL']
            if set(drugs) == set(expected):
                print_success(f"Drugs endpoint passed: {len(drugs)} drugs supported")
                return True
            else:
                print_error(f"Drug list mismatch. Expected: {expected}, Got: {drugs}")
                return False
        print_error(f"Drugs endpoint failed: {response.status_code}")
        return False
    except Exception as e:
        print_error(f"Drugs endpoint failed: {str(e)}")
        return False

def validate_schema(result):
    """Validate result against required schema"""
    required_fields = {
        'patient_id': str,
        'drug': str,
        'timestamp': str,
        'risk_assessment': dict,
        'pharmacogenomic_profile': dict,
        'clinical_recommendation': dict,
        'llm_generated_explanation': dict,
        'quality_metrics': dict
    }
    
    for field, field_type in required_fields.items():
        if field not in result:
            print_error(f"Missing required field: {field}")
            return False
        if not isinstance(result[field], field_type):
            print_error(f"Field {field} has wrong type. Expected {field_type}, got {type(result[field])}")
            return False
    
    # Validate nested fields
    risk_fields = ['risk_label', 'confidence_score', 'severity']
    for field in risk_fields:
        if field not in result['risk_assessment']:
            print_error(f"Missing risk_assessment field: {field}")
            return False
    
    profile_fields = ['primary_gene', 'diplotype', 'phenotype', 'detected_variants']
    for field in profile_fields:
        if field not in result['pharmacogenomic_profile']:
            print_error(f"Missing pharmacogenomic_profile field: {field}")
            return False
    
    recommendation_fields = ['guideline_source', 'recommendation', 'alternative_drugs']
    for field in recommendation_fields:
        if field not in result['clinical_recommendation']:
            print_error(f"Missing clinical_recommendation field: {field}")
            return False
    
    explanation_fields = ['summary', 'mechanism', 'variant_impact']
    for field in explanation_fields:
        if field not in result['llm_generated_explanation']:
            print_error(f"Missing llm_generated_explanation field: {field}")
            return False
    
    quality_fields = ['vcf_parsing_success', 'missing_annotations', 'confidence_level']
    for field in quality_fields:
        if field not in result['quality_metrics']:
            print_error(f"Missing quality_metrics field: {field}")
            return False
    
    # Validate risk_label values
    valid_risk_labels = ['Safe', 'Adjust Dosage', 'Toxic', 'Ineffective', 'Unknown']
    if result['risk_assessment']['risk_label'] not in valid_risk_labels:
        print_error(f"Invalid risk_label: {result['risk_assessment']['risk_label']}")
        return False
    
    print_success("Schema validation passed")
    return True

def test_analyze_endpoint(vcf_file, drugs):
    """Test /analyze endpoint with VCF file"""
    print_info(f"Testing /analyze with {vcf_file.name} and drugs: {drugs}")
    
    if not vcf_file.exists():
        print_error(f"VCF file not found: {vcf_file}")
        return False
    
    try:
        with open(vcf_file, 'rb') as f:
            files = {'vcf': f}
            data = {'drugs': drugs}
            response = requests.post(f"{BACKEND_URL}/analyze", files=files, data=data, timeout=30)
        
        if response.status_code != 200:
            print_error(f"Analysis failed: {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
        
        result = response.json()
        
        # Handle single or multiple results
        results = result if isinstance(result, list) else [result]
        
        print_success(f"Analysis completed: {len(results)} result(s)")
        
        # Validate each result
        all_valid = True
        for i, res in enumerate(results):
            print_info(f"Validating result {i+1}/{len(results)}...")
            if not validate_schema(res):
                all_valid = False
            else:
                print_info(f"  Drug: {res['drug']}")
                print_info(f"  Risk: {res['risk_assessment']['risk_label']}")
                print_info(f"  Phenotype: {res['pharmacogenomic_profile']['phenotype']}")
                print_info(f"  Confidence: {res['risk_assessment']['confidence_score']}")
        
        return all_valid
        
    except Exception as e:
        print_error(f"Analysis failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}PharmaGuard System Test Suite{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    print_info(f"Backend URL: {BACKEND_URL}\n")
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Health endpoint
    tests_total += 1
    if test_health_endpoint():
        tests_passed += 1
    print()
    
    # Test 2: Drugs endpoint
    tests_total += 1
    if test_drugs_endpoint():
        tests_passed += 1
    print()
    
    # Test 3: Analyze with sample1.vcf
    tests_total += 1
    sample1 = SAMPLE_VCF_DIR / "sample1.vcf"
    if test_analyze_endpoint(sample1, "CODEINE"):
        tests_passed += 1
    print()
    
    # Test 4: Analyze with sample2.vcf (multi-drug)
    tests_total += 1
    sample2 = SAMPLE_VCF_DIR / "sample2.vcf"
    if test_analyze_endpoint(sample2, "CLOPIDOGREL,AZATHIOPRINE"):
        tests_passed += 1
    print()
    
    # Summary
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Test Summary{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"Tests Passed: {tests_passed}/{tests_total}")
    
    if tests_passed == tests_total:
        print_success("\n🎉 All tests passed! System is ready for deployment.")
        return 0
    else:
        print_error(f"\n❌ {tests_total - tests_passed} test(s) failed. Please fix issues before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
