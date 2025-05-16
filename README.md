
## 🛡️ Phishing URL Detector — RAG-Based AI Web App

> Detect whether a URL is **Legit or Phishing** using cutting-edge **RAG (Retrieval-Augmented Generation)**, **Pinecone vector DB**, and **Groq’s LLaMA 3 model** — all wrapped in a slick Streamlit app.

---

### 🚀 Features

* 🧠 **LLM Reasoning**: Uses Groq’s LLaMA 3 to explain *why* a URL might be phishing.
* 🔍 **Knowledge-Augmented**: Retrieves relevant facts from a Pinecone-powered knowledge base.
* 🖥️ **Real-Time Streamlit UI**: No REST APIs, just paste a URL and boom — verdict + explanation.
* 📦 Lightweight & Deployable: Run it locally or deploy to Streamlit Cloud/Render/VPS.

---

### 📸 Demo Screenshot

*(Insert screenshot here if you’ve got one — use `st.screenshot()` or take one from browser)*
![image](https://github.com/user-attachments/assets/997156c5-b919-4c9b-9e23-c86b5ed6690e)

---

### ⚙️ How It Works

1. User enters a URL
2. Features like `uses IP`, `has @ symbol`, `HTTPS status` etc. are extracted
3. These are turned into a text query
4. The query retrieves top-k facts from your Pinecone vector DB
5. A LLaMA 3 model from Groq uses both features + context to classify the URL
6. Verdict + LLM explanation is shown in the UI

---

### 🛠️ Tech Stack

* 🧠 **Groq API** – LLaMA 3 for fast, smart reasoning
* 📚 **Pinecone** – semantic search over phishing knowledge base
* 🧩 **Sentence Transformers** – for embedding queries
* 🖼️ **Streamlit** – interactive UI
* 🔐 `.env` for API secrets

---

### 📦 Setup & Run Locally

#### 1. Clone the repo

```bash
git clone https://github.com/your-username/phishing-detector.git
cd phishing-detector
```

#### 2. Install dependencies

```bash
pip install -r requirements.txt
```

#### 3. Add your `.env` file

```env
PINECONE_API_KEY=your_key_here
GROQ_API_KEY=your_groq_key_here
```

#### 4. Run the Streamlit app

```bash
streamlit run app.py
```

---

### 🌐 Deploy It

#### Option A: [Streamlit Cloud](https://streamlit.io/cloud)

1. Push to GitHub
2. Go to Streamlit Cloud → New App
3. Link your repo and set secrets (`PINECONE_API_KEY`, `GROQ_API_KEY`)
4. Boom — you’re live

#### Option B: [Render.com](https://render.com)

* Supports Python web services
* Use `gunicorn app:app` if switching to Flask version

---

### 📁 Project Structure

```bash
📦 phishing-detector/
├── app.py                  # Streamlit app logic
├── requirements.txt        # Dependencies
├── .env                    # Secret keys (not committed)
├── phishing_rag_knowledge_base.json
└── README.md               # This file 😎
```

---

### 🧪 Sample Output

```txt
Verdict: Phishing 🚨

Reasoning: The URL contains an IP address, uses HTTP instead of HTTPS, and includes suspicious patterns often associated with phishing campaigns. Based on similar entries in the knowledge base, this is highly likely to be a phishing attempt.
```

---

### 🤝 Contributing

Want to help make this smarter? PRs welcome. You can:

* Add new features
* Improve UI
* Add more KB entries
* Connect it to a database or logging system

---

### 🧙‍♂️ Credits

Built by [Yash](#) with cyber wizardry, coffee, and a suspicious amount of paranoia.

---

### 📜 License

MIT — because you deserve freedom, not license jail.
