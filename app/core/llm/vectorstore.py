"""Create Pinecone Vector Store and Text Splitter"""

from pinecone import Pinecone
from pinecone.models import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config.settings import pine_cone_settings, recursive_splitter_settings
from app.core.llm.models import get_embedded_model


def create_text_splitter(output_data: str) -> RecursiveCharacterTextSplitter:
    """Split output text using the configured recursive character splitter."""
    chunk_size = recursive_splitter_settings.RECURSIVE_SPLITTER_CHUNK_SIZE
    chunk_overlap = recursive_splitter_settings.RECURSIVE_SPLITTER_CHUNK_OVERLAP
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    string_chunks = text_splitter.split_text(output_data)
    return text_splitter.create_documents(string_chunks)


class NewPineConeVectorStore:
    """Create and expose the application's Pinecone vector store."""

    # This class intentionally provides one public operation.
    # pylint: disable=too-few-public-methods

    def __init__(self):
        self.__pinecone = Pinecone
        self.__pine_cone_vector_settings = PineconeVectorStore
        self.__server_less_spec = ServerlessSpec

    def __get_pinecone(self) -> Pinecone:
        """Return a Pinecone client configured with the application API key."""
        return self.__pinecone(api_key=pine_cone_settings.PINECONE_API_KEY)

    def __create_pinecone_index(self) -> Pinecone:
        """Create the configured Pinecone index if it does not already exist."""
        pinecone_index_name = pine_cone_settings.PINECONE_INDEX_NAME
        pine_cone = self.__get_pinecone()
        if not pine_cone.has_index(pinecone_index_name):
            pine_cone.create_index(
                name=pinecone_index_name,
                dimension=int(pine_cone_settings.PINECONE_DIMENSIONAL_VALUE),
                metric="cosine",
                spec=self.__server_less_spec(cloud="aws", region="us-east-1"),
            )
        return pine_cone.Index(pinecone_index_name)

    def __create_pinecone_vector_store(self) -> PineconeVectorStore:
        return self.__pine_cone_vector_settings(
            index=self.__create_pinecone_index(), embedding=get_embedded_model()
        )

    def create_vector_store(self) -> PineconeVectorStore:
        """Create and return the configured Pinecone vector store."""
        return self.__create_pinecone_vector_store()
