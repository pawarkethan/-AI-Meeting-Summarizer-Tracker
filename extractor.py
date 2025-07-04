def extract_action_items(summary):
    lines = summary.split('.')
    actions = [line.strip() for line in lines if "will" in line or "should" in line or "need to" in line]
    return actions
