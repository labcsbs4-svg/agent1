# 📚 ClearQuery AI - Creative Solutions Inc. company's Knowledge Base Agent

A smart, AI-powered internal assistant designed to answer questions about your company’s policies, products, and documents.  
This agent uses **RAG (Retrieval-Augmented Generation)** to search your internal markdown documents and generate accurate, helpful responses using **Google Gemini**.

Built with:

- **Streamlit** for the UI  
- **LangChain (0.2.x)** for retrieval and chain logic  
- **HuggingFace sentence-transformers** for local embeddings  
- **ChromaDB** for vector storage  
- **Gemini 2.0 Flash** for answer generation  

---

## 🚀 Features

### 🧠 AI-Powered Q&A  
Ask natural questions like:

- “What is InnovateHub?”
- “How many vacation days do we get?”
- “Tell me about Creative Solutions Inc.”

- "What all products does the company offer ?"
- "What is InnovateHub?"
- "How many vacation days do we get?"
- "What is the work-from-home policy ?"
- "And much more.... Happy to assist you !!"

The agent retrieves relevant markdown content and generates context-aware responses.

### 📄 Markdown-Based Knowledge Base  
Add `.md` documents to the `documents/` folder.  
Examples:

- `about_us.md`
- `policies.md`
- `products.md`

### 🧩 Retrieval + LLM Pipeline  
- Uses **local HuggingFace embeddings** (no API quota needed)  
- Fast and efficient vector search using ChromaDB  
- Gemini used only for final answer generation  

### 🖥 Clean Chat Interface  
- Interactive Streamlit UI  
- Chat history saved across interactions  

### 🗑 One-Click Vector Store Reset  
A sidebar button allows deleting and rebuilding the vector database.

---

## 🛠 Tech Stack

| Component        | Technology                                   |
|------------------|----------------------------------------------|
| Frontend UI      | Streamlit                                    |
| Embeddings       | sentence-transformers (MiniLM-L6-v2)         |
| Vector DB        | ChromaDB                                     |
| Document Loader  | LangChain TextLoader                         |
| Text Splitting   | RecursiveCharacterTextSplitter               |
| LLM              | Gemini 2.0 Flash                             |
| RAG Pipeline     | LangChain Retrieval + Stuff Documents Chain  |

---

## 📁 Project Structure

```

project-folder/
│
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
├── documents/                 # Markdown knowledge base files
│   ├── about_us.md
│   ├── policies.md
│   └── products.md
│
├── chroma_db/                 # Auto-generated vectorstore (DO NOT COMMIT)
│
├── .gitignore
└── README.md

````

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
````

---

### 2️⃣ Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

Your `requirements.txt` should include:

```txt
streamlit==1.39.0
python-dotenv==1.0.1

langchain==0.2.11
langchain-core==0.2.36
langchain-community==0.2.10
langchain-text-splitters==0.2.2

langchain-google-genai==1.0.7
google-generativeai==0.7.2

sentence-transformers==3.1.1
chromadb==0.5.4

pypdf==4.3.1
```

---

### 4️⃣ Add your documents

Place your `.md` files inside the `documents/` folder:

```
documents/
 ├── about_us.md
 ├── policies.md
 └── products.md
```

---

### 5️⃣ Set up your Google API Key

Create a `.env` file:

```
GOOGLE_API_KEY=your_google_gemini_api_key
```

---

### 6️⃣ Run the app locally

```bash
streamlit run app.py
```

App will run at:

```
http://localhost:8501
```

---

## 🌐 Deployment (Streamlit Cloud)

### 1️⃣ Push your repository to GitHub

Make sure you do **NOT** commit the vectorstore or environment files.

Your `.gitignore` should contain:

```gitignore
chroma_db/
.env
venv/
__pycache__/
```

---

### 2️⃣ Add Streamlit Cloud secrets

Go to:

```
Streamlit Cloud → Your App → Settings → Secrets
```

Paste this:

```toml
GOOGLE_API_KEY = "your_real_google_api_key"
```

---

### 3️⃣ Deploy

1. Go to Streamlit Cloud
2. Click **“New App”**
3. Select your repo
4. Set the main file to:

```
app.py
```

Click **Deploy** 🎉

Streamlit will automatically:

* Install dependencies
* Build your vectorstore
* Launch the app

---

## 🔧 Troubleshooting

### ❗ “failed to find libmagic”

Cause: Some loaders require `unstructured`.

✔ Already fixed — project now uses `TextLoader`.

---

### ❗ PermissionError deleting `chroma_db`

Cause: SQLite DB open on Windows.

Fix:

1. Stop Streamlit (`Ctrl + C`)
2. Delete folder manually
3. Restart app

---

### ❗ Vector store KeyError "_type"

Cause: Old index created with a different LangChain version.

Fix:

* Delete `chroma_db/` folder
* Restart the app

---

### ❗ Deployment errors due to dependency conflict

Fix:

* Use the exact pinned versions shown above.

---

## 💡 Future Improvements

* Admin panel for uploading new documents
* User authentication / roles
* Source citation links
* Multi-document preview
* Branding & custom themes
* Persistent long-term chat memory

---

