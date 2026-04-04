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
from langchain_core.vectorstores import VectorStore
from app.core.get_user_role import getrole

class graphNodes:
    def __init__(self, embeddings:Embeddings, vdb:VectorStore ):
        self.embeddings = embeddings
        self.vdb = vdb
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
        llm = init_chat_model("groq:qwen/qwen3-32b")
        access_list = getrole(state.user)
        docs = self.vdb.similarity_search( state.query, k=5,filter={"source": {"$in": access_list}})
        class contextrelevancycheker(BaseModel):
            evaluation : bool= Field(description= "boolean verdict on context relevancy for the user asked question")
        relevancy_prompt = PromptTemplate(template="""You are a context relevancy cheker for a user asked question. Give your veridict in the boolean form for the context.
                                           <question>{question}</question>
                                           <context>{context} </context>
                                           """, input_variables=["question", "context"])
        evaluation_llm = (relevancy_prompt | llm).with_structured_output(contextrelevancycheker)
        filtered_docs = []
        for doc in docs:
            output = evaluation_llm.invoke({"question": state.query, "context": doc.page_content })
            if output.evaluation :
                filtered_docs.extend(doc)
        main_llm = init_chat_model(self.query_complexity_analysis(state.query))
        answer_generation_prompt = ChatPromptTemplate.from_messages(
            ["system", "You are an expert in question answering task. Provided an user question answer that question using provided context. Strictly dont use your own knowledge. If the answer is not present in the provided context then say you dont know."],
            ["user", """<question>{question}</question>
                        <context>{context} </context>"""],input_variables=["question", "context"])
        main_llm_chain = answer_generation_prompt | main_llm | StrOutputParser()
        chats = "------------Chat History-----------\n\n"
        for m in state.chat_history[:len(state.chat_history)-1]:
            text  = m.type + ":" + f"\n{m.content}\n\n\n"
            chats = chats + text
        chats = chats + "\n-----------Chat History End---------------\n\n-----------Current User Question-----------\n human:" + state.query
        return {"answer" : main_llm_chain.invoke({"question": chats, "context" : "\n\n".join([d.page_content for d in filtered_docs])})}
        





        

        
        

