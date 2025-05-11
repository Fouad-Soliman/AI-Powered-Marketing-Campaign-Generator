from .BaseAgent import BaseAgent
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import pandas as pd 
from typing import TypedDict,Annotated
from langgraph.graph.message import add_messages
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph,END


class Database_State(TypedDict):
    # Main States
    base_prompt : str
    segment : str
    customer_data : str
    
    # SubGraph States
    retrieved_data :  Annotated[list, add_messages]
    

class DatabaseAgent(BaseAgent):
    
    def __init__(self):
        super().__init__()
        df = pd.read_csv(r"Agents/digital_marketing_campaign_dataset.csv")
        self.agent = create_pandas_dataframe_agent(self.llm,df,allow_dangerous_code=True)

        workflow = StateGraph(Database_State)
        workflow.add_node('analysis',self.analysis_node)
        workflow.add_node('user_history',self.user_history)
        workflow.add_node('user_engagment',self.user_engagment)
        workflow.add_node('user_market_specific',self.user_market_specific)
        workflow.add_node('decision_maker',self.decision_maker)
        ## Left Path edges
        workflow.set_entry_point('analysis')
        workflow.add_edge("analysis",'user_history')
        workflow.add_edge('analysis','user_engagment')
        workflow.add_edge('analysis','user_market_specific')
        
        workflow.add_edge('user_history','decision_maker')
        workflow.add_edge('user_engagment','decision_maker')
        workflow.add_edge('user_market_specific','decision_maker')
        
        
        workflow.add_edge("decision_maker",END)
        
        self.graph = workflow.compile(checkpointer=self.memory)
        
    
    def analysis_node(self,state:Database_State):
        return state
    
    def user_history(self,state: Database_State):
        
        prompt = f"""
        You are a Data analyst that helps the marketing team to get marketing campaign ideas\n
        your role is to the analyze the user data history and get insightful analysis for them\n
        You Must analyze the The User Segment {state['segment']} ONLY
        """
        result = self.agent.invoke(prompt)
        
        return {"retrieved_data":result['output']}
    
    def user_engagment(self,state:Database_State):
        
        prompt = f"""
        You are a Data analyst that helps the marketing team to get marketing campaign ideas\n
        your role is to the analyze the user engagment data and get insightful analysis for them\n
        You Must analyze the The User Segment {state['segment']} ONLY
        """
        result = self.agent.invoke(prompt)
        
        return {"retrieved_data":result['output']}
        
    
    def user_market_specific(self,state:Database_State):
        
        prompt = f"""
        You are a Data analyst that helps the marketing team to get marketing campaign ideas\n
        your role is to the analyze the market specific and get insightful analysis for them\n
        You Must analyze the The User Segment {state['segment']} ONLY
        """
        result = self.agent.invoke(prompt)
        
        
        return {"retrieved_data":result['output']}
    
    def decision_maker(self,state:Database_State):
        
        messages = "\n".join([msg.content for msg in state['retrieved_data']])
        
        # print("#"*1000,messages)
        prompt = """
            You are a Data analyst that helps the marketing team to get marketing campaign ideas\n
            Based on these analytics: {messages} \n\n
            Summarize all of that in an useful way for the marketing campaign ideas
        """
        
        prompt_template = ChatPromptTemplate.from_template(prompt)
            
        evaluator = prompt_template | self.llm
        result =  evaluator.invoke({'messages':messages})
        
        return {"customer_data":result.content}
    
    
if __name__ =='__main__':
    agent = DatabaseAgent()
    
    
    config = {'configurable':{"thread_id":1 }}
    
    initial_state = {
        "user_prompt": "hello", 
        "segment": "A",
    }
    
    print("FINAL OUTPUT",agent.graph.invoke(initial_state,config=config)['database_data'])

    
    
