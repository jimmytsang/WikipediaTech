from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS
from zimmerbot import *

application = FlaskAPI(__name__)
CORS(application)

@application.route("/", methods=["GET", "POST"])
def get_links():
    if request.method == "GET":
        list_of_links = main("dog", "en", "popularity", "10", "include")
    else:
        print(request.data)
        data = request.data
        if data["filter"] == "ores_quality" and data["language"] not in ["en", "ru", "fr"]:
            return ["ORES is not supported in this language"], status.HTTP_202_ACCEPTED
        list_of_links = main(data["query"], data["language"], data["filter"], data["limit"], data["stub"])
        if not list_of_links:
            return ["No search results found for this query"], status.HTTP_202_ACCEPTED
    return list_of_links


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    # app.debug = True
    application.run()
