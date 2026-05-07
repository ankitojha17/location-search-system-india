import wikipedia

class WikipediaAPI:
    INDIAN_STATES = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", 
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", 
        "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", 
        "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", 
        "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
        "Delhi", "Jammu and Kashmir", "Ladakh"
    ]

    @staticmethod
    def fetch_city_data(query):
        search_terms = [f"{query} India", query, f"{query} city"]
        
        for term in search_terms:
            try:
                search_results = wikipedia.search(term)
                if not search_results: continue
                
                target_page = search_results[0]
                summary = wikipedia.summary(target_page, sentences=2, auto_suggest=False)
                
                detected_state = "India"
                for state in WikipediaAPI.INDIAN_STATES:
                    if state.lower() in summary.lower():
                        detected_state = f"{state}, India"
                        break
                
                return {"name": target_page, "state": detected_state,"description": summary}
            except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError):
                continue
            except Exception:
                return None
        return None