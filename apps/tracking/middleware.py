from django.http import HttpResponseForbidden, HttpResponse
from django.template import Context, loader
from tracking.models import Banned

class BannedMiddleware(object):
	def process_request(self, request):
		try:
			ips = [b.ip_addr for b in Banned.objects.all()]
			users = [b.user for b in Banned.objects.all()]
			user = request.user
			ip = request.META.get('REMOTE_ADDR')
		
			output = """
				<h3> Forbidden </h3>
				<p> It looks like your IP or User has been banned from tehorng.
				If you'd like to contact us you can reach us at <a href="mailto:staff@tehorng.com?subject=Banned">staff@tehorng.com</a>
				</p>
			"""

			if ip in ips or user in users:
				return HttpResponseForbidden(output)
		except:
			ips = []
