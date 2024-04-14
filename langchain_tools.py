
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


'''
ai assist class is meant to help with job search, and can read resume and job descriptions to help with job search
'''
class AI_assist:
    
    #add init function
    def __init__(self):
        pass

    #read pdf function that can read and extract text from pdf
    def read_pdf(self, file_path) -> str:
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text()

        return text
    
    #turn text into vectorstore
    def text_to_vectorstore(self, text: str) -> Chroma:

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        docs_chunks = text_splitter.split_text(text)
        text_vectorstore = Chroma.from_texts(docs_chunks, OpenAIEmbeddings())
        return text_vectorstore
