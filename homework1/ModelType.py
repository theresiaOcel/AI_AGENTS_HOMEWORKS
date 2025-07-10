from enum import Enum

class ModelType(Enum):
    GPT_4o_mini = "gpt-4o-mini"
    GPT_41_mini = "gpt-4.1-mini"
    HF_DeepSeek = "accounts/fireworks/models/deepseek-r1-0528"
    LLAMA_31_8B_INSTRUCT = "accounts/fireworks/models/llama-v3p1-8b-instruct"
    MISTRAL_SMALL_31_24B_INSTRUCT = "mistralai/Mistral-Small-3.1-24B-Instruct-2503"
    LLAMA_32_VISION_INSTRUCT = "meta-llama/Llama-3.2-11B-Vision-Instruct"
