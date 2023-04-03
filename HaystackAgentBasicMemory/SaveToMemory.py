def SaveToMemory(result: dict, memory_database: list, **kwargs):
    memory_database.append(result["query"])
    memory_database.append(result["answers"][0].to_dict()["answer"])
