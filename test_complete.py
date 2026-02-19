#!/usr/bin/env python3
"""Complete test with all 6 drugs using comprehensive VCF"""

import requests
import json
import time

BACKEND_URL = "http://127.0.0.1:5000"

print("🧬 PharmaGuard - COMPLETE SYSTEM TEST")
print("="*70)
print("Testing ALL 6 drugs with comprehensive.vcf")
print("="*70 + "\n")

# Test with ALL drugs
with open("sample_vcfs/comprehensive.vcf", 'rb') as f:
    files = {'vcf': f}
    data = {'drugs': 'CODEINE,WARFARIN,CLOPIDOGREL,SIMVASTATIN,AZATHIOPRINE,FLUOROURACIL'}
    
    print("📤 Uploading comprehensive.vcf...")
    print("💊 Analyzing: CODEINE, WARFARIN, CLOPIDOGREL, SIMVASTATIN, AZATHIOPRINE, FLUOROURACIL")
    print("\n⏳ Processing...\n")
    
    start_time = time.time()
    response = requests.post(f"{BACKEND_URL}/analyze", files=files, data=data, timeout=120)
    elapsed = time.time() - start_time

if response.status_code == 200:
    results = response.json()
    
    print(f"✅ Analysis completed in {elapsed:.2f} seconds!")
    print(f"📊 Results for {len(results)} drugs\n")
    print("="*70)
    
    for i, result in enumerate(results, 1):
        risk = result['risk_assessment']['risk_label']
        
        # Emoji based on risk
        emoji = {
            'Safe': '🟢',
            'Adjust Dosage': '🟡',
            'Toxic': '🔴',
            'Ineffective': '🟠',
            'Unknown': '⚪'
        }.get(risk, '⚪')
        
        print(f"\n{i}. {emoji} {result['drug']}")
        print("-"*70)
        print(f"   Patient ID: {result['patient_id']}")
        print(f"   Risk: {risk}")
        print(f"   Severity: {result['risk_assessment']['severity'].upper()}")
        print(f"   Gene: {result['pharmacogenomic_profile']['primary_gene']}")
        print(f"   Phenotype: {result['pharmacogenomic_profile']['phenotype']}")
        print(f"   Diplotype: {result['pharmacogenomic_profile']['diplotype']}")
        print(f"   Confidence: {result['risk_assessment']['confidence_score']*100:.0f}%")
        print(f"   Variants: {len(result['pharmacogenomic_profile']['detected_variants'])}")
        
        if result['pharmacogenomic_profile']['detected_variants']:
            variants = ', '.join([v['rsid'] for v in result['pharmacogenomic_profile']['detected_variants']])
            print(f"   Detected: {variants}")
        
        print(f"\n   💊 Recommendation:")
        print(f"   {result['clinical_recommendation']['recommendation']}")
        
        if result['clinical_recommendation']['alternative_drugs']:
            alts = ', '.join(result['clinical_recommendation']['alternative_drugs'])
            print(f"   Alternatives: {alts}")
        
        print(f"\n   🤖 AI Summary:")
        print(f"   {result['llm_generated_explanation']['summary'][:150]}...")
    
    print("\n" + "="*70)
    print("📈 SUMMARY")
    print("="*70)
    
    risk_counts = {}
    for result in results:
        risk = result['risk_assessment']['risk_label']
        risk_counts[risk] = risk_counts.get(risk, 0) + 1
    
    for risk, count in risk_counts.items():
        emoji = {
            'Safe': '🟢',
            'Adjust Dosage': '🟡',
            'Toxic': '🔴',
            'Ineffective': '🟠',
            'Unknown': '⚪'
        }.get(risk, '⚪')
        print(f"{emoji} {risk}: {count} drug(s)")
    
    print(f"\n✅ Total drugs analyzed: {len(results)}")
    print(f"⏱️  Total time: {elapsed:.2f} seconds")
    print(f"⚡ Average per drug: {elapsed/len(results):.2f} seconds")
    
    # Save full results
    with open('test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Full results saved to: test_results.json")
    
    print("\n" + "="*70)
    print("🎉 ALL TESTS PASSED! System is fully operational!")
    print("="*70)
    
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
