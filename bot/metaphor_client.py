# bot/metaphor_client.py
from metaphor_python import Metaphor
import logging

class MetaphorClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.metaphor_client = Metaphor(api_key=api_key)

    def search(self, query, num_results=1):
        try:
            return self.metaphor_client.search(query=query, num_results=num_results).results
        except Exception as e:
            logging.error(f"[GOSH! ERROR SEARCHING WITH METAPHOR] : {str(e)}")
            return []

    def get_contents(self, id):
        try:
            return self.metaphor_client.get_contents(id).contents[0].extract
        except Exception as e:
            logging.error(f"[NOOO! ERROR GETTING CONTENTS] : {str(e)}")
            return ""