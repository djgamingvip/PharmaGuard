#!/usr/bin/env python3
"""Test PharmaGuard with GPT-4 LLM integration"""

import requests
import json
import time

BACKEND_URL = "http://127.0.0.1:5000"

print("🧬 PharmaGuard - GPT-4 Integration Test\n")
print("="*60)

# Test 1: Single drug with GPT-4 explanation
print("\n📊 Test 1: CODEINE Analysis with GPT-4")
print("-"*60)

with open("sample_vcfs/sample1.vcf", 'rb') as f:
    files = {'vcf': f}
    data = {'drugs': 'CODEINE'}
    
    start_time = time.time()
    response = requests.post(f"{BACKEND_URL}/analyze", files=files, data=data, timeout=60)
    elapsed = time.time() - start_time

if response.status_code == 200:
    result = response.json()
    print(f"✅ Analysis completed in {elapsed:.2f}s\n")
    
    print(f"Patient: {result['patient_id']}")
    print(f"Drug: {result['drug']}")
    print(f"Risk: {result['risk_assessment']['risk_label']}")
    print(f"Phenotype: {result['pharmacogenomic_profile']['phenotype']}")
    print(f"Diplotype: {result['pharmacogenomic_profile']['diplotype']}")
    print(f"Confidence: {result['risk_assessment']['confidence_score']*100:.0f}%")
    
    print(f"\n🤖 AI-Generated Explanation:")
    print("-"*60)
    exp = result['llm_generated_explanation']
    print(f"\n📝 Summary:\n{exp['summary']}")
    print(f"\n🔬 Mechanism:\n{exp['mechanism']}")
    print(f"\n🧬 Variant Impact:\n{exp['variant_impact']}")
    
    print(f"\n💊 Clinical Recommendation:")
    print("-"*60)
    print(result['clinical_recommendation']['recommendation'])
    if result['clinical_recommendation']['alternative_drugs']:
        print(f"\nAlternatives: {', '.join(result['clinical_recommendation']['alternative_drugs'])}")
    
    # Check if explanation looks like GPT-4 or fallback
    if len(exp['summary']) > 100 and 'genetic analysis' not in exp['summary'].lower():
        print("\n✅ GPT-4 API is working! (Detailed explanation generated)")
    else:
        print("\n⚠️  Using fallback explanation (GPT-4 may not be called)")
        print("   This is normal if API key is invalid or rate limited")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)

# Test 2: Multi-drug analysis
print("\n\n📊 Test 2: Multi-Drug Analysis")
print("-"*60)

with open("sample_vcfs/sample2.vcf", 'rb') as f:
    files = {'vcf': f}
    data = {'drugs': 'CLOPIDOGREL,AZATHIOPRINE'}
    
    start_time = time.time()
    response = requests.post(f"{BACKEND_URL}/analyze", files=files, data=data, timeout=60)
    elapsed = time.time() - start_time

if response.status_code == 200:
    results = response.json()
    print(f"✅ Analysis completed in {elapsed:.2f}s\n")
    
    for i, result in enumerate(results, 1):
        print(f"\n--- Drug {i}: {result['drug']} ---")
        print(f"Risk: {result['risk_assessment']['risk_label']}")
        print(f"Phenotype: {result['pharmacogenomic_profile']['phenotype']}")
        print(f"Summary: {result['llm_generated_explanation']['summary'][:100]}...")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)

# Test 3: All supported drugs
print("\n\n📊 Test 3: All Supported Drugs")
print("-"*60)

with open("sample_vcfs/sample1.vcf", 'rb') as f:
    files = {'vcf': f}
    data = {'drugs': 'CODEINE,WARFARIN,CLOPIDOGREL,SIMVASTATIN'}
    
    start_time = time.time()
    response = requests.post(f"{BACKEND_URL}/analyze", files=files, data=data, timeout=90)
    elapsed = time.time() - start_time

if response.status_code == 200:
    results = response.json()
    print(f"✅ Analysis completed in {elapsed:.2f}s\n")
    
    print("Risk Summary:")
    for result in results:
        risk = result['risk_assessment']['risk_label']
        emoji = "🟢" if risk == "Safe" else "🟡" if risk == "Adjust Dosage" else "🔴"
        print(f"{emoji} {result['drug']}: {risk}")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)

print("\n" + "="*60)
print("✅ All tests completed!")
print("="*60)
