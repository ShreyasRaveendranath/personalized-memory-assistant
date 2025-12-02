import json
import re
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline


def load_local_phi():
    model_id = "microsoft/Phi-3-mini-4k-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype="auto",
        device_map="auto"
    )
    text_gen = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        return_full_text=False,
        eos_token_id=tokenizer.convert_tokens_to_ids("<|end|>")
    )
    return HuggingFacePipeline(pipeline=text_gen)

LLM = load_local_phi()


EXTRACTION_PROMPT = """
You are a memory extraction module.

Extract stable user memories ONLY from the messages below.

Messages:
{messages}

Return EXACTLY this JSON:
{{
  "preferences": [],
  "emotional_patterns": [],
  "facts": []
}}

Rules:
- No invented information.
- Extract only if meaningful, repeated, or strongly implied.
- Respond ONLY with valid JSON.
"""


def extract_memories(messages):
    messages = messages[:30]
    formatted_messages = "\n".join([f"{i+1}. {msg}" for i, msg in enumerate(messages)])
    final_prompt = EXTRACTION_PROMPT.format(messages=formatted_messages)
    chat_prompt = (
        f"<|system|>You extract user memories from conversations.<|end|>\n"
        f"<|user|>{final_prompt}<|end|>\n"
        "<|assistant|>"
    )
    raw = LLM.invoke(chat_prompt)
    try:
        data = json.loads(raw)
    except:
        match = re.search(r"\{(.|\n)*\}", raw)
        if match:
            try:
                data = json.loads(match.group(0))
            except:
                data = {"preferences": [], "emotional_patterns": [], "facts": []}
        else:
            data = {"preferences": [], "emotional_patterns": [], "facts": []}
    data.setdefault("preferences", [])
    data.setdefault("emotional_patterns", [])
    data.setdefault("facts", [])

    return data


def respond_with_memories(user_input: str, memories: dict):
    memory_text = json.dumps(memories, indent=2)

    system_prompt = (
        "You are a helpful personalized assistant.\n"
        "Use the user's memories naturally.\n"
        "Do NOT use headings.\n"
        "Give your suggestions as a numbered list.\n"
        f"User Memories:\n{memory_text}"
    )
    prompt = (
        f"<|system|>{system_prompt}<|end|>\n"
        f"<|user|>{user_input}<|end|>\n"
        "<|assistant|>"
    )
    return LLM.invoke(prompt)


PERSONALITIES = {
    "calm_mentor": "Speak calmly, with wisdom and reassurance. Offer thoughtful, balanced guidance.",
    "witty_friend": "Be playful, humorous, casual, supportive, with light jokes.",
    "therapist": "Be empathetic, validating, gentle, reflective. Ask caring follow-up questions."
}

def respond_with_memories_personality(user_input: str, memories: dict, personality: str = "calm_mentor"):
    memory_text = json.dumps(memories, indent=2)
    style = PERSONALITIES.get(personality, PERSONALITIES["calm_mentor"])
    system_prompt = (
    "You are a helpful personalized assistant.\n"
    "Use the user's memories naturally.\n"
    "Do NOT use headings.\n"
    f"Personality Style: {style}\n"
    "Give your suggestions as a numbered list.\n"
    f"User Memories:\n{memory_text}"
    )

    prompt = (
        f"<|system|>{system_prompt}<|end|>\n"
        f"<|user|>{user_input}<|end|>\n"
        "<|assistant|>"
    )

    return LLM.invoke(prompt)