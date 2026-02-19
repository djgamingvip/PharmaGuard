from .cpic_mappings import DRUG_GENE_MAP, RISK_MATRIX, CLINICAL_RECOMMENDATIONS, ALTERNATIVE_DRUGS

def determine_phenotype(gene, star_alleles):
    """Return phenotype based on star alleles using CPIC activity scores."""
    if not star_alleles:
        return 'Unknown'
    
    # Activity score mapping (simplified CPIC approach)
    # No function = 0, Decreased = 0.5, Normal = 1, Increased = 2
    activity_scores = {
        'CYP2D6': {
            '*1': 1, '*2': 1, '*4': 0, '*5': 0, '*6': 0, '*10': 0.5, 
            '*17': 0.5, '*41': 0.5, '*1xN': 2, '*2xN': 2
        },
        'CYP2C19': {
            '*1': 1, '*2': 0, '*3': 0, '*17': 1.5
        },
        'CYP2C9': {
            '*1': 1, '*2': 0.5, '*3': 0.5
        },
        'SLCO1B1': {
            '*1': 1, '*5': 0.5, '*15': 0.5, '*17': 0.5
        },
        'TPMT': {
            '*1': 1, '*2': 0, '*3A': 0, '*3B': 0, '*3C': 0
        },
        'DPYD': {
            '*1': 1, '*2A': 0, 'c.1679T>G': 0.5, 'c.2846A>T': 0.5
        }
    }
    
    gene_scores = activity_scores.get(gene, {})
    total_score = 0
    count = 0
    
    for allele in star_alleles:
        score = gene_scores.get(allele, 1)  # Default to normal if unknown
        total_score += score
        count += 1
    
    if count == 0:
        return 'Unknown'
    
    avg_score = total_score / count
    
    # Map activity score to phenotype
    if avg_score == 0:
        return 'PM'  # Poor Metabolizer
    elif avg_score < 1:
        return 'IM'  # Intermediate Metabolizer
    elif avg_score == 1:
        return 'NM'  # Normal Metabolizer
    elif avg_score < 2:
        return 'RM'  # Rapid Metabolizer
    else:
        return 'UM'  # Ultrarapid Metabolizer

def assess_risk(drug, phenotype):
    """Return risk label, severity, and clinical recommendation."""
    if drug not in RISK_MATRIX:
        return 'Unknown', 'unknown', 'No guideline available for this drug.', []
    
    mapping = RISK_MATRIX[drug]
    risk_label = mapping.get(phenotype, 'Unknown')
    
    # Map risk to severity
    severity_map = {
        'Safe': 'none',
        'Adjust Dosage': 'moderate',
        'Toxic': 'high',
        'Ineffective': 'moderate',
        'Unknown': 'low'
    }
    severity = severity_map.get(risk_label, 'low')
    
    # Get clinical recommendation
    recommendation = CLINICAL_RECOMMENDATIONS.get(drug, {}).get(phenotype, 'Consult CPIC guidelines.')
    
    # Get alternative drugs
    alternatives = ALTERNATIVE_DRUGS.get(drug, [])
    
    return risk_label, severity, recommendation, alternatives