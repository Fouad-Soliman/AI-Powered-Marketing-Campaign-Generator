from langchain.text_splitter import CharacterTextSplitter
import google.generativeai as genai
import json
import requests
from bs4 import BeautifulSoup
from langchain_core.messages import HumanMessage
from typing import Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph,START,END
from typing import Annotated
from typing_extensions import TypedDict
from langchain_community.tools import RequestsGetTool
from langchain_community.utilities import RequestsWrapper
from langchain.tools import Tool
from pytrends.request import TrendReq
from typing import Optional
from langchain.tools import StructuredTool
from dotenv import load_dotenv
load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")
def fetch_trending_searches(query: Optional[str] = "egypt") -> str:
    pytrends = TrendReq()
    trending = pytrends.trending_searches(pn="egypt")

    #trends to a formatted string
    trends_list = trending[0].tolist()[:10]
    return "\n".join(trends_list)

#StructuredTool for Gemini compatibility
egypt_trends_tool = StructuredTool.from_function(
    fetch_trending_searches,
    name="egypt_trends",
    description="Fetch the latest trending searches in Egypt.",
)
tools=[egypt_trends_tool]
## Langgraph Application
from langgraph.graph.message import add_messages
class State(TypedDict):
  business_idea:str
  trends_data:str

from langgraph.prebuilt import ToolNode,tools_condition

def create_trends_graph(state):
  """
  Creates the LangGraph for fetching Egypt trends.
  """
  graph_builder= StateGraph(State)
  llm_with_tools=llm.bind_tools(tools=tools)
  
  
  def chatbot(state:State):
    return {"trends_data":[llm_with_tools.invoke(state["business_idea"])]}

  graph_builder.add_node("chatbot",chatbot)
  graph_builder.add_edge(START,"chatbot")

  return graph_builder.compile()


def run_trends_graph(user_input: str):
    """
    Runs the trends graph with the given user input and returns the final messages.
    """
    graph = create_trends_graph()

    events = graph.stream(
        {"messages": [("user", user_input)]},stream_mode="values"
    )

    final_messages = []
    for event in events:
        final_messages.extend(event["messages"])

    return final_messages