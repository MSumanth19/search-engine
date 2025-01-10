import requests
from flask import Flask, render_template, request, redirect, url_for
from pydantic import BaseModel, Field
from typing import List, Optional

app = Flask(__name__)

# Movie API Call
def query_movie(movie_name):
    url = "https://movie-database-imdb.p.rapidapi.com/movie/"
    querystring = {"name": movie_name}
    
    headers = {
        "X-RapidAPI-Key": "e3a26d3d91msh1df956f0cff2a43p1c4efbjsn35d8a93e0c81",
        "X-RapidAPI-Host": "movie-database-imdb.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            movie_data = response.json()
            return {
                "title": movie_data.get('name', 'N/A'),
                "release_date": movie_data.get('datePublished', 'N/A'),
                "rating": movie_data.get('aggregateRating', {}).get('ratingValue', 'N/A'),
                "genre": ', '.join(movie_data.get('genre', ['N/A'])),
                "actors": [actor.get('name', 'N/A') for actor in movie_data.get('actor', [])],
                "directors": [director.get('name', 'N/A') for director in movie_data.get('director', [])],
                "description": movie_data.get('description', 'N/A'),
            }
        else:
            return {"error": "Failed to fetch movie information."}
    except Exception as e:
        return {"error": str(e)}


# Function to handle normal product search (remains the same)
def display_product_info(data):
    if 'error' in data:
        return data['error']
    
    message = f"<h2>Search Term: \"{data.get('search_term')}\"</h2>"
    
    knowledge_panel = data.get('knowledge_panel', {})
    if knowledge_panel:
        message += "<h3>Knowledge Panel:</h3>"
        message += f"<p><strong>Name:</strong> {knowledge_panel.get('name', '')}</p>"
        message += f"<p><strong>Label:</strong> {knowledge_panel.get('label', '')}</p>"
        description = knowledge_panel.get('description', {})
        if description:
            message += f"<p><strong>Description:</strong> {description.get('text', '')}</p>"
            message += f"<p><strong>URL:</strong> {description.get('url', '')}</p>"
            message += f"<p><strong>Site:</strong> {description.get('site', '')}</p>"
        image = knowledge_panel.get('image', {})
        if image:
            message += f"<p><strong>Image URL:</strong> <img src=\"{image.get('url', '')}\" width=\"{image.get('width', '100')}\" height=\"{image.get('height', '100')}\"></p>"
            message += f"<p><strong>Page URL:</strong> {image.get('page_url', '')}</p>"
        info = knowledge_panel.get('info', [])
        if info:
            message += "<ul><strong>Info:</strong>"
            for item in info:
                message += f"<li><strong>{item['title']}:</strong> {', '.join(item['labels'])}</li>"
            message += "</ul>"
    
    results = data.get('results', [])
    if results:
        message += "<h3>Results:</h3>"
        for idx, result in enumerate(results):
            message += f"<div><h4>{idx + 1}. <a href=\"{result.get('url', '#')}\">{result.get('title', '')}</a></h4>"
            message += f"<p>{result.get('description', '')}</p></div>"
    
    related_keywords = data.get('related_keywords', {}).get('keywords', [])
    if related_keywords:
        message += "<h3>Related Keywords:</h3><ul>"
        for keyword in related_keywords:
            knowledge = keyword.get('knowledge', {})
            if knowledge:
                message += f"<li><strong>Keyword:</strong> <a href=\"/search?query={keyword.get('keyword')}\">{keyword.get('keyword')}</a>"
                message += f" - <strong>Title:</strong> {knowledge.get('title', '')}"
                message += f" - <strong>Label:</strong> {knowledge.get('label', '')}"
                message += f" - <strong>Image:</strong> {knowledge.get('image', '')}</li>"
            else:
                message += f"<li><strong>Keyword:</strong> <a href=\"/search?query={keyword.get('keyword')}\">{keyword.get('keyword')}</a></li>"
        message += "</ul>"
    
    return message
    # Your existing display_product_info logic
    pass

# New function to display movie info in chat-like format
def display_movie_info(movie_data):
    # If there's an error, display it
    if "error" in movie_data:
        return f"<p>Error: {movie_data['error']}</p>"

    # Formatting the movie details
    message = f"<h3>Movie Name: {movie_data.get('name', 'N/A')}</h3>"
    message += f"<p><strong>Release Date:</strong> {movie_data.get('datePublished', 'N/A')}</p>"
    rating = movie_data.get('rating', {})
    message += f"<p><strong>Rating:</strong> {rating.get('ratingValue', 'N/A')}</p>"
    message += f"<p><strong>Genre:</strong> {', '.join(movie_data.get('genre', ['N/A']))}</p>"

    # Actors section
    actors = movie_data.get('actor', [])
    if actors:
        message += "<p><strong>Actors:</strong></p><ul>"
        for actor in actors:
            message += f"<li>{actor.get('name', 'N/A')}</li>"
        message += "</ul>"

    # Directors section
    directors = movie_data.get('director', [])
    if directors:
        message += "<p><strong>Director:</strong></p><ul>"
        for director in directors:
            message += f"<li>{director.get('name', 'N/A')}</li>"
        message += "</ul>"

    # Description and image
    message += f"<p><strong>Description:</strong> {movie_data.get('description', 'N/A')}</p>"
    
    image_url = movie_data.get('image', {}).get('url')
    if image_url:
        message += f"<p><img src='{image_url}' width='200'></p>"

    return message



# books dat

class Book(BaseModel):
    ISBN: str
    author: str
    description: str
    img_link: str
    pdf_link: str
    publisher: str
    title: str
    year: str

class BookSearchResponse(BaseModel):
    results: List[Book]

# Now you can use these models to parse the API response
def parse_book_search_response(response):
    return BookSearchResponse.parse_obj(response)

# Use the models to fetch and parse the API response
def fetch_books_info(query):
    url = "https://getbooksinfo.p.rapidapi.com/"
    headers = {
        "X-RapidAPI-Key": "e3a26d3d91msh1df956f0cff2a43p1c4efbjsn35d8a93e0c81",
        "X-RapidAPI-Host": "getbooksinfo.p.rapidapi.com"
    }
    querystring = {"s": query}

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return parse_book_search_response(response.json())
    else:
        return None

#books model


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('query')

    # Detect if the search query is movie-related
    if 'movie' in search_query.lower():
        # If it's movie-related, ask the user whether to perform normal search or movie recommendation
        return render_template('movie_choice.html', search_query=search_query)
    if 'book' in search_query.lower():
        # If it's movie-related, ask the user whether to perform normal search or movie recommendation
        return render_template('books.html', search_query=search_query)
    
    # If the search query is not movie-related, perform a normal search immediately
    url = "https://google-search74.p.rapidapi.com/"
    querystring = {"query": search_query, "limit": "10", "related_keywords": "true"}
    headers = {
        "x-rapidapi-key": "e3a26d3d91msh1df956f0cff2a43p1c4efbjsn35d8a93e0c81",
        "x-rapidapi-host": "google-search74.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()

            # Extract and display search results (customize this part for your UI)
            product_info = display_product_info(data)

            # Render the results page with search results
            return render_template('result.html', product_info=product_info)

        else:
            return "Failed to fetch search results.", 500
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while processing your search.", 500

@app.route('/abhi', methods=['GET'])
def abhi():
    search_query = request.args.get('query')
    
    # If the search query is not movie-related, perform a normal search immediately
    url = "https://google-search74.p.rapidapi.com/"
    querystring = {"query": search_query, "limit": "10", "related_keywords": "true"}
    headers = {
        "x-rapidapi-key": "e3a26d3d91msh1df956f0cff2a43p1c4efbjsn35d8a93e0c81",
        "x-rapidapi-host": "google-search74.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()

            # Extract and display search results (customize this part for your UI)
            product_info = display_product_info(data)

            # Render the results page with search results
            return render_template('result.html', product_info=product_info)

        else:
            return "Failed to fetch search results.", 500
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while processing your search.", 500







@app.route('/movie_chat', methods=['GET', 'POST'])
def movie_chat():
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        movie_data = query_movie(movie_name)  # Call the API here
        return render_template('movie_chat.html', movie_data=movie_data)
    return render_template('movie_chat.html')


#books rotuer

@app.route('/ram', methods=['GET', 'POST'])
def edu():
    if request.method == 'POST':
        book_query = request.form['book_query']
        book_search_response = fetch_books_info(book_query)
        if book_search_response and book_search_response.results:
            return render_template('edu_results.html', results=book_search_response.results)
        else:
            return render_template('error.html')
    return render_template('edu.html')

# books router



if __name__ == '__main__':
    app.run(debug=True)
