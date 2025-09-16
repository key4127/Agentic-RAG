import json

def generate_weaviate_data(input_path: str, output_path: str):
    with open(input_path, "r", encoding="utf-8") as input, \
         open(output_path, "w", encoding="utf-8") as output:
        while True:
            line_q = input.readline()
            line_nodes = input.readline()

            if not line_q or not line_nodes:
                break

            ids = line_nodes[:-1].split(',')
            content = {
                "Q": line_q[slice(2, None, None)],
                "ids": ids
            }

            json_line = json.dumps(content, ensure_ascii=False)
            output.write(json_line + '\n')

if __name__ == "__main__":
    input_path = "./data/40_q&a.txt"
    output_path = "./data/weaviate/weaviate.jsonl"
    
    generate_weaviate_data(input_path, output_path)