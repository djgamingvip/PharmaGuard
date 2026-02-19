import os

TARGET_GENES = ['CYP2D6', 'CYP2C19', 'CYP2C9', 'SLCO1B1', 'TPMT', 'DPYD']

def parse_vcf(file_path):
    """Parse VCF v4.2 and return list of relevant pharmacogenomic variants."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"VCF file not found: {file_path}")
    
    file_size = os.path.getsize(file_path)
    if file_size > 5 * 1024 * 1024:  # 5MB limit
        raise ValueError("VCF file exceeds 5MB size limit")
    
    variants = []
    vcf_version = None
    missing_annotations = False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # Parse header
                if line.startswith('##'):
                    if line.startswith('##fileformat='):
                        vcf_version = line.split('=')[1]
                    continue
                
                if line.startswith('#CHROM'):
                    continue
                
                if not line:
                    continue
                
                # Parse variant records
                parts = line.split('\t')
                if len(parts) < 8:
                    continue
                
                chrom, pos, rsid, ref, alt, qual, filt, info = parts[:8]
                
                # Parse INFO field
                info_dict = {}
                for item in info.split(';'):
                    if '=' in item:
                        key, value = item.split('=', 1)
                        info_dict[key] = value
                
                gene = info_dict.get('GENE', '')
                
                # Filter for target pharmacogenomic genes
                if gene in TARGET_GENES:
                    star_allele = info_dict.get('STAR', '')
                    
                    if not star_allele:
                        missing_annotations = True
                    
                    variant = {
                        'chrom': chrom,
                        'pos': int(pos),
                        'rsid': rsid if rsid != '.' else f"chr{chrom}:{pos}",
                        'ref': ref,
                        'alt': alt,
                        'gene': gene,
                        'star_allele': star_allele,
                        'quality': float(qual) if qual != '.' else 0,
                        'filter': filt
                    }
                    variants.append(variant)
        
        return {
            'variants': variants,
            'vcf_version': vcf_version,
            'missing_annotations': missing_annotations,
            'total_variants': len(variants)
        }
    
    except UnicodeDecodeError:
        raise ValueError("Invalid VCF file encoding. Expected UTF-8.")
    except Exception as e:
        raise ValueError(f"Error parsing VCF file: {str(e)}")