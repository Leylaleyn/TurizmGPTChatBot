from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader  # 📄 PDF için bu loader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

# ********************** 1. PDF'den Veriyi Yükleme **********************
pdf_path = "Bes_yildizli_oteller.pdf"
loader = PyMuPDFLoader(pdf_path)
docs_list = loader.load()

# ********************** 2. Metinleri Küçük Parçalara Ayırma **********************
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, chunk_overlap=0
)
splits = text_splitter.split_documents(docs_list)

# ********************** 3. Vektör Veri Tabanı Oluşturma (Chroma) **********************
vectorstore = Chroma.from_documents(
    documents=splits,
    collection_name="rag-chroma",
    embedding=OpenAIEmbeddings(),
    persist_directory="./.chroma"
)

# ********************** 4. Retriever (Bilgi Getirici) Oluşturma **********************
retriever = Chroma(
    collection_name="rag-chroma",
    persist_directory="./.chroma",
    embedding_function=OpenAIEmbeddings(),
).as_retriever()
