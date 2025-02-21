import json

class LLMSettings:
    @staticmethod
    def save(settings):
        with open('llm_settings.json', 'w') as f:
            json.dump(settings, f)
            
    @staticmethod 
    def load():
        try:
            with open('llm_settings.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "api_key": "",
                "base_url": "",
                "model": "",
                "temperature": 0.7
            }
