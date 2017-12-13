import pywikibot
import requests
import json, urllib
import re
import sys
from language_dict import language_dict

base_url = "w/api.php?action=query&format=json&list=search&srlimit=500&srsearch="
#url_example = https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch=life%science%data

#Create languages dictionary from "list_of_wiki_languages.txt"
# def generate_language_dict():
#     with open("list_of_wiki_languages.txt", "r") as file:
#         lines = file.read().split(",")
#         for i in range(len(lines)):
#             #lines[i] = re.sub("\s","",lines[i])
#             lines[i] = lines[i].strip()
#             lines[i] = lines[i].strip("\'")
#         dictionary = {lines[i+1]:lines[i] for i in range(0, len(lines), 2)}
#     return dictionary

###############
#MAIN FUNCTION#
###############

#Returns a list of dictionaries of LANGUAGE articles from a search query SEARCH_ITEM
#The dictionaries contain the article's TITLE, PAGEID, WORDCOUNT, and SNIPPET
#Example:
#    Input: "Swift", "English"
#    Output:
#        [
#         {"title":"Swift", "pageid":455, "wordcount": 500, "snippet":"some description of Swift"},
#         {"title": "Taylor Swift", "pageid":280, "wordcount": 331, "snippet":"some description of Taylor Swift"},
#         {"title": "Reputation", "pageid":670, "wordcount": 899, "snippet":"some description of Repuation"}
#        ]
def query_articles(search_item, language_code):
    data = get_data(search_item, language_code)
    result = []
    for e in data["query"]["search"]:
        #remove unwanted dictionary keys
        e.pop("ns", None)
        e.pop("size", None)
        e.pop("timestamp", None)
        result += [e]

    if not result:
        print("Please try another search query.")
        if suggestion_exists(data):
            print("Suggestion: " + get_search_suggestion(search_item, language_code))
    return result

#Returns a list of article names (strings) from querying for SEARCH_ITEM
#Example:
#    Input: "Swift", "English"
#    Output: ["Swift", "Taylor Swift", "Reputation"]
def get_article_names_from_query(article_dictionaries):
    result = []
    for d in article_dictionaries:
        result += [d["title"]]
    for title in result:
        print(title)
    return result

# Returns the Page objects from a query
def get_articles_from_names(article_names, language_code):
    articles = {}
    site = pywikibot.getSite(language_code)
    for article_name in article_names:
        articles[article_name] = pywikibot.Page(site, article_name)
    return articles



#Returns the search replacement suggestion for the user's search
#Example:
#    Input: "asdf Einstein!"
#    Output: "asif Einstein"
#    Input: "Albert Einstein"
#     Output: None
def get_search_suggestion(search_item, language_code):
    data = get_data(search_item, language_code)
    if suggestion_exists(data):
        return data["query"]["searchinfo"]["suggestion"]
    else:
        return None


##################
#HELPER FUNCTIONS#
##################

#Returns JSON data from the Wikipedia Web API for querying
def get_data(search_item, language_code):
    with urllib.request.urlopen(build_url(search_item, language_code)) as url:
        data = json.loads(url.read().decode())
        return data

#Builds the json request URL
def build_url(search_item, language_code):
    site = pywikibot.getSite(language_code)
    wiki_language_url = language_code + ".wikipedia.org/"

    url_search_extension = re.sub("\s", "%", search_item.strip())

    result = "https://" + wiki_language_url + base_url + url_search_extension
    return result

#returns True/False depending if there is a search replacement suggestion for the user's search
def suggestion_exists(json_data):
    return "suggestion" in json_data["query"]["searchinfo"]



######################
#EXAMPLE / HOW TO USE#
######################

if __name__ == "__main__":

    # query_articles("ARTICLE NAME", "LANGUAGE")
    article_dictionaries = query_articles("tapas", language_dict["Spanish"])
    get_article_names_from_query(article_dictionaries)

    get_search_suggestion("asdf Einstein!", language_dict["English"])
