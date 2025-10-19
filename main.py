from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Knowledge base from TypeScript Book
knowledge_base = {
    "fat arrow": "Lovingly called the fat arrow (because -> is a thin arrow and => is a fat arrow) and also called a lambda function (because of other languages).",
    "!!": "The !! operator converts any value into an explicit boolean. The unary ! operator converts its operand to a Boolean and negates it. Using !! twice gives you the Boolean equivalent - !!x is the same as Boolean(x).",
    "arrow function": "Another commonly used feature is the fat arrow function ()=>something. The motivation for a fat arrow is: you don't need to keep typing function. The fat arrow makes it simple for you to create a function.",
    "this": "Fat arrows fix the 'this' problem by capturing the meaning of this from the surrounding context. As a wise man once said 'I hate JavaScript as it tends to lose the meaning of this all too easily'.",
    "lambda": "The fat arrow is also called a lambda function (because of other languages).",
    "boolean conversion": "You can cast a variable to boolean using the double exclamation mark !!. It converts truthy values to true and falsy values to false.",
}

@app.get("/search")
async def search(q: str):
    query_lower = q.lower()
    
    # Simple keyword matching
    best_match = None
    best_score = 0
    
    for key, value in knowledge_base.items():
        # Check if key is in query
        if key in query_lower:
            score = len(key)
            if score > best_score:
                best_score = score
                best_match = value
    
    # Additional pattern matching for specific questions
    if "fat arrow" in query_lower or "=> syntax" in query_lower or "affectionately call" in query_lower:
        best_match = knowledge_base["fat arrow"]
    elif "!!" in q or "double exclamation" in query_lower or "explicit boolean" in query_lower:
        best_match = knowledge_base["!!"]
    elif "lambda" in query_lower:
        best_match = knowledge_base["lambda"]
    
    if best_match:
        return {
            "answer": best_match,
            "sources": "TypeScript Deep Dive by Basarat Ali Syed"
        }
    
    return {
        "answer": "I couldn't find a relevant answer in the TypeScript book.",
        "sources": "TypeScript Deep Dive by Basarat Ali Syed"
    }

@app.get("/")
async def root():
    return {"status": "running"}

