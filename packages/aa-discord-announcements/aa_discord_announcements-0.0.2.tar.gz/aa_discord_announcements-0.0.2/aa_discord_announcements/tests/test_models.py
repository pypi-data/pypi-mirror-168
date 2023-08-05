"""
Test models
"""

# Django
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.test import TestCase, modify_settings

# AA Discord Announcements
from aa_discord_announcements.models import PingTarget, Webhook


class TestModels(TestCase):
    """
    Test our models
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up groups and users
        """

        super().setUpClass()

        cls.group = Group.objects.create(name="Superhero")

    def test_discord_webhook_invalid_webhook_url_should_throw_exception(self):
        """
        Test if we get a ValidationError for a Discord webhook
        :return:
        """

        # given
        webhook = Webhook(
            url=(
                "https://discord.com/api/webhooks/754119343402302920F/x-BfFCdEG"
                "-qGg_39_mFUqRSLoz2dm6Oa8vxNdaAxZdgKOAyesVpy-Bzf8wDU_vHdFpm-"
            ),
        )

        # when
        with self.assertRaises(ValidationError):
            webhook.clean()

        with self.assertRaisesMessage(
            ValidationError,
            expected_message=(
                "Invalid webhook URL. The webhook URL you entered does not match any "
                "known format for a Discord webhook. Please check the "
                "webhook URL."
            ),
        ):
            webhook.clean()

    @modify_settings(INSTALLED_APPS={"remove": "allianceauth.services.modules.discord"})
    def test_should_raise_validation_error_for_not_activated_discord_service(self):
        """
        Test should raise a validation error when Discord service is not active
        :return:
        """

        # given
        announcement_target = PingTarget(name=self.group, discord_id=123456789)

        # when
        with self.assertRaises(ValidationError):
            announcement_target.clean()

        with self.assertRaisesMessage(
            ValidationError,
            expected_message=(
                "You might want to install the Discord service first ..."
            ),
        ):
            announcement_target.clean()

    def test_should_raise_validation_error_on_save(self):
        """
        Test should raise validation error on save
        :return:
        :rtype:
        """

        ping_target = PingTarget(name=self.group)

        with self.assertRaises(ValidationError):
            ping_target.save()

    def test_should_return_ping_target_model_string_name(self):
        """
        Test should return the PingTarget model string name
        :return:
        :rtype:
        """

        ping_target = PingTarget(name=self.group)

        self.assertEqual(str(ping_target), self.group.name)

    def test_should_return_webhook_model_string_name(self):
        """
        Test should return the Webhook model string name
        :return:
        :rtype:
        """

        webhook = Webhook(
            name="Test Webhook",
            url=(
                "https://discord.com/api/webhooks/754119343402302920F/x-BfFCdEG"
                "-qGg_39_mFUqRSLoz2dm6Oa8vxNdaAxZdgKOAyesVpy-Bzf8wDU_vHdFpm-"
            ),
        )

        webhook.save()

        self.assertEqual(str(webhook), "Test Webhook")
