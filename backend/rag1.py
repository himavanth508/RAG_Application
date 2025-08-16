from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
import os
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from db import vectors_collection
from langchain.vectorstores.mongodb_atlas import MongoDBAtlasVectorSearch

os.environ["GOOGLE_API_KEY"] = ""        


embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
DB_DIR = "vector_store"
INDEX_SUBDIR = "faiss_index"
INDEX_FILE = os.path.join(DB_DIR, INDEX_SUBDIR)

def ingest_file(path, user_id):
    try:
        filename = os.path.basename(path)
        exists = vectors_collection.find_one({"user_id": str(user_id), "filename": filename})
        if exists:
            raise ValueError("A file with this name already exists for this user.")

        loader = PyMuPDFLoader(path) if path.endswith(".pdf") else TextLoader(path, encoding="utf-8")
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = splitter.split_documents(docs)

        for chunk in chunks:
            chunk.metadata["user_id"] = str(user_id)
            chunk.metadata["filename"] = filename

        vectorstore = MongoDBAtlasVectorSearch.from_documents(
            documents=chunks,
            embedding=embedding,
            collection=vectors_collection,
            index_name="vector_index",
        )

        vectors_collection.insert_one({
            "user_id": str(user_id),
            "filename": filename,
            "status": "indexed"
        })

    except Exception as e:
        print(f"[ingest_file] Error: {e}")
        raise f"Error: {e}"


def get_answer(query, user_id):
    try:
        # Filter vectors belonging to this user only
        vectorstore = MongoDBAtlasVectorSearch(
            embedding=embedding,
            collection=vectors_collection,
            index_name="vector_index",
        )
        print(f"Retrieving vectors for user_id: {user_id}")
        print("Vectorstore:", vectorstore)

        retriever = vectorstore.as_retriever(
            search_kwargs={"pre_filter": {"user_id": str(user_id)}}
        )
        # retriever = vectorstore.as_retriever()
        print("Retriever created with user_id filter:", retriever)

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.2,
            convert_system_message_to_human=True
        )

        system_prompt = """You are a helpful and friendly assistant. 
        You can respond casually and naturally to greetings like 'Hi', 'Hello', or 'Hey'.
        When a user asks a question, use the context below to answer accurately.
        Context: {context}
        Question: {input}
        Answer:"""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

        qa_chain = create_stuff_documents_chain(llm, prompt)
        chain = create_retrieval_chain(retriever, qa_chain)
        response = chain.invoke({"input": query})
        return response.get("answer", "No answer found.")

    except Exception as e:
        print(f"[get_answer] Error: {e}")
        return f"Error: {e}"
