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

    # Prepend system prompt
    clean_messages.insert(0, {
        "role": "system",
        "content": SYSTEM_PROMPT
    })

    response = client.chat.completions.create(
        model=deployment,
        messages=clean_messages,
        max_completion_tokens=40000
    )

    return response.choices[0].message.content

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
        max_completion_tokens=40000,
        stop=None,
        stream=False
    )

    raw = response.choices[0].message.content
    try:
        faqs = json.loads(raw)
    except json.JSONDecodeError:
        faqs = [] 
    return faqs
