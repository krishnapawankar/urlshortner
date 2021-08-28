from flask import Flask, render_template, request, url_for
from urlshortner import shorten_url
import re
import os

app = Flask(__name__)


# Error Handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# get shortened url
def get_shortened_url(long_url):
    shortened_url = shorten_url()
    return shortened_url


# validate long url
def validate_long_url(long_url):
    if re.search('https?://[a-z-]+.\w+.[a-z]+/.*', long_url) != None:
        print(long_url + ' is a valid url.')
        return long_url


# save long url and short url into a file.
def save_urls(long_url, shortened_url):
    with open("urls_file.txt", "a") as f:
        f.write(long_url + " | " + shortened_url + "\n")


# save long url and short url in memory.
def save_urls_to_memory(long_url, shortened_url):
    urls_dict = {}
    urls_dict[long_url] = shortened_url
    return urls_dict


def get_urls_dict():
    with open("urls_file.txt") as f:
        urls_dict = {}
        for line in f:
            l, s = line.split("|")
            urls_dict[l.strip()] = s.strip()
    return urls_dict


# check existing url
def is_url_already_exists(long_url):
    urls_dict = get_urls_dict()
    return True if long_url in urls_dict else False


# return existing short url
def get_existing_short_url(long_url):
    urls_dict = get_urls_dict()
    if long_url in urls_dict:
        return urls_dict.get(long_url)


def create_urls_file():
    with open("urls_file.txt", "w"):
        pass


# route for home page
@app.route('/', defaults={'url': 'MY URL SHORTNER'})
def home_page(url):
    return render_template('index.html', shortened_url=url)


# route for shorten url
@app.route('/shorten', methods=['POST', 'GET'])
def shorten():
    long_url = request.form.get('long_url')

    if validate_long_url(long_url):
        if not is_url_already_exists(long_url):
            shortened_url = get_shortened_url(long_url)
            save_urls(long_url, shortened_url)
            save_urls_to_memory(long_url, shortened_url)
            message = 'GREAT!! YOUR SHORTENED URL: ' + url_for("home_page") + shortened_url
            return render_template('index.html', shortened_url=message)
        else:
            shortened_url = get_existing_short_url(long_url)
            message = 'GREAT!! YOUR EXISTING SHORTENED URL: ' + shortened_url
            return render_template('index.html', shortened_url=message)
    else:
        message = 'WRONG URL: PLEASE INPUT VALID URL.'
        return render_template('index.html', shortened_url=message)


# main function
if __name__ == "__main__":
    if not os.path.isfile('./urls_file.txt'):
        create_urls_file()
    app.run(debug=True)
