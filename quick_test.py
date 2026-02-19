#!/usr/bin/env python3
"""Quick test script to analyze a VCF file"""

import requests
import json

# Configuration
BACKEND_URL = "http://127.0.0.1:5000"
VCF_FILE = "sample_vcfs/sample1.vcf"
DRUGS = "CODEINE"

print("🧬 PharmaGuard Quick Test\n")
print(f"Backend: {BACKEND_URL}")
print(f"VCF File: {VCF_FILE}")
print(f"Drugs: {DRUGS}\n")

# Test analysis
print("📊 Analyzing...")
with open(VCF_FILE, 'rb') as f:
    files = {'vcf': f}
    data = {'drugs': DRUGS}
    response = requests.post(f"{BACKEND_URL}/analyze", files=files, data=data)

if response.status_code == 200:
    result = response.json()
    print("✅ Analysis Complete!\n")
    print(json.dumps(result, indent=2))
    
    print("\n" + "="*60)
    print("📋 Summary:")
    print("="*60)
    print(f"Patient ID: {result['patient_id']}")
    print(f"Drug: {result['drug']}")
    print(f"Risk: {result['risk_assessment']['risk_label']}")
    print(f"Severity: {result['risk_assessment']['severity']}")
    print(f"Phenotype: {result['pharmacogenomic_profile']['phenotype']}")
    print(f"Diplotype: {result['pharmacogenomic_profile']['diplotype']}")
    print(f"Confidence: {result['risk_assessment']['confidence_score']*100:.0f}%")
    print(f"\n💡 Recommendation:")
    print(result['clinical_recommendation']['recommendation'])
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
