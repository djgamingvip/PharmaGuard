#!/usr/bin/env python3
"""Test with sample2.vcf"""

import requests
import json

BACKEND_URL = "http://127.0.0.1:5000"

print("🧬 Testing sample2.vcf with multiple drugs\n")

# Test with drugs that ARE in sample2.vcf
with open("sample_vcfs/sample2.vcf", 'rb') as f:
    files = {'vcf': f}
    data = {'drugs': 'CLOPIDOGREL,AZATHIOPRINE'}
    
    response = requests.post(f"{BACKEND_URL}/analyze", files=files, data=data, timeout=30)

if response.status_code == 200:
    results = response.json()
    print("✅ Success!\n")
    for result in results:
        print(f"Drug: {result['drug']}")
        print(f"Risk: {result['risk_assessment']['risk_label']}")
        print(f"Phenotype: {result['pharmacogenomic_profile']['phenotype']}")
        print(f"Diplotype: {result['pharmacogenomic_profile']['diplotype']}")
        print()
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)

# Now test with a drug NOT in sample2.vcf (should handle gracefully)
print("\n" + "="*60)
print("Testing with drug NOT in VCF (CODEINE)...")
print("="*60 + "\n")

with open("sample_vcfs/sample2.vcf", 'rb') as f:
    files = {'vcf': f}
    data = {'drugs': 'CODEINE'}
    
    response = requests.post(f"{BACKEND_URL}/analyze", files=files, data=data, timeout=30)

if response.status_code == 200:
    result = response.json()
    print("✅ Handled gracefully!\n")
    print(f"Drug: {result['drug']}")
    print(f"Risk: {result['risk_assessment']['risk_label']}")
    print(f"Phenotype: {result['pharmacogenomic_profile']['phenotype']}")
    print(f"Diplotype: {result['pharmacogenomic_profile']['diplotype']}")
    print(f"Detected Variants: {len(result['pharmacogenomic_profile']['detected_variants'])}")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
