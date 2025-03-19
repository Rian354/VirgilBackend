from app import app
from flask import request, jsonify
from langchain_ollama import OllamaLLM


llm = OllamaLLM(model="llama3.1")


@app.route("/chat", methods=['POST'])
def chat():
    """
        This endpoint takes a user input and returns a response from the Ollama model.
        """
    data = request.json
    user_prompt = data.get("prompt")

    if not user_prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        response = llm.invoke(input=user_prompt)
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500
