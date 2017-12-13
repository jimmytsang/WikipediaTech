import pywikibot
import json, urllib
from language_dict import language_dict

# def generate_language_dict():
#     with open("list_of_wiki_languages.txt", "r") as file:
#         lines = file.read().split(",")
#         for i in range(len(lines)):
#             lines[i] = lines[i].strip()
#             lines[i] = lines[i].strip("\'")
#         dictionary = {lines[i+1]:lines[i] for i in range(0, len(lines), 2)}
#     return dictionary


### primary function
def count_backlinks(article_name, language_code):
    site = pywikibot.getSite(language_code)
    backlinks = getlinks(site, article_name)
    print(article_name)
    linked_to_count = 0
    for backlink in backlinks:
        linked_to_count += 1
    print(str(linked_to_count) + " articles link to " + article_name + "\n")

    return linked_to_count

### returns num number of links that link to the original article (in this case the original article is set to the first
### article that appears in the generated set of articles)
def getlinks(site, pageName):
    page = pywikibot.Page(site, pageName)
    return site.pagebacklinks(page, followRedirects=False, filterRedirects=True)


if __name__ == "__main__":

    count_backlinks("Pear", language_dict["English"])
