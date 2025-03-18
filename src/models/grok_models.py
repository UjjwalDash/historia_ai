from langchain_groq import ChatGroq

def load_grok_models(model_name, api_key, temperature):
    return ChatGroq(model=model_name, api_key = api_key, temperature = temperature)