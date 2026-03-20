import requests
import config
import json


class Spider:
    def __init__(self,):
        self.api_key = config.SCRAP_API_KEY
        self.selected_key = {
            "provider": 'None',
            "api_key": 'None',
            "usage": 0,
            "limit": 0,
            "use_rate": 100
        }
        
        api_usages = self.api_usage()
        
        print('='*50 + "\nAPI Usage Summary:\n" + '='*50)
        for item in api_usages:
            print(f"Provider: {item['provider']}, API Key: {item['api_key']}, Usage: {item['usage']}/{item['limit']} ({item['use_rate']:.2f}%)")
        print('='*50)
        self.check_api_key()
        print('='*50)



    def api_usage(self):
        base_url = {
            "scrapingdog": "https://api.scrapingdog.com/account?api_key=",
            "serpapi": "https://serpapi.com/account?api_key="
        }

        api_usages = []
        for key, value in self.api_key.items():
            if key == 'scrapingdog':
                for a_key in value:
                    url = base_url[key] + a_key
                    response = requests.get(url)
                    if response.status_code == 200:
                        data = response.json()
                        api_usages.append({
                            "provider": key,
                            "api_key": a_key,
                            "usage": int(data['requestUsed']),
                            "limit": int(data['requestLimit']),
                            "use_rate": int(data['requestUsed']) / int(data['requestLimit']) * 100
                        })
            elif key == 'serpapi':
                for a_key in value:
                    url = base_url[key] + a_key
                    response = requests.get(url)
                    if response.status_code == 200:
                        data = response.json()
                        api_usages.append({
                            "provider": key,
                            "api_key": a_key,
                            "usage": int(data['this_month_usage']),
                            "limit": int(data['searches_per_month']),
                            "use_rate": int(data['this_month_usage']) / int(data['searches_per_month']) * 100
                        })

        return api_usages
    

    def check_api_key(self,):
        api_usages = self.api_usage()

        curkey = self.selected_key['api_key']

        # select the key with large rest
        for item in api_usages:
            if item['usage'] == item['limit']:
                print(f"API Key {item['api_key']} from provider {item['provider']} has reached its limit. Skipping.")
                continue
            if self.selected_key['provider'] == 'None' or item['use_rate'] < self.selected_key.get('use_rate', 100):
                self.selected_key = item
        
        if self.selected_key['provider'] == 'None':
            print("No valid API key available. Please check your API keys and their usage.")
        elif self.selected_key['api_key'] == curkey:
            pass
        else:
            print(f"Selected API Key: [{self.selected_key['api_key']}] from provider {self.selected_key['provider']} with usage rate {self.selected_key['use_rate']:.2f}%")
    
    
    def scrapingdog_search(self, query, results=10, country="us"):
        scholar_base_url = "https://api.scrapingdog.com/google_scholar"
        params = {
            "api_key": self.selected_key['api_key'],
            "query": query,
            "results": results,
            "country": country
        }
        response = requests.get(scholar_base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data['scholar_results']
        else:
            print(f"Scrapingdog request failed with status code: {response.status_code}")
            return []
        
    def scrapingdog_citations(self, scholar_id, results=10, country="us"):
        cite_base_url = "https://api.scrapingdog.com/google_scholar/cite"
        params = {
            "api_key": self.selected_key['api_key'],
            "query": scholar_id,
        }
        response = requests.get(cite_base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Scrapingdog request failed with status code: {response.status_code}")
            return []
        

    def serpapi_search(self, query):
        scholar_base_url = "https://serpapi.com/search?engine=google_scholar"
        params = {
            "api_key": self.selected_key['api_key'],
            "q": query,
            "hl": 'en',
        }
        response = requests.get(scholar_base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data['organic_results']
        else:
            print(f"serpapi request failed with status code: {response.status_code}")
            return []
        
    def serpapi_citations(self, scholar_id, results=10, country="us"):
        cite_base_url = "https://serpapi.com/search?engine=google_scholar_cite"
        params = {
            "api_key": self.selected_key['api_key'],
            "q": scholar_id,
        }
        response = requests.get(cite_base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"serpapi request failed with status code: {response.status_code}")
            return []
        

    def search(self, query):
        self.check_api_key()
        if self.selected_key['provider'] == 'scrapingdog':
            return self.scrapingdog_search(query)
        elif self.selected_key['provider'] == 'serpapi':
            return self.serpapi_search(query)
        else:
            print("No valid API provider selected.")
            return []
        
    def get_citations(self, scholar_id):
        self.check_api_key()
        if self.selected_key['provider'] == 'scrapingdog':
            return self.scrapingdog_citations(scholar_id)
        elif self.selected_key['provider'] == 'serpapi':
            return self.serpapi_citations(scholar_id)
        else:
            print("No valid API provider selected.")
            return []