from django.conf import settings
# from google import genai
from openai import AzureOpenAI
import json

SYSTEM_PROMPT = (
    "You are the Support Assistant for Politecnico di Milano. "
    "You provide guidance regarding campus locations, buildings, facilities, nearby services, study plans, exams, courses, academic resources, enrollment, visa, residence permit, and other administrative steps."
    "If the question is not related to Polimi, say: "
    "\"I can only help with topics related to Politecnico di Milano.\""
)

REASONING_FORMAT_PROMPT = (
    "Always return your response as a strict JSON object with keys 'answer' and 'reasoning'. "
    "'answer': the final concise reply for the user. 'reasoning': a brief (1-3 sentences) explanation of why you gave that answer (do not include sensitive internal policies). "
    "Example: {\"answer\": \"<final answer>\", \"reasoning\": \"<brief rationale>\"}."
)

# THIS SHOULD BE USED ONLY WHEN USING GEMINI API
#==================================================================================================================================
# client = genai.Client(api_key=settings.GEMINI_API_KEY)

# def generate_conversation_response(messages):
#     """
#     messages = [
#         {"role": "user", "content": "..."},
#         {"role": "assistant", "content": "..."}
#     ]
#     """
#     # Prepend system prompt
#     content = SYSTEM_PROMPT + "\n\n" + "\n".join(
#         m["content"] for m in messages if m["role"] in ["user", "assistant"]
#     )

#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=content
#     )

#     return response.text

# def get_trending_faqs():
#     prompt = (
#         SYSTEM_PROMPT + "\n\n"
#         "Generate 5 FAQS that the students from Politecnico di Milano or students in Italy ask."
#         "Return the output strictly as a JSON array of strings, without any extra text or explanation."
#     )

#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )

#     return response.text
#==================================================================================================================================

endpoint = settings.AZURE_ENDPOINT_URL
deployment = settings.AZURE_DEPLOYMENT_NAME
subscription_key = settings.AZURE_OPENAI_API_KEY

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
)

def get_max_completion_tokens():
    val = getattr(settings, "LLM_MAX_COMPLETION_TOKENS", 2048)
    try:
        return max(1, min(int(val), 16384))
    except (TypeError, ValueError):
        return 2048

def generate_conversation_response(messages):
    """
    messages = [
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."}
    ]
    """

    # Ensure content is always a string
    clean_messages = []
    for m in messages:
        clean_messages.append({
            "role": m["role"],
            "content": str(m["content"])
        })

    # Prepend system prompt and formatting instruction
    clean_messages.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
    clean_messages.insert(1, {"role": "system", "content": REASONING_FORMAT_PROMPT})

    response = client.chat.completions.create(
        model=deployment,
        messages=clean_messages,
        max_completion_tokens=get_max_completion_tokens()
    )

    raw_content = str(response.choices[0].message.content or "")

    # Attempt to parse JSON for answer and reasoning
    answer = raw_content
    reasoning = None
    try:
        parsed = json.loads(raw_content)
        if isinstance(parsed, dict) and "answer" in parsed and "reasoning" in parsed:
            answer = parsed.get("answer")
            reasoning = parsed.get("reasoning")
    except json.JSONDecodeError:
        pass

    # Determine latest user question for logging
    latest_user_message = None
    for m in reversed(clean_messages):
        if m.get("role") == "user":
            latest_user_message = m.get("content")
            break

    # Print reasoning to terminal logs
    if latest_user_message:
        print("[LLM QUESTION]", latest_user_message, flush=True)
    if reasoning:
        print("[LLM REASONING]", reasoning, flush=True)
    else:
        print("[LLM REASONING] <unavailable – JSON parse failed>", flush=True)

    return answer

def get_trending_faqs():
    prompt = (
        SYSTEM_PROMPT + "\n\n"
        "Generate 5 FAQS that the students from Politecnico di Milano or students in Italy ask."
        "Return the output strictly as a JSON array of strings, without any extra text or explanation."
    )

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_completion_tokens=get_max_completion_tokens(),
        stop=None,
        stream=False
    )

    raw = response.choices[0].message.content
    try:
        faqs = json.loads(raw)
    except json.JSONDecodeError:
        faqs = [] 
    return faqs
