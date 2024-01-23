from llama_index.llms import OpenAI
from loguru import logger
from repo_agent.chat_with_repo.json_handler import JsonFileProcessor

logger.add("./log.txt", level="DEBUG", format="{time} - {name} - {level} - {message}")


class TextAnalysisTool:
    def __init__(self, llm, db_path):
        self.jsonsearch = JsonFileProcessor(db_path)
        self.llm = llm
        self.db_path = db_path

    def keyword(self, query):
        prompt = f"Please provide a list of keywords related to the following query, requests output no more than 3 keywords, Input: {query}, Output:"
        response = self.llm.complete(prompt)
        return response

    def tree(self, query):
        prompt = f"Please analyze the following text and generate a tree structure based on its hierarchy:\n\n{query}"
        response = self.llm.complete(prompt)
        return response

    def format_chat_prompt(self, message, instruction):
        prompt = f"System:{instruction}\nUser: {message}\nAssistant:"
        return prompt

    def queryblock(self, message):
        search_result = self.jsonsearch.search_in_json_nested(self.db_path, message)
        if isinstance(search_result, dict):
            search_result = search_result["code_content"]
        return str(search_result)

    def nerquery(self, message):
        query1 = """
        The output must strictly be a pure function name or class name, without any additional characters.
        For example:
        Pure function names: calculateSum, processData
        Pure class names: MyClass, DataProcessor
        The output function name or class name should be only one.
        """
        query = f"Extract the most relevant class or function from the following{query1}input:\n{message}\nOutput:"
        response = self.llm.complete(query)
        logger.debug(f"Input: {message}, Output: {response}")
        return response


if __name__ == "__main__":
    api_base = "https://api.openai.com/v1"
    api_key = "your_api_key"
    log_file = "your_logfile_path"
    llm = OpenAI(api_key=api_key, api_base=api_base)
    db_path = "your_database_path"
    test = TextAnalysisTool(llm, db_path)