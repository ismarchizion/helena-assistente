import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader

# Carrega a chave da OpenAI do .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Caminhos
DOCUMENTOS_DIR = "documents"
CHROMA_DIR = "vectorstore"

# 🔎 Carrega todos os documentos .txt e .pdf da pasta "documents"
def carregar_documentos():
    documentos = []
    if not os.path.exists(DOCUMENTOS_DIR):
        raise FileNotFoundError(f"Pasta '{DOCUMENTOS_DIR}' não encontrada.")

    for filename in os.listdir(DOCUMENTOS_DIR):
        path = os.path.join(DOCUMENTOS_DIR, filename)
        try:
            if filename.endswith(".txt"):
                loader = TextLoader(path, encoding="utf-8")
                documentos.extend(loader.load())
            elif filename.endswith(".pdf"):
                loader = PyPDFLoader(path)
                documentos.extend(loader.load())
        except Exception as e:
            print(f"Erro ao carregar '{filename}': {e}")
    return documentos

# ⚙️ Constrói a base vetorial com embeddings da OpenAI
def construir_base_de_conhecimento():
    if not openai_api_key:
        raise EnvironmentError("❌ OPENAI_API_KEY não encontrada no .env")

    documentos = carregar_documentos()
    if not documentos:
        raise ValueError("❌ Nenhum documento carregado para indexação.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(documentos)

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    print("✅ Base de conhecimento vetorial construída com sucesso!")
# 🗂️ Carrega a base de conhecimento vetorial
# 🤖 Realiza busca por similaridade na base Chroma
def responder_com_base(pergunta):
    if not openai_api_key:
        raise EnvironmentError("❌ OPENAI_API_KEY não encontrada no .env")

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)

    try:
        resultados = db.similarity_search(pergunta, k=3)
        if not resultados:
            return "Desculpe, não encontrei informações relevantes na base."
        resposta = "\n---\n".join([doc.page_content for doc in resultados])
        return resposta
    except Exception as e:
        return f"Erro ao buscar na base de conhecimento: {e}"
