# 🕵️‍♂️ IntelliNews: News Research Tool 📑

**IntelliNews** is a powerful, AI-driven web application designed to streamline news research by allowing users to process up to three news article URLs, extract their content, and query them intelligently using natural language. Powered by **Streamlit**, **LangChain**, **FAISS**, and **Google Generative AI**, IntelliNews leverages advanced embeddings and large language models (LLMs) to provide accurate, source-backed answers to user questions. 🚀

---

Working Link 

https://intellinews-news-research.streamlit.app/

---

![Screenshot 2025-04-18 110107](https://github.com/user-attachments/assets/5d6a25df-e5dd-4bef-9dfb-0c9f9984941b)

## 🌟 Features

- **URL Processing**: Input up to three news article URLs to extract and process their content. 🌐
- **Text Chunking**: Splits articles into manageable chunks for efficient retrieval using `RecursiveCharacterTextSplitter`. 📄
- **Vector Store**: Uses **FAISS** to create a vector store for fast similarity search with **Google Generative AI Embeddings**. 🔍
- **Intelligent Q&A**: Query processed articles with natural language, powered by **Google Gemini 1.5 Flash** LLM and **RetrievalQAWithSourcesChain**. 🧠
- **Session Memory**: Maintains a conversation history to track questions, answers, and sources. 🗃️
- **Modern UI**: Sleek, dark-themed interface with custom CSS styling, built using **Streamlit**. 🎨
- **Source Attribution**: Provides clickable source links for transparency and credibility. 📚
- **Error Handling**: Robust validation for URLs and API keys, with user-friendly error messages. ⚠️

---

## 🛠️ Tech Stack

- **Python**: Core programming language (3.8+).
- **Streamlit**: Frontend framework for building the web app.
- **LangChain**: Orchestrates LLM workflows, embeddings, and retrieval chains.
- **FAISS**: Efficient vector store for similarity search.
- **Google Generative AI**: Powers embeddings (`embedding-001`) and LLM (`gemini-1.5-flash`).
- **Validators**: Ensures valid URLs.
- **Pickle**: Serializes documents for persistence.
- **Dotenv**: Manages environment variables securely.

---

## 📋 Prerequisites

Before running IntelliNews, ensure you have the following:

- **Python 3.8+** installed.
- A **Google API Key** with access to Google Generative AI services.
- Basic familiarity with command-line tools and Python package management.

---

## 🚀 Installation

Follow these steps to set up IntelliNews locally:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/intellinews.git
   cd intellinews
   ```

2. **Create a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**: Create a `.env` file in the project root and add your Google API key:

   ```env
   GOOGLE_API_KEY=your-google-api-key
   ```

5. **Run the Application**:

   ```bash
   streamlit run app.py
   ```

   The app will open in your default browser at `http://localhost:8501`.

---

## 📝 Usage

1. **Enter URLs**:

   - In the sidebar, paste up to three news article URLs (e.g., `https://example.com/article`).
   - Click **Process URLs** to load and process the articles. 📰

2. **Ask Questions**:

   - In the main panel, type a question about the articles (e.g., "What are the key takeaways?").
   - Click **Ask Question** to get an AI-generated answer with source attribution. 🔎

3. **View History**:

   - Scroll down to see the conversation history, including questions, answers, and clickable source links. 🗃️

4. **Error Handling**:

   - Invalid URLs or missing API keys will trigger clear error messages.
   - If no relevant information is found, a warning will be displayed.

---

## 📂 Project Structure

```plaintext
intellinews/
├── app.py                # Main Streamlit application
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not tracked)
├── faiss_index.bin       # FAISS index file (generated)
├── faiss_docs.pkl        # Serialized documents (generated)
├── README.md             # Project documentation
```

---

## 🔧 Configuration

- **Chunk Size**: The `RecursiveCharacterTextSplitter` uses a chunk size of 1000 characters with a 200-character overlap. Adjust in `app.py` if needed.
- **Embedding Model**: Uses `models/embedding-001`. Update in `app.py` for other Google embedding models.
- **LLM Model**: Uses `gemini-1.5-flash`. Modify in `app.py` to use other Google LLMs.
- **Max Output Tokens**: Set to 500 for concise answers. Adjust in `app.py` for longer or shorter responses.
- **FAISS Index**: Stored as `faiss_index.bin` and documents as `faiss_docs.pkl`. These are generated after processing URLs.

---

## 🐛 Troubleshooting

- **API Key Error**: Ensure the `GOOGLE_API_KEY` is set in the `.env` file and is valid.
- **Invalid URLs**: Verify that URLs are accessible and properly formatted (e.g., include `https://`).
- **Processing Failure**: Check internet connectivity and ensure the URLs point to text-based articles.
- **No Relevant Info**: Rephrase the question or process additional articles.
- **Dependency Issues**: Run `pip install -r requirements.txt` to ensure all packages are installed.

For further assistance, open an issue on the GitHub repository.

---

## 🙌 Acknowledgments

- **Streamlit**: For an intuitive web app framework.
- **LangChain**: For seamless integration with LLMs and vector stores.
- **Google Generative AI**: For powerful embeddings and LLM capabilities.
- **FAISS**: For efficient similarity search.
- Made with ❤️ by Karan Saxena.

---

## 🌐 Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please ensure your code follows PEP 8 standards and includes relevant tests.

---

## 📬 Contact

For questions or feedback, reach out to Karan Saxena or open an issue on GitHub.

Happy researching! 🕵️‍♂️
