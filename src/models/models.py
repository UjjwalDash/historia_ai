import yaml
import os
from langchain_openai import ChatOpenAI
from src.models.grok_models import load_grok_models
from dotenv import load_dotenv

load_dotenv("src/config/tools/.email_env")

with open('src/config/models/models_config.yaml', 'r') as file:
    config = yaml.safe_load(file)

service_provider_query = config['response_generator']['service_provider']
model_name_query = config['response_generator']['model_name']
api_key_query = os.getenv("API_KEY")
base_url_query = config['response_generator']['base_url']
temperature_query = config['response_generator']['temperature']

if service_provider_query == 'grok':
    query_llm = load_grok_models(model_name_query, api_key_query, temperature_query)


print("response_generator :", service_provider_query)



