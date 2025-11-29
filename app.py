import streamlit as st 
import os
import shutil
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)


# Load environment variables
load_dotenv()

# --- App Configuration ---
st.set_page_config(page_title="Company Knowledge Base", page_icon="📚")
st.title("📚 Company Knowledge Base Agent")
st.markdown("""
    Ask me anything about our company! 
    I can answer questions about our products, policies, and history.
    
    **Example questions:**
    * What is InnovateHub?
    * How many vacation days do we get?
    * Tell me about the company.
""")



# --- Constants ---
DOCUMENTS_DIR = "./documents"
VECTORSTORE_DIR = "./chroma_db"

if st.session_state.get("delete_vs"):
    if os.path.exists(VECTORSTORE_DIR):
        shutil.rmtree(VECTORSTORE_DIR, ignore_errors=True)
    st.session_state.delete_vs = False

@st.cache_resource
def get_retrieval_chain():
    """
    Initializes and returns a retrieval chain.
    This function is cached to avoid expensive re-initialization on every app rerun.
    """
    google_api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
    if not google_api_key:
    st.error("Google API Key not found. Please set GOOGLE_API_KEY in Streamlit secrets or environment.")
    st.stop()

    # 1. Local embeddings (NO Google embeddings → no quota issues)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # 2. Gemini chat model (only for generation, not embeddings)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=google_api_key,
        temperature=0.3,
    )

    # 3. Load and Process Documents
    if not os.path.exists(VECTORSTORE_DIR):
        st.info(f"Creating new vector store from documents in '{DOCUMENTS_DIR}'...")
        if not os.path.exists(DOCUMENTS_DIR):
            os.makedirs(DOCUMENTS_DIR)
            st.warning(f"'{DOCUMENTS_DIR}' was empty. Please add your knowledge base files there.")
            st.stop()

        # Only load markdown files for now, using a simple text loader (no unstructured/libmagic)
        loader = DirectoryLoader(
        DOCUMENTS_DIR,
        glob="**/*.md",
        loader_cls=TextLoader,      # <- this avoids unstructured/libmagic
        show_progress=True,
        )
        documents = loader.load()


        if not documents:
            st.warning(f"No markdown documents found in '{DOCUMENTS_DIR}'. Please add your knowledge base files.")
            st.stop()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        split_docs = text_splitter.split_documents(documents)

        # Build Chroma vector store with local embeddings
        vectorstore = Chroma.from_documents(
            documents=split_docs,
            embedding=embeddings,  # positional name is fine
            persist_directory=VECTORSTORE_DIR,
        )
        st.success("Vector store created and saved.")
    else:
        st.info("Loading existing vector store...")
        vectorstore = Chroma(
            persist_directory=VECTORSTORE_DIR,
            embedding_function=embeddings,
        )
        st.success("Vector store loaded.")

    retriever = vectorstore.as_retriever()

    # Prompt for RAG
    prompt_template = """
    You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. 
    Be concise and helpful.

    Context:
    {context}

    Question:
    {input}

    Answer:
    """
    prompt = ChatPromptTemplate.from_template(prompt_template)

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, question_answer_chain)

    return retrieval_chain


# --- UI Interaction ---

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if user_question := st.chat_input("What is your question?"):
    st.session_state.chat_history.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    try:
        retrieval_chain = get_retrieval_chain()
        with st.spinner("Thinking..."):
            response = retrieval_chain.invoke({"input": user_question})
            answer = response.get("answer", "Sorry, I couldn't find an answer.")

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.chat_history.append({"role": "assistant", "content": answer})

    except Exception as e:
        st.error(f"An error occurred: {e}")

# --- Sidebar ---
with st.sidebar:
    st.header("About")
    st.markdown("""
        This is a Knowledge Base Agent built with Streamlit, LangChain, and Google Gemini. 
        It answers questions based on the documents found in the `documents` folder.
    """)
    st.header("Setup Status")
    st.markdown(f"**Documents Folder:** `{DOCUMENTS_DIR}`")
    st.markdown(f"**Vector Store:** `{VECTORSTORE_DIR}`")
    if os.path.exists(VECTORSTORE_DIR):
        st.success("Vector store is ready.")
    else:
        st.info("Vector store will be created on the first run.")

    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

    if st.button("Delete Vector Store"):
        if os.path.exists(VECTORSTORE_DIR):
            import shutil
            shutil.rmtree(VECTORSTORE_DIR)
            st.rerun()
        else:
            st.warning("Vector store not found.")

    if st.button("Delete Vector Store on Next Start"):
        st.session_state.delete_vs = True
        st.success("Vector store will be deleted next time you restart the app.")

