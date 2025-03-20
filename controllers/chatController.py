import os.path

from app import app
from flask import request, jsonify
from langchain_ollama import OllamaLLM
from werkzeug.utils import secure_filename
from langchain.document_loaders import (PyPDFLoader, Docx2txtLoader, TextLoader)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain.chains import RetrievalQA

llm = OllamaLLM(model="llama3.1")
FILE_UPLOAD_DIRECTORY = 'uploads'
_MODEL = "llama3.1"
VECTOR_STORE_DB='vector_store'

embeddings = OllamaEmbeddings(
    model=_MODEL,
)

@app.route("/llm_chat", methods=['POST'])
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

@app.route("/chat", methods=['POST'])
def invoiceChat():
    """
           This endpoint takes a user input and returns a response from the Ollama model.
           """
    data = request.json
    user_prompt = data.get("prompt")

    if not user_prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        vectorStore = FAISS.load_local(VECTOR_STORE_DB, embeddings, allow_dangerous_deserialization=True)
        retriever = vectorStore.as_retriever()

        qa_chain = RetrievalQA.from_llm(
            llm, retriever=retriever
        )

        response = qa_chain.run(user_prompt)
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def isFileValid(file):
    name = file.filename
    return name != '' and '.' in name and name.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'doc', 'docx'}


def fileLoader(path, type):
    if type == 'pdf':
        return PyPDFLoader(path).load()
    if type in {'doc', 'docx'}:
        return Docx2txtLoader(path).load()
    if type == 'text':
        return TextLoader(path).load()
    else:
        raise ValueError('Error: unsupported file format')


def getVectorStore(files):
    textSplitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20, length_function=len,
                                                  is_separator_regex=False)
    _docs = []
    for file in files:
        doc = textSplitter.split_documents([file])
        _docs.extend(doc)

    limitedFiles = _docs[:2]

    vectorStore = FAISS.from_documents(limitedFiles, embeddings)
    return vectorStore

@app.route("/upload", methods=['POST'])
def upload_doc_to_vector_store():
    # Ensure a file is provided
    if 'file' not in request.files:
        print("Files received:", request.files.keys())
        return jsonify({'status': 'Bad Request', 'error': 'No file provided'}), 400

    file = request.files['file']
    if not isFileValid(file):
        return jsonify({'status': 'Bad Request', 'error': 'Invalid file selection'}), 400

    name = secure_filename(file.filename)
    file_path = os.path.join(FILE_UPLOAD_DIRECTORY, name)

    # Ensure the upload directory exists
    if not os.path.exists(FILE_UPLOAD_DIRECTORY):
        os.makedirs(FILE_UPLOAD_DIRECTORY, exist_ok=True)

    try:
        file.save(file_path)
    except Exception as e:
        return jsonify({'status': 'Error', 'message': f'Failed to save file: {str(e)}'}), 500

    try:
        file_extension = name.rsplit('.', 1)[1].lower()
        docs = fileLoader(file_path, file_extension)
        vector_store = getVectorStore(docs)
        vector_store.save_local(VECTOR_STORE_DB)
        return jsonify({'message': f'File {name} is saved in vectorStore successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


#
# @app.route("/upload", methods=['POST'])
# def upload_doc_to_vector_store():
#     # Ensure a file is provided
#     if 'file' not in request.files:
#         print("Files received:", request.files.keys())
#         return jsonify({'status': 'Bad Request', 'error': 'No file provided'}), 400
#
#     file = request.files['file']
#     if not isFileValid(file):
#         return jsonify({'status': 'Bad Request', 'error': 'Invalid file selection'}), 400
#
#     name = secure_filename(file.filename)
#     file_path = os.path.join(FILE_UPLOAD_DIRECTORY, name)
#
#     try:
#         file.save(file_path)
#     except Exception as e:
#         return jsonify({'status': 'Error', 'message': f'Failed to save file: {str(e)}'}), 500
#
#     try:
#         file_extension = name.rsplit('.', 1)[1].lower()
#         docs = fileLoader(file_path, file_extension)
#         vector_store = getVectorStore(docs)  # Corrected function name
#         vector_store.save_local(VECTOR_STORE_DB)
#         return jsonify({'message': f'File {name} is saved in vectorStore successfully'}), 200
#     except Exception as e:
#         return jsonify({'message': str(e)}), 400

