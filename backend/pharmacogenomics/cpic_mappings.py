# Drug to gene mapping (CPIC-aligned)
DRUG_GENE_MAP = {
    'CODEINE': 'CYP2D6',
    'WARFARIN': 'CYP2C9',  # Simplified to primary gene
    'CLOPIDOGREL': 'CYP2C19',
    'SIMVASTATIN': 'SLCO1B1',
    'AZATHIOPRINE': 'TPMT',
    'FLUOROURACIL': 'DPYD'
}

# Phenotype to risk mapping (CPIC-aligned)
RISK_MATRIX = {
    'CODEINE': {
        'PM': 'Ineffective',
        'IM': 'Adjust Dosage',
        'NM': 'Safe',
        'RM': 'Toxic',
        'UM': 'Toxic',
        'Unknown': 'Unknown'
    },
    'CLOPIDOGREL': {
        'PM': 'Ineffective',
        'IM': 'Adjust Dosage',
        'NM': 'Safe',
        'RM': 'Safe',
        'UM': 'Safe',
        'Unknown': 'Unknown'
    },
    'WARFARIN': {
        'PM': 'Adjust Dosage',
        'IM': 'Adjust Dosage',
        'NM': 'Safe',
        'RM': 'Safe',
        'UM': 'Safe',
        'Unknown': 'Unknown'
    },
    'SIMVASTATIN': {
        'PM': 'Toxic',
        'IM': 'Adjust Dosage',
        'NM': 'Safe',
        'RM': 'Safe',
        'UM': 'Safe',
        'Unknown': 'Unknown'
    },
    'AZATHIOPRINE': {
        'PM': 'Toxic',
        'IM': 'Adjust Dosage',
        'NM': 'Safe',
        'RM': 'Safe',
        'UM': 'Safe',
        'Unknown': 'Unknown'
    },
    'FLUOROURACIL': {
        'PM': 'Toxic',
        'IM': 'Adjust Dosage',
        'NM': 'Safe',
        'RM': 'Safe',
        'UM': 'Safe',
        'Unknown': 'Unknown'
    }
}

# Clinical recommendations per drug-phenotype
CLINICAL_RECOMMENDATIONS = {
    'CODEINE': {
        'PM': 'Avoid codeine. Use alternative analgesic (e.g., morphine, non-opioid).',
        'IM': 'Use label-recommended dosage. Monitor for reduced efficacy.',
        'NM': 'Use label-recommended dosage.',
        'RM': 'Avoid codeine due to increased risk of toxicity. Use alternative.',
        'UM': 'Avoid codeine due to high risk of toxicity. Use alternative.',
        'Unknown': 'Use with caution. Consider genetic testing.'
    },
    'CLOPIDOGREL': {
        'PM': 'Alternative antiplatelet therapy recommended (e.g., prasugrel, ticagrelor).',
        'IM': 'Consider alternative antiplatelet or increased dose per guidelines.',
        'NM': 'Use label-recommended dosage.',
        'RM': 'Use label-recommended dosage.',
        'UM': 'Use label-recommended dosage.',
        'Unknown': 'Use with caution. Consider genetic testing.'
    },
    'WARFARIN': {
        'PM': 'Reduce initial dose by 25-50%. Monitor INR closely.',
        'IM': 'Reduce initial dose by 10-25%. Monitor INR closely.',
        'NM': 'Use standard dosing protocol. Monitor INR.',
        'RM': 'Use standard dosing protocol. Monitor INR.',
        'UM': 'Use standard dosing protocol. Monitor INR.',
        'Unknown': 'Use standard dosing. Monitor INR closely.'
    },
    'SIMVASTATIN': {
        'PM': 'Avoid simvastatin or use lowest dose. Consider alternative statin.',
        'IM': 'Reduce dose or consider alternative statin.',
        'NM': 'Use label-recommended dosage.',
        'RM': 'Use label-recommended dosage.',
        'UM': 'Use label-recommended dosage.',
        'Unknown': 'Use with caution. Monitor for myopathy.'
    },
    'AZATHIOPRINE': {
        'PM': 'Reduce dose to 10% of standard. Monitor closely for toxicity.',
        'IM': 'Reduce dose to 30-70% of standard. Monitor blood counts.',
        'NM': 'Use label-recommended dosage.',
        'RM': 'Use label-recommended dosage.',
        'UM': 'Use label-recommended dosage.',
        'Unknown': 'Use with caution. Consider genetic testing.'
    },
    'FLUOROURACIL': {
        'PM': 'Avoid fluorouracil. High risk of severe toxicity.',
        'IM': 'Reduce dose by 50% or consider alternative. Monitor closely.',
        'NM': 'Use label-recommended dosage.',
        'RM': 'Use label-recommended dosage.',
        'UM': 'Use label-recommended dosage.',
        'Unknown': 'Use with caution. Consider genetic testing.'
    }
}

# Alternative drugs
ALTERNATIVE_DRUGS = {
    'CODEINE': ['Morphine', 'Hydromorphone', 'Oxycodone', 'Tramadol'],
    'CLOPIDOGREL': ['Prasugrel', 'Ticagrelor'],
    'WARFARIN': ['Apixaban', 'Rivaroxaban', 'Dabigatran'],
    'SIMVASTATIN': ['Pravastatin', 'Rosuvastatin', 'Atorvastatin'],
    'AZATHIOPRINE': ['Mycophenolate', 'Methotrexate'],
    'FLUOROURACIL': ['Capecitabine (with caution)', 'Raltitrexed']
}