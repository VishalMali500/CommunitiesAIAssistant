from typing_extensions import TypedDict, List, NotRequired
from langchain_core.documents import Document
from typing import  Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class chatgraphstate(TypedDict):
    user : str
    attempts : int = 0
    query : str
    context : List[Document]
    messages : Annotated[List[BaseMessage], add_messages]
    feedback : NotRequired[str]
    response : NotRequired[str]
    chat_history : List[BaseMessage]

