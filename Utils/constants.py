RELATED_INFLUENCERS = []

def sanitation(s) :
    s = s.strip().replace(',', '.')
    # Millions sanitation
    if 'M' in s : return float(s.replace('M', '').strip()) * 1000000
    # Thousands sanitation
    if 'mil' in s : return float(s.replace('mil', '').strip()) * 1000
    if 'K' in s : return float(s.replace('K', '').strip()) * 1000
    # Bellow 10k sanitation
    if '.' in s : return float(s) * 1000
    # Bellow 1k sanitation
    return float(s)