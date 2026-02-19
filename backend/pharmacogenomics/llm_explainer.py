import openai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI with the best model
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_explanation(patient_id, drug, risk_label, phenotype, variants, gene):
    """Generate LLM explanation using GPT-3.5-turbo with variant citations following exact schema."""
    
    # If no API key, return structured fallback
    if not openai.api_key or openai.api_key == 'your_openai_api_key_here':
        return generate_fallback_explanation(patient_id, drug, risk_label, phenotype, variants, gene)
    
    # Handle empty variants list
    if not variants or len(variants) == 0:
        return generate_fallback_explanation(patient_id, drug, risk_label, phenotype, [], gene)
    
    # Build detailed variant information
    variant_details = []
    for v in variants:
        try:
            variant_details.append(
                f"- {v.get('rsid', 'unknown')} in {v.get('gene', gene)} (star allele: {v.get('star_allele', 'unknown')}, "
                f"position: chr{v.get('chrom', '?')}:{v.get('pos', '?')}, quality: {v.get('quality', 'N/A')})"
            )
        except Exception as e:
            print(f"Error processing variant: {e}")
            continue
    
    if not variant_details:
        return generate_fallback_explanation(patient_id, drug, risk_label, phenotype, variants, gene)
    
    variant_str = "\n".join(variant_details)
    
    # Create comprehensive prompt for GPT-4
    prompt = f"""You are a board-certified clinical pharmacogenomics expert providing a detailed risk assessment.

PATIENT INFORMATION:
- Patient ID: {patient_id}
- Drug Prescribed: {drug}
- Risk Classification: {risk_label}
- Primary Gene: {gene}
- Metabolizer Phenotype: {phenotype}

GENETIC VARIANTS DETECTED:
{variant_str}

TASK:
Generate a comprehensive clinical explanation in JSON format with these exact keys:

1. "summary": A clear 2-3 sentence summary explaining the overall risk assessment and what it means for this patient.

2. "mechanism": A detailed explanation of the biological mechanism - how these specific genetic variants affect the {gene} enzyme's function and consequently alter {drug} metabolism and efficacy.

3. "variant_impact": Specific analysis of how each detected variant (cite by rsID) contributes to the overall phenotype and risk profile.

REQUIREMENTS:
- Be scientifically accurate and cite specific variants by rsID
- Explain in terms understandable to healthcare providers
- Reference CPIC guidelines where applicable
- Avoid speculation - only state what is supported by evidence
- Return ONLY valid JSON, no markdown formatting

Example format:
{{
  "summary": "Patient exhibits...",
  "mechanism": "The {gene} gene encodes...",
  "variant_impact": "The {v['rsid']} variant..."
}}"""

    try:
        # Use GPT-3.5-turbo (more widely available) or GPT-4 if available
        model = "gpt-3.5-turbo"  # Change to "gpt-4" if you have access
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "system", 
                    "content": "You are a clinical pharmacogenomics expert. Provide accurate, evidence-based explanations. Always respond with valid JSON only, no markdown code blocks."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.2,  # Lower temperature for more consistent, factual responses
            max_tokens=800,
            top_p=0.9
        )
        
        content = response.choices[0].message.content.strip()
        
        # Clean up markdown formatting if present
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0].strip()
        elif '```' in content:
            content = content.split('```')[1].split('```')[0].strip()
        
        # Parse JSON response
        explanation = json.loads(content)
        
        # Validate and ensure all required keys exist
        required_keys = ['summary', 'mechanism', 'variant_impact']
        for key in required_keys:
            if key not in explanation or not explanation[key]:
                explanation[key] = generate_fallback_field(key, drug, gene, phenotype, risk_label, variants)
        
        return explanation
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Content received: {content[:200] if 'content' in locals() else 'No content'}")
        return generate_fallback_explanation(patient_id, drug, risk_label, phenotype, variants, gene)
        
    except openai.error.AuthenticationError:
        print("OpenAI API authentication failed - check API key")
        return generate_fallback_explanation(patient_id, drug, risk_label, phenotype, variants, gene)
        
    except openai.error.RateLimitError:
        print("OpenAI API rate limit exceeded")
        return generate_fallback_explanation(patient_id, drug, risk_label, phenotype, variants, gene)
        
    except Exception as e:
        print(f"Error generating LLM explanation: {type(e).__name__}: {str(e)}")
        return generate_fallback_explanation(patient_id, drug, risk_label, phenotype, variants, gene)


def generate_fallback_field(field, drug, gene, phenotype, risk_label, variants):
    """Generate a specific fallback field."""
    variant_list = ', '.join([v['rsid'] for v in variants]) if variants else 'none'
    
    fallbacks = {
        'summary': f"Patient has {phenotype} phenotype for {gene}, resulting in {risk_label} risk classification for {drug}. Genetic testing detected {len(variants)} variant(s) affecting drug metabolism.",
        'mechanism': f"The {gene} gene encodes an enzyme critical for {drug} metabolism. The patient's {phenotype} phenotype indicates altered enzyme activity, which affects how the body processes this medication. This can lead to either reduced drug efficacy or increased risk of adverse effects.",
        'variant_impact': f"Detected variants ({variant_list}) in {gene} contribute to the {phenotype} metabolizer status. These genetic variations alter enzyme function, directly impacting {drug} pharmacokinetics and clinical response."
    }
    
    return fallbacks.get(field, f"Information about {field} not available.")


def generate_fallback_explanation(patient_id, drug, risk_label, phenotype, variants, gene):
    """Generate comprehensive fallback explanation when LLM is unavailable."""
    variant_list = ', '.join([v['rsid'] for v in variants]) if variants else 'none detected'
    
    # Drug-specific mechanism information
    drug_mechanisms = {
        'CODEINE': f"{gene} converts codeine to morphine (active form). {phenotype} metabolizers may experience altered pain relief.",
        'WARFARIN': f"{gene} metabolizes warfarin. {phenotype} status affects dosing requirements and bleeding risk.",
        'CLOPIDOGREL': f"{gene} activates clopidogrel to its active form. {phenotype} metabolizers may have reduced antiplatelet effect.",
        'SIMVASTATIN': f"{gene} transporter affects simvastatin uptake. {phenotype} status influences myopathy risk.",
        'AZATHIOPRINE': f"{gene} metabolizes azathioprine. {phenotype} metabolizers have altered toxicity risk.",
        'FLUOROURACIL': f"{gene} metabolizes fluorouracil. {phenotype} status significantly affects toxicity risk."
    }
    
    mechanism = drug_mechanisms.get(drug, f"{gene} affects {drug} metabolism. {phenotype} status alters drug response.")
    
    return {
        "summary": f"Genetic analysis reveals {phenotype} phenotype for {gene}, classifying {drug} risk as {risk_label}. This assessment is based on {len(variants)} detected variant(s) that affect drug metabolism and clinical response.",
        "mechanism": mechanism,
        "variant_impact": f"Variants identified: {variant_list}. These genetic variations in {gene} modify enzyme activity, leading to the {phenotype} metabolizer classification and corresponding {risk_label} risk profile for {drug} therapy."
    }