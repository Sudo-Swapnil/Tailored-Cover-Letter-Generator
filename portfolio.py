import uuid
import chromadb
import pandas as pd


class Portfolio:
    def __init__(self, file_path="./resources/my_portfolio.csv") -> None:
        self.file_path: str = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.chroma_client.delete_collection(name="portfolio")
        self.collection = self.chroma_client.get_or_create_collection(name='portfolio')


    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row['Techstack'],
                            metadatas={'links': row["Links"], 'Descriptions': row['Description']},
                            ids=[str(uuid.uuid4())])
                
    def query_links(self, skills):
        print("FROM portfilio")
        links = self.collection.query(query_texts=skills, n_results=1)
        print("DONE")
        filtered_results = {
            'ids': [],
            'distances': [],
            'metadatas': [],
            'documents': []
        }

        for i, distance in enumerate(links['distances']):
            if distance[0] < 1:
                filtered_results['ids'].append(links['ids'][i])
                filtered_results['distances'].append(distance)
                filtered_results['metadatas'].append(links['metadatas'][i])
                filtered_results['documents'].append(links['documents'][i])

        # Output the filtered results
        print(links)
        print("RETURNING")
        print(filtered_results)
        return filtered_results