import requests

# Function to format the product information
def display_product_info(data):
    if 'error' in data:
        return data['error']
    
    message = f"search_term: \"{data.get('search_term')}\"\n"
    
    knowledge_panel = data.get('knowledge_panel', {})
    if knowledge_panel:
        message += "knowledge_panel:\n"
        message += f"  name: \"{knowledge_panel.get('name', '')}\"\n"
        message += f"  label: \"{knowledge_panel.get('label', '')}\"\n"
        description = knowledge_panel.get('description', {})
        if description:
            message += f"  description:\n    text: \"{description.get('text', '')}\"\n"
            message += f"    url: \"{description.get('url', '')}\"\n"
            message += f"    site: \"{description.get('site', '')}\"\n"
        image = knowledge_panel.get('image', {})
        if image:
            message += f"  image:\n    url: \"{image.get('url', '')}\"\n"
            message += f"    width: {image.get('width', '')}\n"
            message += f"    height: {image.get('height', '')}\n"
            message += f"    page_url: \"{image.get('page_url', '')}\"\n"
        info = knowledge_panel.get('info', [])
        if info:
            message += f"  info:\n"
            for item in info:
                message += f"    {item['title']}: {', '.join(item['labels'])}\n"
    
    results = data.get('results', [])
    for idx, result in enumerate(results):
        message += f"{idx}:\n"
        message += f"  position: {idx + 1}\n"
        message += f"  url: \"{result.get('url')}\"\n"
        message += f"  title: \"{result.get('title')}\"\n"
        message += f"  description: \"{result.get('description')}\"\n"
    
    related_keywords = data.get('related_keywords', {}).get('keywords', [])
    if related_keywords:
        message += "related_keywords:\n"
        for keyword in related_keywords:
            knowledge = keyword.get('knowledge', {})
            if knowledge:
                message += f"  - keyword: \"{keyword.get('keyword')}\"\n"
                message += f"    title: \"{knowledge.get('title', '')}\"\n"
                message += f"    label: \"{knowledge.get('label', '')}\"\n"
                message += f"    image: \"{knowledge.get('image', '')}\"\n"
            else:
                message += f"  - keyword: \"{keyword.get('keyword')}\"\n"
    
    return message

# Get search query from user
search_query = input("Enter the search term: ")

# API endpoint and query parameters
url = "https://google-search74.p.rapidapi.com/"
querystring = {"query": search_query, "limit": "10", "related_keywords": "true"}

# Headers with API key
headers = {
    "x-rapidapi-key": "e3a26d3d91msh1df956f0cff2a43p1c4efbjsn35d8a93e0c81",
    "x-rapidapi-host": "google-search74.p.rapidapi.com"
}

# Making the API request
response = requests.get(url, headers=headers, params=querystring)
data = response.json()

# Display the product information
product_info = display_product_info(data)
print(product_info)
