from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from pharmacogenomics.vcf_parser import parse_vcf
from pharmacogenomics.rules_engine import determine_phenotype, assess_risk
from pharmacogenomics.cpic_mappings import DRUG_GENE_MAP
from pharmacogenomics.llm_explainer import generate_explanation
import tempfile

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

SUPPORTED_DRUGS = ['CODEINE', 'WARFARIN', 'CLOPIDOGREL', 'SIMVASTATIN', 'AZATHIOPRINE', 'FLUOROURACIL']

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze VCF file and return pharmacogenomic risk assessment."""
    try:
        # Validate drug input
        drugs_input = request.form.get('drugs', '').strip()
        if not drugs_input:
            return jsonify({'error': 'No drugs specified'}), 400
        
        drugs = [d.strip().upper() for d in drugs_input.split(',') if d.strip()]
        
        # Validate VCF file
        vcf_file = request.files.get('vcf')
        if not vcf_file:
            return jsonify({'error': 'No VCF file uploaded'}), 400
        
        if not vcf_file.filename.endswith('.vcf'):
            return jsonify({'error': 'Invalid file format. Expected .vcf file'}), 400
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.vcf', mode='w', encoding='utf-8') as tmp:
            content = vcf_file.stream.read().decode('utf-8')
            tmp.write(content)
            tmp_path = tmp.name
        
        # Parse VCF
        try:
            parse_result = parse_vcf(tmp_path)
            variants = parse_result['variants']
            vcf_version = parse_result['vcf_version']
            missing_annotations = parse_result['missing_annotations']
        except Exception as e:
            os.unlink(tmp_path)
            return jsonify({'error': f'VCF parsing failed: {str(e)}'}), 400
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        
        if not variants:
            return jsonify({
                'error': 'No pharmacogenomic variants found in VCF',
                'message': 'VCF must contain variants in genes: CYP2D6, CYP2C19, CYP2C9, SLCO1B1, TPMT, DPYD'
            }), 400
        
        # Group variants by gene
        gene_variants = {}
        for v in variants:
            gene = v['gene']
            if gene not in gene_variants:
                gene_variants[gene] = []
            gene_variants[gene].append(v)
        
        # Process each drug
        results = []
        patient_id = f"PATIENT_{uuid.uuid4().hex[:8].upper()}"
        
        for drug in drugs:
            # Validate drug support
            if drug not in SUPPORTED_DRUGS:
                results.append({
                    'patient_id': patient_id,
                    'drug': drug,
                    'timestamp': datetime.utcnow().isoformat() + 'Z',
                    'error': f'Unsupported drug. Supported drugs: {", ".join(SUPPORTED_DRUGS)}',
                    'risk_assessment': {
                        'risk_label': 'Unknown',
                        'confidence_score': 0.0,
                        'severity': 'unknown'
                    }
                })
                continue
            
            # Get primary gene for drug
            gene = DRUG_GENE_MAP[drug]
            variants_for_gene = gene_variants.get(gene, [])
            
            # Determine phenotype and risk
            if not variants_for_gene:
                phenotype = 'Unknown'
                diplotype = 'Unknown'
                risk_label, severity, recommendation, alternatives = assess_risk(drug, phenotype)
                confidence = 0.5
                detected = []
                # Use empty list for explanation when no variants
                explanation_variants = []
            else:
                # Extract star alleles
                star_alleles = [v['star_allele'] for v in variants_for_gene if v['star_allele']]
                
                # Determine diplotype
                if len(star_alleles) >= 2:
                    diplotype = f"{star_alleles[0]}/{star_alleles[1]}"
                elif len(star_alleles) == 1:
                    diplotype = f"{star_alleles[0]}/*1"  # Assume wild-type for missing allele
                else:
                    diplotype = 'Unknown'
                
                # Determine phenotype
                phenotype = determine_phenotype(gene, star_alleles)
                
                # Assess risk
                risk_label, severity, recommendation, alternatives = assess_risk(drug, phenotype)
                
                # Calculate confidence based on variant quality
                avg_quality = sum([v['quality'] for v in variants_for_gene]) / len(variants_for_gene)
                confidence = min(0.95, 0.7 + (avg_quality / 100) * 0.25)
                
                # Build detected variants list
                detected = [{
                    'rsid': v['rsid'],
                    'gene': v['gene'],
                    'allele': v['star_allele']
                } for v in variants_for_gene]
                
                # Use variants for explanation
                explanation_variants = variants_for_gene
            
            # Generate LLM explanation
            explanation = generate_explanation(patient_id, drug, risk_label, phenotype, explanation_variants, gene)
            
            # Build output JSON matching EXACT schema
            result = {
                'patient_id': patient_id,
                'drug': drug,
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'risk_assessment': {
                    'risk_label': risk_label,
                    'confidence_score': round(confidence, 2),
                    'severity': severity
                },
                'pharmacogenomic_profile': {
                    'primary_gene': gene,
                    'diplotype': diplotype,
                    'phenotype': phenotype,
                    'detected_variants': detected
                },
                'clinical_recommendation': {
                    'guideline_source': 'CPIC',
                    'recommendation': recommendation,
                    'alternative_drugs': alternatives
                },
                'llm_generated_explanation': explanation,
                'quality_metrics': {
                    'vcf_parsing_success': True,
                    'missing_annotations': missing_annotations,
                    'confidence_level': 'high' if confidence > 0.8 else 'medium' if confidence > 0.5 else 'low'
                }
            }
            results.append(result)
        
        # Return single object if one drug, array if multiple
        return jsonify(results if len(results) > 1 else results[0]), 200
    
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/', methods=['GET'])
def index():
    """API information endpoint."""
    return jsonify({
        'service': 'PharmaGuard API',
        'version': '1.0.0',
        'description': 'Pharmacogenomic Risk Prediction System',
        'endpoints': {
            'GET /': 'API information',
            'GET /health': 'Health check',
            'GET /drugs': 'List supported drugs',
            'POST /analyze': 'Analyze VCF file (form-data: vcf, drugs)'
        },
        'supported_drugs': SUPPORTED_DRUGS,
        'supported_genes': ['CYP2D6', 'CYP2C19', 'CYP2C9', 'SLCO1B1', 'TPMT', 'DPYD'],
        'documentation': 'See README.md for full API documentation'
    }), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'service': 'PharmaGuard API',
        'version': '1.0.0'
    }), 200

@app.route('/drugs', methods=['GET'])
def list_drugs():
    """List supported drugs."""
    return jsonify({
        'supported_drugs': SUPPORTED_DRUGS,
        'count': len(SUPPORTED_DRUGS)
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)