def save_to_memory(result: dict, memory_database: list):
    memory_database.append(result["query"])
    memory_database.append(result["answers"][0].to_dict()["answer"])
