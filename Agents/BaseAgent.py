from abc import ABC
from configs.config import get_settings
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI

class BaseAgent(ABC):
    
    def __init__(self):
        super().__init__()

        self.app_settings = get_settings()
        self.memory = MemorySaver()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
            api_key=self.app_settings.GOOGLE_API_KEY,
            max_retries=2,
            
            )
        
       
   

            
     