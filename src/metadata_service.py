import requests
url = "https://openlibrary.org/search.json?q="

class MetadataService:
    """ 
    Service to fetch metadata for textual items.
    TODO: 1. Expand to other souces. 2. Add async 3. Caching
    """
    @staticmethod
    def _fetch_metadata(title: str ="", isbn: str=""):
        """
        Fetch metadata from an external source. OpenLibrary API is used here. Google books API
        will be used in the future. Requires either title or isbn to be provided and defaults 
        to isbn if both are provided for more precise results.
        """
        if not title and not isbn:
            raise ValueError
        if title:
            title = title.replace(" ", "+")
        query = isbn if isbn else title
        response = requests.get(url + query)
        if response.status_code != 200:
            raise ConnectionError("Failed to fetch metadata")
        data = response.json()
        if data['numFound'] == 0:
            raise ValueError("No metadata found")

        return data 
