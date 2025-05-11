from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,END
from typing import TypedDict, Annotated,Literal
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

class Review(BaseModel):
    """Check Whether it has the order id or not and extract it"""
    review: Literal["accepted", "review"] = Field(
        description="Return 'accepted' if the content is related to user prompt, otherwise return 'review'."
    )

def review_content(state):
    llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
            api_key="AIzaSyAW3Cpa3h0HZ5yO2JE1K0NNdtkGurwYhpU",
            max_retries=2,
            
            )
    structured_llm = llm.with_structured_output(Review)
    content = state['content']
    user_prompt = state['user_prompt']
    template = """
        You are a Content Reviewer responsible for evaluating content created by a content creator.\n
        Your role is to assess whether the content aligns with the given user prompt and meets quality standards.\n
        You must determine if the content is 'Accepted' or 'Needs Review'.\n
        Only return one of these two outcomes based on your evaluation.\n
        User Message: {usermessage}
        Content:{content}
        """  
    prompt_template = ChatPromptTemplate.from_template(template=template)
    evaluator = prompt_template | structured_llm
    result =  evaluator.invoke({'usermessage':user_prompt,'content':content})
    return result.review