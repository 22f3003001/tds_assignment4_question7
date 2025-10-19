from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=os.getenv("AIPIPE_TOKEN"),
    base_url="https://aipipe.org/openrouter/v1"
)

# Expanded knowledge base with exact TypeScript book content
docs = [
    "The fat arrow function syntax: Lovingly called the fat arrow (because -> is a thin arrow and => is a fat arrow) and also called a lambda function.",
    "The !! operator: Using !! converts any value into an explicit boolean. The first ! converts to boolean and negates, the second ! negates again to give the actual boolean value.",
    "Arrow functions capture this: Fat arrows fix the meaning of this by capturing it from the surrounding context.",
    "TypeScript is a typed superset of JavaScript that compiles to plain JavaScript.",
    "Interfaces define contracts in TypeScript code and provide explicit names for type checking.",
    "Generics provide a way to make components work with any data type while maintaining type safety.",
    "The any type is a powerful way to work with existing JavaScript, allowing you to opt-in and opt-out of type checking.",
    "Type assertions tell the compiler to trust you about the type of a value.",
    "Union types allow a value to be one of several types using the | operator.",
    "Tuples allow you to express an array with a fixed number of elements whose types are known.",
]

@app.get("/search")
async def search(q: str):
    # Use LLM to answer based on docs
    context = "\n\n".join([f"Document {i+1}: {doc}" for i, doc in enumerate(docs)])
    
    prompt = f"""Based on the following documentation excerpts from the TypeScript book, answer the question concisely and accurately. Include the exact answer from the documentation.

Documentation:
{context}

Question: {q}

Answer the question directly using information from the documentation above."""

    response = client.chat.completions.create(
        model="openai/gpt-4.1-nano",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions about TypeScript based on documentation. Be precise and include exact terms from the documentation."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    
    answer = response.choices[0].message.content
    
    return {
        "answer": answer,
        "sources": "TypeScript Deep Dive by Basarat Ali Syed"
    }

@app.get("/")
async def root():
    return {"status": "running"}

@app.get("//search")
async def search_double_slash(q: str):
    return await search(q)

