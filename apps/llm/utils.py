import re

def format_response_as_steps(text):
    steps = []

    pattern = r"(\d+\. .+?)(?=\n\d+\. |\Z)"
    matches = re.findall(pattern, text, flags=re.DOTALL)

    for match in matches:
        lines = match.strip().split("\n")
        title = lines[0]
        content = [line.strip(" •–-") for line in lines[1:] if line.strip()]
        steps.append({"title": title, "content": content})

    if not steps:
        steps.append({"title": "Info", "content": [text]})

    return steps