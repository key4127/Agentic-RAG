import weaviate
import csv

def convert_to_csv(collection, output_path):
    total_count = collection.aggregate.over_all(total_count=True).total_count
    batch_size = 100

    print(f'Total count is {total_count}')

    with open(output_path, "w", newline="", encoding="utf-8") as output:
        writer = csv.writer(output)
        writer.writerow(['UUID', 'title', 'category', 'text'])

        for batch_start in range(0, total_count, batch_size):
            result = collection.query.fetch_objects(
                limit=batch_size,
                offset=batch_start,
                return_properties=["title", "category", "text"]
            )
            
            for i, obj in enumerate(result.objects, start=batch_start + 1):
                properties = obj.properties
                title = properties.get('title', '') if properties else ''
                category = properties.get('category', '') if properties else ''
                text = properties.get('text', '') if properties else ''
                
                writer.writerow([
                    obj.uuid,
                    str(title),
                    str(category),
                    str(text)
                ])

def main():
    client = weaviate.connect_to_local(
        host="localhost",
        port=8081,
        grpc_port=50051,
    )
    collection = client.collections.get("Agentic_RAG_Docs")
    
    output_path = "./data/weaviate/weaviate.csv"

    convert_to_csv(collection, output_path)

    client.close()

if __name__ == "__main__":
    main()