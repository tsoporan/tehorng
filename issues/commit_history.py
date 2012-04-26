import feedparser
from django.template.defaultfilters import mark_safe, timesince
import datetime
import time

TEHORNG_COMMIT_URL = "https://github.com/tsoporan/tehorng/commits/master.atom"

def get_commit_history():
    parsed = feedparser.parse(TEHORNG_COMMIT_URL)
    entries = parsed['entries']
    commits = []

    for entry in entries:
        commit_updated = datetime.datetime.fromtimestamp(time.mktime(entry.updated_parsed))
        commit_link = entry.link 
        commit_hash = entry.link.split('/')[-1][:7] 
        commit_msg = entry.title 
       
        time_format = "%H:%M:%S on %b. %d %Y"

        s = mark_safe("""<a href="%s" title="%s">%s</a> %s <strong>%s</strong>""" % (commit_link, commit_msg, commit_hash, commit_msg, commit_updated.strftime(time_format) ))

        commits.append(s)

    return commits



