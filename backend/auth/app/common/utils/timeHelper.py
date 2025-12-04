def parse_duration(duration_str):
    time_mapping = {
        's': 1,      # seconds
        'm': 60,     # minutes
        'h': 3600,   # hours
        'd': 86400   # days
    }
    total_seconds = 0
    parts = duration_str.split()  # Split by space
    
    for part in parts:
        if len(part) > 1:  # e.g., '15m', '1d'
            num = int(part[:-1])  # Numeric part
            unit = part[-1]        # Unit part (s, m, h, d)
            total_seconds += num * time_mapping.get(unit, 0)

    return total_seconds