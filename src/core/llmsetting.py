import json

def get_llm_settings():
    try:
        with open('llm_settings.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "api_key": "",
            "base_url": "",
            "model": "",
            "visionmode":"",
            "temperature": 0.7
        }

def save_llm_settings(settings):
    with open('llm_settings.json', 'w') as f:
        json.dump(settings, f)
