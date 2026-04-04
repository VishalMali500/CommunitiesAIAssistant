from app.graph.state.graphstate import chatgraphstate
from langchain.chat_models import BaseChatModel
from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage
from langchain_core.embeddings import Embeddings
from langchain_core.prompts import PromptTemplate

class graphNodes:
    def __init__(self, embeddings:Embeddings):
        self.embeddings = embeddings
    def summarize_history_node(state : chatgraphstate):
        as_is_mgs = state.chat_history[len(state.chat_history)-9:]
        to_summarize_msg = state.chat_history[:len(state.chat_history)-9]
        chathistory = ""

        for m in to_summarize_msg:
            text  = m.type + ":" + f"\n{m.content}\n\n\n"
            chathistory = chathistory + text

        pt = ChatPromptTemplate(
            [("system", "You are a chat summary agent. You are responsible for generating the summary of chats between human and AI without loosing important information")],
            [("user", "{chathistory}")]
        )
        chain = pt | init_chat_model("groq:qwen/qwen3-32b") | StrOutputParser()
        summary = chain.invoke({"chathistory": chathistory})

        return {"chat_history" : [AIMessage(content=summary)] + as_is_mgs }
    
    def query_expansion_node(state : chatgraphstate):

        pt = ChatPromptTemplate(
            [("system", "You are query expansion expert. The user query is too short to understand. Expand the user provided query to its symantic & synthetic similar query. expanded query =>")],
            [("user", "{query}")]
        )
        chain = pt | init_chat_model("groq:qwen/qwen3-32b") | StrOutputParser()

        return {"query": chain.invoke({"query": state.query})}
    
    def query_complexity_analysis(self, query: str ):
        llm = init_chat_model("groq:qwen/qwen3-32b")
        
        class queryhardnessevaluator(BaseModel):
            evalution : Literal["Hard", "Medium", "Easy"] = Field(description= "evaluated toughness of user asked question from the LLM perspective")
        evaluation_prompt = PromptTemplate(template="""You are a user question toughness evaluator. Based on your evaluation the complexity of llm will be decided to answer user question.
                                           
                                           <userquestion>{question} </userquestion>
                                           """, input_variables=["question"])
        evaluation = (evaluation_prompt | llm).with_structured_output(queryhardnessevaluator).invoke({"question": query})
        return evaluation.evalution

    def answer_generation_node(self, state:chatgraphstate):
        self.embeddings

