from .BaseAgent import BaseAgent
from typing import TypedDict,Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,END,START
from langchain_core.messages import BaseMessage
from typing import  Any, List, TypedDict
from .DatabaseAgent import DatabaseAgent
from .ContentCreatorAgent import create_content_graph
from .trendsAgent import create_trends_graph
from .ReviewerAgent import review_content

class Main_State(TypedDict):
    # Main States
    business_idea : str
    segment : str
    retrieved_data :  Annotated[list, add_messages]
    trends_data: str
    customer_data: str
    ideation_output: List[str]  # Changed to List[str]
    #idea: str #Removed
    detailed_content: List[str] #Changed To List
    messages: List[BaseMessage]
    theme: str
    primary_obj:str
    budget_range:str
    audience : str
    product_name:str
    primary_channel:str
    comm_channel:str
    restriections:str
    messages: List[BaseMessage]

class MainAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        
        data_agent = DatabaseAgent()
        workflow = StateGraph(Main_State)
        workflow.add_node("data_agent",data_agent.graph)
        workflow.add_node("content_agent",create_content_graph)
        workflow.add_node("trend_agent",create_trends_graph)
        workflow.add_node("reviewer",review_content)
        workflow.add_node("dummy",self.dummy)
        
        workflow.add_edge(START,"data_agent")
        workflow.add_edge(START,"trend_agent")
        
        workflow.add_edge('data_agent',"content_agent")
        workflow.add_edge('trend_agent',"content_agent")
        workflow.add_edge('reviewer',"dummy")
        
        workflow.add_conditional_edges("dummy",
                                       review_content,
                                       {
                                           "accepted":END,
                                            "review":'content_agent'
                                       })
        
        self.graph = workflow.compile(checkpointer=self.memory)
    
    
    def dummy(self,state):
        return state
        
    
    

    