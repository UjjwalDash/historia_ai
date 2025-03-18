import yaml

with open('src/config/memory/memory_config.yaml', 'r') as file:
    config = yaml.safe_load(file)

if config['cache_memory'] == 'true':

    from src.memory import cache_memory

elif config['long_term_memory'] == 'true':
    
    pass

elif config['sort_term_memory'] == 'true':

    pass
