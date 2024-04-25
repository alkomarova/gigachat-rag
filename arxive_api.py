import os
from typing import List, Tuple

from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.callbacks.manager import CallbackManagerForRetrieverRun
from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.convert_to_openai import format_tool_to_openai_function
from langchain_community.utilities.arxiv import ArxivAPIWrapper
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.retrievers import BaseRetriever
from langchain.chains import ConversationalRetrievalChain

from langchain.chat_models.gigachat import GigaChat

TOKEN = os.getenv('GCTOKEN')



class ArxivRetriever(BaseRetriever, ArxivAPIWrapper):
    """`Arxiv` retriever.

    It wraps load() to get_relevant_documents().
    It uses all ArxivAPIWrapper arguments without any change.
    """

    get_full_documents: bool = False

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        try:
            if self.is_arxiv_identifier(query):
                results = self.arxiv_search(
                    id_list=query.split(),
                    max_results=self.top_k_results,
                ).results()
            else:
                results = self.arxiv_search(  # type: ignore
                    query[: self.ARXIV_MAX_QUERY_LENGTH], max_results=self.top_k_results
                ).results()
        except self.arxiv_exceptions as ex:
            return [Document(page_content=f"Arxiv exception: {ex}")]
        docs = [
            Document(
                page_content=result.summary,
                metadata={
                    "Published": result.updated.date(),
                    "Title": result.title,
                    "Authors": ", ".join(a.name for a in result.authors),
                },
            )
            for result in results
        ]
        return docs


description = (
    "A wrapper around Arxiv.org "
    "Useful for when you need to answer questions about Physics, Mathematics, "
    "Computer Science, Quantitative Biology, Quantitative Finance, Statistics, "
    "Electrical Engineering, and Economics "
    "from scientific articles on arxiv.org. "
    "Input should be a search query."
)

# Create the tool
retriever = ArxivRetriever(load_max_docs=20)
llm = GigaChat(credentials=TOKEN, 
               model="GigaChat-Pro",
               verify_ssl_certs=False,
                    scope='GIGACHAT_API_CORP')
                    
assistant_system_message = """You are a helpful research assistant. \
Lookup relevant information as needed."""

qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever)
questions = [
    "What are Heat-bath random walks with Markov base?",
    "What is the ImageBind model?",
    "How does Compositional Reasoning with Large Language Models works?",
    "Сколько слоев в ImageNet?",
    "Что такое LSTM?"
]
chat_history = []

for question in questions:
    result = qa({"question": question, "chat_history": chat_history})
    chat_history.append((question, result["answer"]))
    print(f"-> **Question**: {question} \n")
    print(f"**Answer**: {result['answer']} \n")