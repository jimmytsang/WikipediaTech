import pywikibot
import requests
import json, urllib
import datetime
import re
from language_dict import language_dict

url = "http://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
#url_example = "/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/Albert_Einstein/monthly/2015100100/2015123100"

#Create languages dictionary from "list_of_wiki_languages.txt"
# def generate_language_dict():
    # with open("list_of_wiki_languages.txt", "r") as file:
    #     lines = file.read().split(",")
    #     for i in range(len(lines)):
    #         #lines[i] = re.sub("\s","",lines[i])
    #         lines[i] = lines[i].strip()
    #         lines[i] = lines[i].strip("\'")
    #     dictionary = {lines[i+1]:lines[i] for i in range(0, len(lines), 2)}
    # return dictionary


###############
#MAIN FUNCTION#
###############

#Returns the total number of page views over the last 3 months for the page named "article_name"
def get_page_view(article_name, language_code):
    with urllib.request.urlopen(build_url(article_name, language_code)) as url:
        data = json.loads(url.read().decode())
        total_views = get_total_views(data)
        return total_views


##################
#HELPER FUNCTIONS#
##################

#Builds the json request URL
def build_url(article_name, language_code):
    #get the wikipedia URL extension for the article called "article_name"
    site = pywikibot.getSite(language_code)
    page = pywikibot.Page(site, article_name)
    wiki_url_extension = page.urlname()

    wiki_language_url = language_code + ".wikipedia"

    #Create the start and end date strings for the 3-month period
    start_date, end_date = create_start_end_months()

    result = url + wiki_language_url + "/all-access/all-agents/" + wiki_url_extension +"/monthly/" + start_date + "/" + end_date
    return result

#Creates the start and end date strings for the request URL
def create_start_end_months():
    day = datetime.date.today().day
    end_month = datetime.date.today().month
    end_year = datetime.date.today().year
    start_month = datetime.date.today().month - 3 #creates a 3-month period
    start_year = datetime.date.today().year
    if start_month <= 0:
        start_month += 12
        start_year -= 1
    end_string = str(end_year) + buffer_date(end_month) + buffer_date(day) + "00"
    start_string = str(start_year) + buffer_date(start_month) + buffer_date(day) + "00"
    return start_string, end_string

#Buffers 1-digit dates with a 0
def buffer_date(date):
    if date < 10:
        return "0" + str(date)
    else:
        return str(date)

#Returns the sum of views from the last 3 months
def get_total_views(data):
    total_views = 0
    for item in data['items']:
        total_views += item['views']
    return total_views


######################
#EXAMPLE / HOW TO USE#
######################

if __name__ == "__main__":
    query = "Albert Einstein"
    language = "Icelandic"
    num_views = get_page_view(query, language_dict[language])
    print(query + " has " + str(num_views) + " views in " + language)
