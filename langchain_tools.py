
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from pypdf import PdfReader
from langchain.agents.agent_types import AgentType
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import pandas as pd
from langchain.document_loaders.csv_loader import CSVLoader
load_dotenv()




class AI_assist:
    
    #add init function
    def __init__(self):
        pass


    
    #turn text into vectorstore
    def text_to_vectorstore(self, text: str) -> Chroma:

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        docs_chunks = text_splitter.split_text(text)
        text_vectorstore = Chroma.from_texts(docs_chunks, OpenAIEmbeddings())
        return text_vectorstore

    
    #load csv file 
    def csv_loader(self, file_path: str) -> str:
        loader = CSVLoader(file_path= file_path)
        csv_data = loader.load()
        
        return str(csv_data)
    
    #load pdf file
    def pdf_loader(self, pdf_url:str) -> str:

        text = ''
        pdf_reader = PdfReader(pdf_url)
        for page in pdf_reader.pages:
            
            text += page.extract_text()
        
        return str(text)

    # embedding csv data into vectorstore
    def text_to_vectorstore(self, data:str) -> Chroma:
        """
        This function takes a list of csv data, splits it into chunks, and then converts these chunks into a Chroma vectorstore.

        Parameters:
        csv_data (list): The csv data to be converted.

        Returns:
        Chroma: The Chroma vectorstore representation of the csv data.
        """
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs_chunks = text_splitter.split_text(data)
        docs_vectorstore = Chroma.from_texts(docs_chunks, OpenAIEmbeddings())
        return docs_vectorstore
    

    #turn vectorstore into retriever
    def vectorstore_to_retriever(self, vectorstore: Chroma, short_document: bool = False):
        """
        Converts a vectorstore to a retriever.

        Args:
            vectorstore (Chroma): The vectorstore to convert.
            short_document (bool, optional): Whether to use short document retrieval. Defaults to False.

        Returns:
            Retriever: The converted retriever.
        """
        try:
            if short_document:
                retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
            else:
                retriever = vectorstore.as_retriever()

        except Exception as e:
            print(f"Error occurred while converting vectorstore to retriever: {e}")
            retriever = None

        return retriever
    
    #add system pre injected templates
    def system_pre_injected_templates(self):
        pass

    def get_context_retriever_chain(vector_store):
        llm = ChatOpenAI()

        retriever = vector_store.as_retriever()
        prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name= "chat_history"),
            ("user","{input}"),
            ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
        ])

        retriver_chain = create_history_aware_retriever(llm,retriever, prompt)
        return retriver_chain    
    #create a document chain
    def get_conversational_rag_chain(retriever_chain):

        llm = ChatOpenAI()

        prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's questions based on the below context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ])

        stuff_documents_chain = create_stuff_documents_chain(llm,prompt)

        return create_retrieval_chain(retriever_chain,stuff_documents_chain)


        


