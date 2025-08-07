import pandas as pd
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import os
from dotenv import load_dotenv


load_dotenv() # Load environment variables from .env file


# --- Configuration ---
CSV_FILE_PATH = 'cisse.csv' # Replace with your CSV file path
CHROMA_DB_PATH = 'chroma_db'
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def generate_and_store_embeddings(csv_file_path: str, persist_directory: str):
    """
    Generates embeddings from a CSV file and stores them in a ChromaDB vector database.
    """
    if not os.path.exists(csv_file_path):
        print(f"Error: CSV file not found at {csv_file_path}")
        return


    print(f"Loading data from {csv_file_path}...")
    df = pd.read_csv(csv_file_path)


    # Assuming your CSV has a column you want to embed, e.g., 'text_content'
    # Adjust 'text_content' to the actual column name in your CSV
    if 'text_content' not in df.columns:
        print("Error: 'text_content' column not found in CSV. Please adjust the column name or modify the script.")
        return


    documents = []
    for index, row in df.iterrows():
        # You can combine multiple columns if needed
        content = str(row['text_content']) # Ensure content is string
        metadata = row.drop('text_content').to_dict() # Store other columns as metadata
        documents.append(Document(page_content=content, metadata=metadata))


    print(f"Loaded {len(documents)} documents. Splitting into chunks...")
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        is_separator_regex=False,
    )
    splits = text_splitter.split_documents(documents)
    print(f"Split into {len(splits)} chunks.")


    print("Initializing OpenAI Embeddings...")
    #uses text-embedding-ada-002 by default
    embeddings = OpenAIEmbeddings()


    print(f"Creating and storing embeddings in ChromaDB at {persist_directory}...")
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vectorstore.persist()
    print("Embeddings generated and stored successfully!")


if __name__ == "__main__":
    # Create a dummy CSV for testing if it doesn't exist
    if not os.path.exists(CSV_FILE_PATH):
        print(f"Creating a dummy CSV file: {CSV_FILE_PATH}")
        dummy_data = {
            'text_content': [
                "The quick brown fox jumps over the lazy dog.",
                "Artificial intelligence is rapidly advancing.",
                "Machine learning is a subset of AI.",
                "Natural Language Processing deals with text and speech.",
                "Python is a popular language for AI and machine learning."
            ],
            'category': ['animal', 'tech', 'tech', 'tech', 'programming'],
            'id': [1, 2, 3, 4, 5]
        }
        dummy_df = pd.DataFrame(dummy_data)
        dummy_df.to_csv(CSV_FILE_PATH, index=False)
        print("Dummy CSV created. Please update 'your_data.csv' with your actual data.")


    generate_and_store_embeddings(CSV_FILE_PATH, CHROMA_DB_PATH)
