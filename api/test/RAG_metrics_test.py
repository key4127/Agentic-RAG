from llama_index.core import Settings as LlamaIndexSettings
from llama_index.llms.deepseek import DeepSeek
from llama_index.core.schema import QueryBundle
from api.config import Settings
from api.dependencies import get_embedding_model
from api.dependencies import get_retriever
from api.dependencies import get_flash_reranker
import json
import os

max_id_num = 0

def metric_test(request_ids, get_ids):
    right_nodes = [
        id
        for id in request_ids
        if id in get_ids
    ]

    # global max_id_num
    # max_id_num = max(max_id_num, len(request_ids))

    return len(right_nodes)

def main():
    LlamaIndexSettings.llm = DeepSeek(model="deepseek-chat", api_key=os.getenv("DEEPSEEK_API_KEY"))
    LlamaIndexSettings.embed_model = get_embedding_model()

    input_file = "./data/weaviate/weaviate.jsonl"

    total_precision = 0
    total_recall = 0
    total_F1 = 0

    retriever = get_retriever()
    reranker = get_flash_reranker()

    with open(input_file, "r", encoding="utf-8") as input:
        lines = input.readlines()

        for line in lines:
            test = json.loads(line)
            query = test["Q"]
            query_bundle = QueryBundle(query)

            raw_nodes = retriever.retrieve(query)
            get_nodes = reranker.postprocess_nodes(raw_nodes, query_bundle)

            nodes_scores = [
                node.score
                for node in get_nodes
            ]
            print(nodes_scores)

            get_nodes = [
                node.node_id
                for node in get_nodes
                if node.score is not None and node.score >= 0.8
            ]

            right_nums = len(test["ids"])
            get_nums = len(get_nodes)
            right_get_nums = metric_test(test["ids"], get_nodes)

            precision = right_get_nums / get_nums \
                        if get_nums != 0 \
                        else 1.0
            recall = right_get_nums / right_nums \
                        if right_nums != 0 \
                        else 0
            f1 = 2 * precision * recall / (precision + recall) \
                    if precision + recall != 0 \
                    else 0

            total_precision += precision
            total_recall += recall
            total_F1 += f1

        query_num = len(lines)

        print(f'Precision: {total_precision / query_num}')
        print(f'Recall:    {total_recall / query_num}')
        print(f'F1:        {total_F1 / query_num}')

    # print(f'num: {max_id_num}')

if __name__ == "__main__":
    main()