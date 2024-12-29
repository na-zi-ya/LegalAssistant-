import openai
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set your OpenAI API Key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")


def analyze_legal_document(text, prompt_type, question=None):
    """
    Analyze a legal document based on the provided prompt type.
    Args:
        text (str): The content of the legal document.
        prompt_type (str): The type of analysis (e.g., summarize, extract key clauses, Q&A).
        question (str): The specific question to answer (for Q&A prompt type).
    Returns:
        str: The analysis result.
    """
    if prompt_type == "summarize":
        prompt = f"Summarize the following legal document in concise terms:\n\n{text}"
    elif prompt_type == "extract_clauses":
        prompt = f"Extract the key clauses from the following legal document:\n\n{text}"
    elif prompt_type == "qa":
        if not question:
            return "No question provided for Q&A."
        prompt = f"Answer the following question based on the legal document:\n\nDocument: {text}\n\nQuestion: {question}"
    else:
        return "Invalid prompt type"

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Change model to suit your needs (e.g., gpt-4, if available)
            # prompt=prompt,
              messages=[
        {"role": "system", "content": "You are a helpful assistant for analyzing legal documents."},
        {"role": "user", "content": prompt}
    ],
            max_tokens=1500,
            temperature=0.2,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Analyze endpoint to process legal documents.
    """
    try:
        data = request.json
        text = data["text"]
        prompt_type = data["prompt_type"]  # summarize, extract_clauses, qa
        question = data.get("question")  # Optional for Q&A
        result = analyze_legal_document(text, prompt_type, question)
        return jsonify({"status": "success", "result": result})
    except KeyError as e:
        return jsonify({"status": "error", "message": f"Missing field: {e}"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
