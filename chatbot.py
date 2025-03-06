import os
import chromadb
import cohere
from dotenv import load_dotenv
import logging
import sys

# Suppress all ChromaDB logs by setting the logging level to ERROR
logging.getLogger("chromadb").setLevel(logging.ERROR)

# Optionally, redirect stderr to null (completely hides unwanted logs)
sys.stderr = open(os.devnull, "w")


# Load API key
load_dotenv()
COHERE_API_KEY  = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

script_dir = os.path.dirname(__file__)  # Get path
db_path = os.path.join(script_dir, "chat_memory")


# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path=db_path)
chat_collection = chroma_client.get_or_create_collection("chat_history")


def store_interaction(user_input, ai_response):
    """Stores conversation history in vector storage with a proper ID."""
    existing_ids = chat_collection.get()["ids"] if chat_collection.get() else []
    new_id = str(len(existing_ids))  # Assign unique ID

    chat_collection.add(
        ids=[new_id],
        documents=[user_input],
        metadatas=[{"response": ai_response}]
    )



def retrieve_relevant_context(user_input):
    """Fetches past conversation based on relevance using vector search."""
    results = chat_collection.query(query_texts=[user_input], n_results=2)

    if not results.get("documents"):
        return ""

    retrieved_texts = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        retrieved_texts.append(f"{doc} -> {meta['response']}")

    return "\n".join(retrieved_texts)


def analyze_code(code):
    """Analyzes Python code while keeping the original version unique."""
    
    # Check if a previous "original_code" exists
    existing_original_code = retrieve_relevant_context("original_code")
    
    # If a new original code is provided, replace the previous one
    if existing_original_code.strip() and existing_original_code.strip() != code.strip():
        existing_ids = chat_collection.get()["ids"]
        if existing_ids:
            for idx in existing_ids:
                chat_collection.delete(ids=[idx])

    # Store the new original code
    store_interaction("original_code", code)  

    prompt = (
        "You are an expert Python mentor. "
        "Analyze the following code carefully:\n"
        f"{code}\n\n"
        "When responding, strictly follow these instructions:\n"
        "- Highlight syntax errors, missing imports, or inefficiencies, and **ask if the user would like help fixing them**.\n"
        "- Suggest improvements without rewriting code unless the user requests changes.\n"
        "- Keep the response natural and concise—like a mentor guiding their mentee.\n"
        "- Never rewrite or execute code unless the user explicitly requests it.\n"
        "- Always avoid paraphrasing and unnecessary repetition."
        "- Keep your response concise and sharp."
    )
    try:
        response = co.generate(model="command", temperature=0, prompt=prompt, max_tokens=300)
        return response.generations[0].text.strip()
    except Exception as e:
        print("Error : ",e)


def chat_with_ai(user_input):
    """Engages in a conversational dialogue while keeping the original code in context."""
    relevant_context = retrieve_relevant_context(user_input)
    original_code = retrieve_relevant_context("original_code")
    
    prompt = (
        "You are an expert Python mentor, continuing a conversation with the user. "
        "Here’s the original code and previous discussion for reference:\n"
        f"{original_code}\n\n"
        "Previous discussion:\n"
        f"{relevant_context}\n\n"
        "Strictly follow these instructions:\n"
        "- Maintain your role as a helpful Python mentor when responding. "
        "- Never mention Cohere or any language model information — always stick to your Python mentor persona.\n"
        "- Respond directly to the user's question **without unnecessary introductions or explanations**.\n"
        "- Respond to the user's question in a **concise and clear manner** while staying in your mentor role.\n"
        "- Only apologize if the question isn't about programming or your role as a Python mentor.\n"
        f"User: {user_input}"
    )

    response = co.generate(model="command", temperature=0, prompt=prompt, max_tokens=300).generations[0].text.strip()

    # Store interaction
    store_interaction(user_input, response)

    return response


def start_chat_mode():
    """Starts an interactive chat session."""
    while True:
        user_input = input("\nAsk me anything or type 'exit' to stop: ")
        if user_input.lower() == "exit":
            print("👋 Exiting chat mode...\n")
            break
        response = chat_with_ai(user_input)
        print(f"\n🤖 AI: {response}")
