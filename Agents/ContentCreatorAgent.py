import os
import logging
from typing import Dict, Any, List, TypedDict

from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# Import Chat models and prompt templates from LangChain
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# Import the LangGraph classes.
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

# Set up basic logging.
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
load_dotenv()
# 1. Define the State

class ContentCreationState(TypedDict):
    """
    Represents the state of the content creation process.
    """
    trends_data: str
    customer_data: str
    ideation_output: List[str]  # Changed to List[str]
    #idea: str #Removed
    detailed_content: List[str] #Changed To List
    messages: List[BaseMessage]

# 2. Define Nodes as Functions with LangChain Runnables

# Content Ideation Node
class ContentIdeas(BaseModel):
    ideas: List[str] = Field(description="A list of content ideas based on the trends and customer insights.")

content_parser = PydanticOutputParser(pydantic_object=ContentIdeas)

def content_ideation(state: ContentCreationState):
    """Generates campaign ideas based on trends and customer data."""
    logging.info(f"[ContentIdeationNode] Received state: {state}")

    system_message = (
        "You are a creative marketing strategist specializing in generating innovative "
        "and data-driven campaign ideas for modern, sustainable brands. "
        "Your responses should be imaginative, insightful, and directly address the input data."
    )
    human_message = (
        "Based on the following trends: {trends_data}\n"
        "and customer insights: {customer_data},\n"
        "please generate 3-5 creative campaign ideas.\n"
        "{format_instructions}"
    )

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        MessagesPlaceholder(variable_name="messages"),
        ("user", human_message)
    ])

    chain = chat_prompt | GoogleGenerativeAI(model="gemini-1.5-flash",temperature=1.0) | content_parser

    result = chain.invoke({
        "trends_data": state["trends_data"],
        "customer_data": state["customer_data"],
        "format_instructions": content_parser.get_format_instructions(),
        "messages": state["messages"]
    })

    logging.info(f"[ContentIdeationNode] Generated ideation output:\n{result}")
    return {"ideation_output": result.ideas}

# Select Idea Node REMOVED
#Content Drafting Node
def content_drafting(state: ContentCreationState):
    """Expands all the ideas into detailed campaign narratives."""
    ideas = state["ideation_output"]  # Get ideas directly
    logging.info(f"[ContentDraftingNode] Received ideas: {ideas}")

    system_message = (
        "You are a skilled copywriter and storyteller specializing in transforming creative ideas "
        "into detailed, engaging marketing campaigns. Your writing should be rich in detail, on-brand, "
        "and tailored to a modern, eco-conscious audience."
    )
    output_template = (
        "Please structure your response using the following format:\n"
        "Title: <Campaign Title>\n"
        "Overview: <Brief campaign summary>\n"
        "Narrative: <Detailed campaign description>\n"
        "Call-to-Action: <Compelling call-to-action>\n"
    )

    drafted_contents = []
    for idea in ideas:
        human_message = (
            "Expand the following idea into a detailed campaign narrative.\n"
            "Idea: {idea}\n\n" + output_template
        )
        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="messages"),
            ("user", human_message)
        ])

        chain = chat_prompt | GoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

        detailed_content = chain.invoke({
            "idea": idea,
            "messages": state["messages"]
        })
        drafted_contents.append(detailed_content)
        logging.info(f"[ContentDraftingNode] Drafted content for idea '{idea}':\n{detailed_content}")
    return {"detailed_content": drafted_contents}

def create_content_graph(state):
    """
    Creates the LangGraph for content ideation and drafting.
    """
    builder = StateGraph(ContentCreationState)

    builder.add_node("content_ideation", content_ideation)
    builder.add_node("content_drafting", content_drafting)
    builder.set_entry_point("content_ideation")
    builder.add_edge("content_ideation", "content_drafting")
    builder.add_edge("content_drafting", END)

    return builder.compile()


def run_content_graph(trends_data: str, customer_data: str):
    """
    Runs the content graph with the given inputs and returns the final content.
    """
    graph = create_content_graph()

    external_inputs = {
        "trends_data": trends_data,
        "customer_data": customer_data,
        "ideation_output": [],
        "detailed_content": [],
        "messages": []
    }

    final_state = graph.invoke(external_inputs)
    final_content = final_state.get("detailed_content", "No content generated.")
    return final_content