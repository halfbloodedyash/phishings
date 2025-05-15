import streamlit as st
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from urllib.parse import urlparse
import ipaddress, json, os, requests

# --- Secrets ---
PINECONE_API_KEY = "pcsk_3NCxVP_9RajCoFsbr2H83sERanRhsLKuZL6QLfWc24t56NC1QADYuR31jbH3CMnFNpbH97"
GROQ_API_KEY = "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"
INDEX_NAME = "phishing-rag"

# --- Init ---
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

with open("phishing_rag_knowledge_base.json", "r") as f:
    knowledge_base = json.load(f)

# --- Functions ---
def extract_features(url):
    parsed = urlparse(url)
    features = {
        "url_length": len(url),
        "has_https": parsed.scheme == "https",
        "subdomain_count": parsed.netloc.count("."),
        "has_ip": False,
        "has_at_symbol": '@' in url,
    }
    try:
        ipaddress.ip_address(parsed.hostname)
        features["has_ip"] = True
    except:
        features["has_ip"] = False
    return features

def features_to_text(features):
    parts = [
        f"URL is {features['url_length']} characters long",
        "uses HTTPS" if features['has_https'] else "does not use HTTPS",
        f"has {features['subdomain_count']} subdomains"
    ]
    if features["has_ip"]:
        parts.append("uses an IP address")
    if features["has_at_symbol"]:
        parts.append("contains an '@' symbol")
    return ", ".join(parts) + "."

def retrieve_context(query_text, top_k=5):
    query_embedding = embedder.encode(query_text).tolist()
    result = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    return [match['metadata']['content'] for match in result['matches']]

def classify_url(url):
    features = extract_features(url)
    query_text = features_to_text(features)
    context_chunks = retrieve_context(query_text)

    prompt = f"""
You are a cybersecurity expert.

Given the URL features and supporting context below, determine if the URL is phishing or legitimate.

URL: {url}
Features: {query_text}

Knowledge Base:
{chr(10).join(context_chunks)}

Explain your reasoning and give your final classification as 'Legit' or 'Phishing'.
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {"role": "system", "content": "You are a cybersecurity analyst."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

# --- Streamlit UI ---
st.title("🔐 Phishing URL Detector")
st.write("Enter a URL and we'll tell you if it's shady or safe...")

url_input = st.text_input("Enter URL:")

if st.button("Analyze"):
    if url_input:
        with st.spinner("Consulting LLaMA..."):
            try:
                result = classify_url(url_input)
                st.success("Result:")
                st.markdown(result)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid URL.")
