from query_article_titles import *
from page_popularity import *
from linked_pages import *
from ores_assessment import *
import sys

# MAIN FUNCTION

def main(query, language_code, filter_method, limit, stub):
    # Process script arguments
    # For now, we only support limiting by number of articles, not total package size
    limit = min(int(limit), 500)

    # Get the query results (list of dictionaries)
    article_dictionaries = query_articles(query, language_code)[:limit+20]
    # List of article titles
    article_names = get_article_names_from_query(article_dictionaries)

    if filter_method == "ores_quality" or stub == "exclude":
        ores_rating_results = get_ores_assessment(article_names, language_code)
        # Assign a numerical score based on qualitative assessment
        scaled_ores_rating_results = scale_article_assessments(ores_rating_results)
        if stub == "exclude":
            scaled_ores_rating_results = {name : score for name, score in scaled_ores_rating_results.items() if score != 0}
            article_names = [name for name in article_names if name in scaled_ores_rating_results]

    # Dictionary of page objects with article names as keys
    articles = get_articles_from_names(article_names, language_code) # {"title: page_object"}
    # Initialize empty dictionary of article ratings hashed by article name/title
    article_ratings = {} # {"title: numerical_article_score"}

    if filter_method == "ores_quality":
            article_ratings = scaled_ores_rating_results
    elif filter_method == "popularity":
        for article in articles:
            article_ratings[article] = get_page_view(article, language_code)
    elif filter_method == "most_linked_to":
        for article in articles:
            article_ratings[article] = count_backlinks(article, language_code)
    else:
        print("Invalid filter method. Please choose popularity, most_linked_to, or ores_quality")
        sys.exit(0)

    sorted_articles = sorted(articles.items(), key=lambda x: article_ratings[x[0]], reverse=True)
    return process_results(sorted_articles[:limit])

def process_results(sorted_articles):
    results = []
    for i in range(len(sorted_articles)):
        results.append(sorted_articles[i][1].full_url())
    return results

if __name__ == "__main__":
    query = input("Please enter your query: ")
    language = language_dict[input("Please enter a language: ").capitalize()]
    filter_method = input("Please enter the filtering method: ")
    limit = input("Enter a limit no more than 500: ")
    stub = "include"
    main(query, language, filter_method, limit, stub)
