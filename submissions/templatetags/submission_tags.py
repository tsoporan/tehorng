from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@stringfilter #expects string
def clean_url(value):
	sites = [
		'sendspace',
		'rapidshare',
		'mediafire',
		'megaupload',
		'sharebee',
		'zshare',
		'hotfile',
		'badongo',
		'4shared',
		'multiupload',
		'easy-share',
		'rghost',
		'bandcamp',
		'depositfiles',
		'filefactory', 
		'filestube',
	]
	try:
		split = value.split('/')
		url = split[2].lower()
		for s in sites:
			if s in url: return s
		return url
	except Exception, e:
		return value
register.filter('clean_url', clean_url)


def truncate_chars(value, max_length):
    if len(value) <= max_length:
        return value
    trunc_val = value[:max_length]
    if value[max_length] != " ":
        rightmost_space = trunc_val.rfind(" ")
        if rightmost_space != -1:
            trunc_val = trunc_val[:rightmost_space]
    return trunc_val + "..."
register.filter('truncate_chars', truncate_chars)
