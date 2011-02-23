from django.core.management.base import LabelCommand
from updates.models import Update
from submissions.utils import update_twitter_official

class Command(LabelCommand):
	help = "Enter a message to update the site with, will appear on index page. Enter message and severity all in one for example 'this is a message --light'"
	args = "[message [--{light,medium,strong}]]"

	def handle_label(self, label, **options):
		args = label.split('--')
		message = args[0]
		severity = args[1]

		new_update = Update(
			message = message,
			severity = severity,
		)	
		new_update.save()
		update_twitter_official(message)
		print("Update saved to database.")
	
