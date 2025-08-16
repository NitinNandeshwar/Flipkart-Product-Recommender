from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from flipkart.data_converter import DataConverter
from flipkart.config import Config

class DataIngestor:
    def __init__(self):
        self.embedding = HuggingFaceEndpointEmbeddings(model=Config.EMBEDDING_MODEL)

        self.vstore = AstraDBVectorStore(
            embedding=self.embedding,
            collection_name="flipkart_database",
            api_endpoint=Config.ASTRA_DB_API_ENDPOINT,
            token=Config.ASTRA_DB_APPLICATION_TOKEN,
            namespace=Config.ASTRA_DB_KEYSPACE
        )
    
    def ingest(self,load_existing:bool=True):
        if load_existing:
            print("Loading existing data from AstraDB...")
            return self.vstore
        
        print("Converting data from CSV to Documents...")
        converter = DataConverter(file_path="data/flipkart_product_review.csv")
        docs = converter.convert()
        
        print("Ingesting documents into AstraDB...")
        self.vstore.add_documents(docs)
        
        print("Data ingestion completed successfully.")
        return self.vstore
    

# if __name__ == "__main__":
#     ingestor = DataIngestor()
#     ingestor.ingest(load_existing=False)