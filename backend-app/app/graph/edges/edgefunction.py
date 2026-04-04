from app.graph.state.graphstate import chatgraphstate
from langchain.chat_models import BaseChatModel
from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.prompts.prompt import PromptTemplate

class Routers:
    def __init__(self, llm:BaseChatModel):
        self.llm = llm
        self.expalntion_needed = False

    def query_expansion_needed(self, query):
        if len(query)<15:
            class queryExpansionevaluator(BaseModel):
                verdict : bool = Field(description="True is the question is complex. False if the question is generic eg. How are you ?, who are you ?. It should be False if you think it is refferening to some previous conversation history")
            llm = self.llm 
            exp_evaluation_prompt = PromptTemplate(template="""You are a user question expansion required evaluator. Based on your evaluation the query expansion needed will be decided.
                                        
                                        <userquestion>{question} </userquestion>
                                        """, input_variables=["question"])
            evaluation = (exp_evaluation_prompt | llm).with_structured_output(queryExpansionevaluator).invoke({"question": query})
            self.expalntion_needed = evaluation.verdict
    
    def query_analysis_routing(self,state:chatgraphstate):
        self.query_expansion_needed()
        if len(state.chat_history)> 9:
            return "summarize_history_node"
        elif self.expalntion_needed == False :
            return "answer_generation_node" 
        else :
            return "query_expansion_node"
        






        self.query_complexity_analysis(state.query)
        cascading_dict = {"Hard": "groq:openai/gpt-oss-120b", "Medium": "groq:whisper-large-v3-turbo", "Easy": "groq:qwen/qwen3-32b" }
        answer_generation_model = cascading_dict[self.answer_generation_model]
        

