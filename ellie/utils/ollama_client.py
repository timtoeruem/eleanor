import os
from utils.config import ConfigManager  # Import Config Manager from [[citation:2]]
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

class OllamaClient:
    def __init__(self):
        self.config = ConfigManager()  # Initialize config manager
        self.model_name = "llama3.1:latest"  # Default model name

    def authenticate_ollama(self):
        
        ollama_config = {
            "url": "http://localhost:11434",
            "api_key": None,  # If API key isn't used with Ollama
            "headers": {}      # Additional headers can be specified here if needed
        }
        

        template = """Question: {question}

Answer: Let's think step by step."""
        prompt = ChatPromptTemplate.from_template(template)

        model = OllamaLLM(model="llama3.1", base_url=ollama_config["url"])

        chain = prompt | model

        return chain.invoke({"question": "What is LangChain?"})
            
        
if __name__ == "__main__":
    x=OllamaClient()
    test=x.authenticate_ollama()
    print(test)
