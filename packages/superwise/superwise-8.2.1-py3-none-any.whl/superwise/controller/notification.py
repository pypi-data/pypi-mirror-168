""" This module implement notification functionality  """
from typing import Optional

from superwise.controller.base import BaseController
from superwise.models.notification import Notification
from superwise.resources.superwise_enums import NotificationType


class NotificationController(BaseController):
	"""Class NotificationController - responsible for notification functionality"""

	def __init__(self, client, sw):
		"""

		### Args:

		`client`: superwise client object

		`sw`: superwise  object

		"""
		super().__init__(client, sw)
		self.path = "notification/v1/notifications"
		self.model_name = "Notification"

	def create_email_notification(self, name: str, email: str):
		"""

		  ### Args:

		  `name`: notification name

		  `email`: notification email

		  """
		notification_model: Notification = Notification(
			name=name, notification_metadata={"target":[email]}, type=NotificationType.Email.value
		)
		return super().create(notification_model)

	def create_slack_notification(self, name: str, webhook_url: str):
		"""
          Create Slack webhook notification
		  ### Args:

		  `name`: notification name

		  `webhook_url`: notification email

		  """
		notification_model: Notification = Notification(
			name=name, notification_metadata={"target":webhook_url}, type=NotificationType.SlackWebhook.value
		)
		return super().create(notification_model)

	def create_pagerduty_notification(self, name: str, token: str):
		"""
		  Create PagerDuty notification
		  ### Args:

		  `name`: notification name

		  `token`: PagerDuty integration IGcsTokenSet to notify on new incidents

		  """
		notification_model: Notification = Notification(
			name=name, notification_metadata={"target":token}, type=NotificationType.PagerDuty.value
		)
		return super().create(notification_model)

	def create_webhook_notification(self, name: str, webhook_url: str):
		"""
		  Create Webhook notification
		  ### Args:

		  `name`: notification name

		  `webhook_url`: webhook url

		  """
		notification_model: Notification = Notification(
			name=name, notification_metadata={"target":webhook_url}, type=NotificationType.Webhook.value
		)
		return super().create(notification_model)

	def create_datadog_notification(self, name: str, dd_api_key: str, dd_application_key: str):
		"""
		  Create Datadog notification
		  ### Args:

		  `name`: notification name

		  `dd_api_key`: API key will allow us to submit metrics and events to Datadog

		  `dd_application_key`: Application keys will allows us to submit incidents to Datadog

		  """
		notification_metadata = {"target":{"dd_api_key":dd_api_key, "dd_application_key":dd_application_key}}

		notification_model: Notification = Notification(
			name=name, notification_metadata=notification_metadata, type=NotificationType.Datadog.value
		)
		return super().create(notification_model)

	def get(self, name: Optional[str] = None):
		"""

		  ### Args:

		  `name`: notification name

		  """
		if name is not None:
			return super().get({"name":name})
		return super().get({})
