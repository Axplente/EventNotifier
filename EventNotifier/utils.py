def parse_skip_days(raw, alert_days):
    clean = ""
    for ch in raw:
        if ch.isdigit() or ch == ",":
            clean += ch

    parts = clean.split(",")

    skip_list = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        try:
            n = int(p)
        except ValueError:
            continue
        skip_list.append(n)

    skip_list.sort()

    if skip_list and max(skip_list) > alert_days:
        return None

    return skip_list