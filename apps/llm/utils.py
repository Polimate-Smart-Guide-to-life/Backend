import re

def format_response_as_steps(text):
    if text is None:
        text = ""
    text = str(text).strip()

    steps = []

    # Primary pattern: blocks starting with "1. " on separate lines
    primary_pattern = r"(\d+\.\s.+?)(?=(?:\n\d+\.\s)|\Z)"
    matches = re.findall(primary_pattern, text, flags=re.DOTALL)

    # If no matches, attempt to normalize inline enumerations like "1)" or "1:"
    if not matches:
        normalized = re.sub(r"(\d+)[\):]", r"\1.", text)
        # Insert newlines before each number occurrence except at start
        normalized = re.sub(r"(?<!^)\s(?=\d+\.\s)", "\n", normalized)
        matches = re.findall(primary_pattern, normalized, flags=re.DOTALL)
        text = normalized

    for match in matches:
        block = match.strip()
        # Try to split into a heading and body. Supports bold headings ending with ':'
        m = re.match(r"^\d+\.\s*(?:\*\*(?P<h1>.+?)\*\*:?|(?P<h2>[^:\n]+):?)\s*(?P<body>.*)$", block, flags=re.DOTALL)
        if m:
            heading = (m.group("h1") or m.group("h2") or "").strip()
            body = (m.group("body") or "").strip()
        else:
            # Fallback: split first line as title, rest as body
            lines = block.split("\n")
            heading = lines[0].strip()
            body = "\n".join(lines[1:]).strip()

        # Derive content bullets from body
        content = []
        if body:
            # Split on newlines or bullet symbols first
            parts = re.split(r"\n|•|\u2022|^-\s|\s-\s", body)
            parts = [p for p in parts if p and p.strip()]
            if len(parts) <= 1:
                # If still a single paragraph, split by sentences
                parts = re.split(r"(?<=[.!?])\s+", body)
                parts = [p for p in parts if p and p.strip()]
            content = [p.strip(" •–-") for p in parts if p.strip()]

        # If content ended up empty and heading is very long, move heading into content
        if not content and len(heading) > 80:
            content = [heading]
            heading = "Info"

        steps.append({"title": heading, "content": content})

    # Fallback: try to split by common bullet separators if no structured steps
    if not steps:
        bullets = re.split(r"\n|•|\u2022|^-\s|\s-\s", text)
        bullets = [b.strip() for b in bullets if b and b.strip()]
        if len(bullets) > 1:
            steps = [{"title": "Info", "content": bullets}]
        else:
            steps = [{"title": "Info", "content": [text]}]

    return steps