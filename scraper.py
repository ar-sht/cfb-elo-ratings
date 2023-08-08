from bs4 import BeautifulSoup
import urllib.request
import re

SOURCE = "http://www.jhowell.net/cf/scores/byname.htm"

fp = urllib.request.urlopen(SOURCE)  # this part took me way too long to figure out
html = fp.read()

soup = BeautifulSoup(html, "html.parser")
team_list = soup.body.find_all("p")[3]  # hard-coding ftw

anchors = team_list.find_all("a")  # They're all links ¯\_(ツ)_/¯

links = [anchor["href"] for anchor in anchors]  # This is the easy bit

pattern = r"^(.*?)\s*(\([A-Za-z]+\))?\s*\("  # ahhh fucking regexes. thank god for chatgpt's help:
#  First group matches anything for the team name at the beginning
#  Lets the spaces go
#  Second group matches any only-alphabet parentheses
#  Then ends at the first next open paren
#  So first group plus second gets me what I want
teams = [
    "Air Force"
]  # fuck you, i'm not trying to think bout this <br> removing shit rn
for anchor in anchors[1:]:  # looping through them tags
    text = anchor.string  # get the text out (breaks for Air Force, see comment above)
    if not text:  # in case something goes bad...
        print("AAAAAAAAHHHHHHH!")
        exit(1)

    match = re.match(pattern, text)  # yay regexes!
    if match:  # good to double-check
        team_name = match.group(1)  # get the first out-of-parentheses bit
        additional_info = match.group(2)  # get the second in-parentheses bit
        if additional_info:
            # if it exists, we'll pop it on there w/ the space put back in
            team_name += " " + additional_info
    teams.append(team_name.strip())  # stick it in the list


def serialize_record(team, page):
    pass


pages = dict(zip(teams, links))  # ok, sometimes i do like python...
for team, page in pages.values():
    serialize_record(page)
