import glob
import csv
import sys
import codecs
import mechanicalsoup


"""
import string
import mechanize
import cookielib
import re
import os
import sys
from time import gmtime, strftime
from random import randint
from time import sleep
from bs4 import BeautifulSoup
"""

import private


def open_cache_page(url, posted):

  clean = url.strip()

  short_url = "/account/login"
  login_url = "https://www.geocaching.com" + short_url
  
  try:
    browser = mechanicalsoup.StatefulBrowser()     # Create a browser object
  except:
    print("Unexpected error:", sys.exc_info()[0])
    raise

  try:
    print("Fetching account login page at URL: {}".format(login_url))
    response = browser.open(login_url)
    print("  Response: {}".format(response))
  except:
    print("Unexpected error:", sys.exc_info()[0])
    raise

  try:
    if not browser.select_form('form[action="{}"]'.format(short_url)):
      print("  Unable to open login form!")
      return False
  except:
    print("Unexpected error:", sys.exc_info()[0])
    raise

  browser.get_current_form()    #   .print_summary()
  browser['Username'] = private.username
  browser['Password'] = private.password
  response = browser.submit_selected()  # submit form
  print("  Login response: {}".format(response))

  # Now we should be logged in.  Attempt to fetch the cache page and check.

  try:
    print("Fetching cache page at URL: {}".format(clean))
    response = browser.open(clean)
    print("  Page fetch response: {}".format(response))
  except:
    print("Unexpected error:", sys.exc_info()[0])
    raise

  user = browser.get_current_page().find('span', class_='user-name').text    # verify we are now logged in ( get username in webpage )

  if private.username in user:
    print("  You are connected as " + private.username)
  else:
    print("Connection failed!")
    return False

  html = browser.get_current_page()
  link = html.find('a', {'id': 'ctl00_ContentBody_uxEditGeocacheLink'})
  href = link['href']

  try:
    print("Following link to cache edit page at URL: {}".format(link))
    response = browser.follow_link(link)
    print("  Page fetch response: {}".format(response))
  except:
    print("Unexpected error:", sys.exc_info()[0])
    raise

  try:
    if not browser.select_form('form[id="aspnetForm"]'):
      print("  Unable to open cache edit form!")
      return False
  except:
    print("Unexpected error:", sys.exc_info()[0])
    raise

  browser.select_form().print_summary()
  browser["ctl00$ContentBody$tbPostedCoordinates"] = posted

  try:
    print("Submitting the cache listing changes.")
    response = browser.submit_selected()
    print("  Form submit response: {}".format(response))
  except:
    print("Unexpected error:", sys.exc_info()[0])
    raise

  return True

# -----------------------------------------------------------------------------

def main():
  
  print("update-gc-art.py starting...")

  for numbers in glob.iglob('/tmp/inputs/*.csv'):
    
    if numbers.rsplit(".")[-1] != "csv":
      print("ERROR - File must have a .csv extension!  {} found.".format(numbers))
      exit(1)
      
    print("Processing CSV file {}...".format(numbers))

    with codecs.open(numbers, "rU", encoding='utf-8', errors='ignore') as csvFile:
      reader = csv.DictReader(csvFile)
      for row in reader:
        url = row['GC Code']
        if url:
          posted = row['Posted']
          page = open_cache_page(url, posted)


 
if __name__ == '__main__':
    main()
