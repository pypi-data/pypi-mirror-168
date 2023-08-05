import requests

class LotrSdk():
    base_url = "https://the-one-api.dev/v2"

    def __init__(self, api_key:str):
        self.api_key = api_key  


    def check__response_status(self, status:int):
        if(status==200):
            return True
        return False


    def get_all_books(self):
        try:
            url = f"{self.base_url}/book"
            response = requests.request("GET", url)
            status = response.status_code
            if (self.check__response_status(status)):
                return response.json()
        except Exception as e:
            return e


    def get_a_book(self, id:str):
        try:
            url = f"{self.base_url}/book/{id}"
            response = requests.request("GET", url)
            status = response.status_code
            if (self.check__response_status(status)):
                return response.json()
        except Exception as e:
            return e

    
    def get_chapters_from_book(self, id:str):
        try:
            url = f"{self.base_url}/book/{id}/chapter"
            response = requests.request("GET", url)
            status = response.status_code
            if (self.check__response_status(status)):
                return response.json()
        except Exception as e:
            return e

    
    def get_all_movies(self):
        try:
            url = f"{self.base_url}/movie"
            headers = {
                "Authorization": "Bearer " + self.api_key
            }
            response = requests.request("GET", url, headers=headers)
            status = response.status_code
            if (self.check__response_status(status)):
                return response.json()
        except Exception as e:
            return e


    def get_a_movie(self, id:str):
        try:
            url = f"{self.base_url}/movie/{id}"
            headers = {
                "Authorization": "Bearer " + self.api_key
            }
            response = requests.request("GET", url, headers=headers)
            status = response.status_code
            if (self.check__response_status(status)):
                return response.json()
        except Exception as e:
            return e


    def get_a_movies_quotes(self, id:str):
        try:
            url = f"{self.base_url}/movie/{id}/quote"
            headers = {
                "Authorization": "Bearer " + self.api_key
            }
            response = requests.request("GET", url, headers=headers)
            status = response.status_code
            if (self.check__response_status(status)):
                return response.json()
        except Exception as e:
            return e


    def get_all_characters(self):
        try:
            url = f"{self.base_url}/character?limit=10"
            headers = {
                "Authorization": "Bearer " + self.api_key
            }
            response = requests.request("GET", url, headers=headers)
            status = response.status_code
            if (self.check__response_status(status)):
                return response.json()
        except Exception as e:
            return e


    def get_a_character(self, id:str):
        try:
            url = f"{self.base_url}/character/{id}"
            headers = {
                "Authorization": "Bearer " + self.api_key
            }
            response = requests.request("GET", url, headers=headers)
            status = response.status_code
            if (self.check__response_status(status)):
                return response.json()
        except Exception as e:
            return e


    def get_all_char_quotes(self, id:str):
        try:
            url = f"{self.base_url}/character/{id}/quote?limit=10"
            headers = {
                "Authorization": "Bearer " + self.api_key
            }
            response = requests.request("GET", url, headers=headers)
            status = response.status_code
            if (self.check__response_status(status)):
                return response.json()
        except Exception as e:
            return e


    def get_all_movie_quotes(self):
        try:
            url = f"{self.base_url}/quote?limit=10"
            headers = {
                "Authorization": "Bearer " + self.api_key
            }
            response = requests.request("GET", url, headers=headers)
            status = response.status_code
            if (self.check__response_status(status)):
                return response.json()
        except Exception as e:
            return e


    def get_movie_quote(self, id:str):
        try:
            url = f"{self.base_url}/quote/{id}"
            headers = {
                "Authorization": "Bearer " + self.api_key
            }
            response = requests.request("GET", url, headers=headers)
            status = response.status_code
            if (self.check__response_status(status)):
                return response.json()
        except Exception as e:
            return e


    def get_all_chapters(self):
        try:
            url = f"{self.base_url}/chapter"
            headers = {
                "Authorization": "Bearer " + self.api_key
            }
            response = requests.request("GET", url, headers=headers)
            status = response.status_code
            if (self.check__response_status(status)):
                return response.json()
        except Exception as e:
            return e


    def get_book_chapter(self, id:str):
        try:
            url = f"{self.base_url}/chapter/{id}"
            headers = {
                "Authorization": "Bearer " + self.api_key
            }
            response = requests.request("GET", url, headers=headers)
            status = response.status_code
            if (self.check__response_status(status)):
                return response.json()
        except Exception as e:
            return e
            

    