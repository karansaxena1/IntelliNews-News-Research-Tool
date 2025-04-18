import os
import pickle
import streamlit as st
import faiss
from dotenv import load_dotenv
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.faiss import InMemoryDocstore
import validators

# Load environment variables
load_dotenv()

st.set_page_config(page_title="IntelliNews - News Research", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #f8f8f8; }
    .stTextInput > div > div > input {
        background-color: #111; color: #f8f8f8; border: 1px solid #f87171; border-radius: 6px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #f87171; box-shadow: 0 0 6px rgba(248, 113, 113, 0.4);
    }
    .stButton > button {
        background-color: #ef4444; color: white; border: none;
        padding: 10px 20px; border-radius: 6px; font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #dc2626;
    }
    .stMarkdown code {
        color: #f87171;
    }
    .made-with-love {
        font-size: 15px;
        color: #777;
        margin-top: 20px;
        text-align: center;
    }
    .made-with-love a {
        color: #f87171;
        text-decoration: none;
    }
    .made-with-love a:hover {
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🕵️‍♂️ IntelliNews: News Research Tool")
st.sidebar.title("Paste up to 3 news article URLs")

# Sidebar input
urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}", placeholder="https://example.com/article", key=f"url_{i}")
    if url.strip():
        urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")

index_file = "faiss_index.bin"
docs_file = "faiss_docs.pkl"

# Verify API key
if not os.getenv("GOOGLE_API_KEY"):
    st.error("❌ GOOGLE_API_KEY not set.")
    st.stop()

# Initialize LLM & embeddings
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
    max_output_tokens=500
)

try:
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
except Exception as e:
    st.error(f"Failed to initialize embeddings: {e}")
    st.stop()

# Process URLs
if process_url_clicked:
    if not urls:
        st.error("Please enter at least one URL.")
    elif not all(validators.url(url) for url in urls):
        st.error("One or more URLs are invalid.")
    else:
        try:
            st.info("Loading and processing articles 📰...")
            loader = WebBaseLoader(
                web_paths=urls,
                requests_kwargs={"headers": {"User-Agent": "IntelliNewsInsights/1.0"}}
            )
            data = loader.load()
             
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            docs = text_splitter.split_documents(data)

            vectorstore = FAISS.from_documents(docs, embeddings)
            faiss.write_index(vectorstore.index, index_file)
            with open(docs_file, "wb") as f:
                pickle.dump(docs, f)

            st.success("✅ Articles processed. Ask a question below.")
        except Exception as e:
            st.error(f"Processing failed: {e}")
            st.stop()

# Ask a question
st.markdown("### 🔎 Ask a question about the articles:")
query = st.text_input("Your Question", placeholder="e.g., What are the key takeaways?", label_visibility="collapsed")
ask_clicked = st.button("🧠 Ask Question")

if ask_clicked and query:
    if os.path.exists(index_file) and os.path.exists(docs_file):
        try:
            index = faiss.read_index(index_file)
            with open(docs_file, "rb") as f:
                docs = pickle.load(f)

            docstore = InMemoryDocstore({str(i): doc for i, doc in enumerate(docs)})
            index_to_docstore_id = {i: str(i) for i in range(len(docs))}
            vectorstore = FAISS(
                embedding_function=embeddings,
                index=index,
                docstore=docstore,
                index_to_docstore_id=index_to_docstore_id
            )

            search_results = vectorstore.similarity_search(query, k=4)
            if not search_results:
                st.warning("No relevant info found.")
                st.stop()

            chain = RetrievalQAWithSourcesChain.from_llm(
                llm=llm,
                retriever=vectorstore.as_retriever(search_kwargs={"k": 4})
            )

            with st.spinner("Generating answer..."):
                result = chain.invoke({"question": query})  # ✅ Updated to use `.invoke()`

            answer = result["answer"]
            sources_raw = result.get("sources", "")

            # Handle both string and list of sources
            if isinstance(sources_raw, list):
                sources = [s.strip() for s in sources_raw if s.strip()]
            else:
                sources = [s.strip() for s in sources_raw.split("\n") if s.strip()]

            # Store in session memory
            st.session_state.chat_history.append({
                "question": query,
                "answer": answer,
                "sources": sources
            })

        except Exception as e:
            st.error(f"Query error: {e}")
    else:
        st.warning("Please process the URLs first.")

# Display chat history
if st.session_state.chat_history:
    st.markdown("---")
    st.subheader("🗃️ Conversation History")
    for i, chat in enumerate(reversed(st.session_state.chat_history), 1):
        st.markdown(f"**Q{i}:** {chat['question']}")
        st.markdown(f"**A{i}:** {chat['answer']}")
        if chat.get("sources"):
            st.markdown("**Sources:**")
            for src in chat["sources"]:
                st.markdown(f"- [{src}]({src})")
        st.markdown("---")

st.markdown("<div class='made-with-love'>Made with ❤️ by <a href='https://www.linkedin.com/in/karan1saxena/' target='_blank'>Karan Saxena</a></div>", unsafe_allow_html=True)
