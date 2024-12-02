from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.faiss import FAISS  # Update import path if necessary
from langchain.docstore.document import Document
import os
import pickle
import logging

logger = logging.getLogger(__name__)

class PDFIndexer:
    def __init__(self, pdf_text, pdf_id):
        self.pdf_text = pdf_text
        self.pdf_id = pdf_id
        self.embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        self.index_file_path = f"app/indices/{self.pdf_id}_faiss_index.pkl"
        self.vector_store = None

    async def build_index(self):
        try:
            if os.path.exists(self.index_file_path):
                with open(self.index_file_path, "rb") as f:
                    self.vector_store = pickle.load(f)
            else:
                text_splitter = CharacterTextSplitter(
                    separator="\n",
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len,
                )
                chunks = text_splitter.split_text(self.pdf_text)
                docs = [Document(page_content=chunk) for chunk in chunks]
                self.vector_store = FAISS.from_documents(docs, self.embeddings)
                os.makedirs(os.path.dirname(self.index_file_path), exist_ok=True)
                with open(self.index_file_path, "wb") as f:
                    pickle.dump(self.vector_store, f)
        except Exception as e:
            logger.error(f"Error building index for PDF {self.pdf_id}: {e}", exc_info=True)
            raise e

    async def get_relevant_text(self, query):
        try:
            if self.vector_store is None:
                await self.build_index()
            similar_docs = self.vector_store.similarity_search(query)
            relevant_text = "\n".join([doc.page_content for doc in similar_docs])
            return relevant_text
        except Exception as e:
            logger.error(f"Error retrieving relevant text: {e}", exc_info=True)
            raise e
