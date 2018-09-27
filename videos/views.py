import logging
import requests
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialApp, SocialToken, SocialAccount
from django.utils.crypto import get_random_string
from patronage.views import PatronageView
from patronage.models import Tier, UserTier, RemoteBenefit

logger = logging.getLogger(__file__)


class VimeoPatronageView(PatronageView):
    remote_app = "vimeo_oauth2"
    remote_app_name = "Vimeo"

    def grant_remote_benefits(self, tier):
        # Get creator vimeo token
        remoteusers = SocialToken.objects.filter(
            account__user__in=tier.creators.all(), app__provider=self.remote_app
        )
        if remoteusers:
            token = remoteusers[0].token
            # Get patron vimeo user ids
            patrons = SocialAccount.objects.filter(
                user__usertier__in=UserTier.objects.filter(tier=tier),
                provider=self.remote_app,
            )
            # Get tier benefits
            benefits = tier.benefits.all()
            # Call out updates to vimeo
            for benefit in benefits:
                for patron in patrons:

                    response = requests.put(
                        f'https://api.vimeo.com/channels/{benefit.remote_id}/privacy/users/{patron.uid}',
                        headers={"Authorization": "Bearer {}".format(token)},
                    )

    def get_remote_benefits(self):
        remote_benefits = []
        try:
            vimeouser = SocialToken.objects.get(
                account__user=self.request.user, app__provider="vimeo_oauth2"
            )
        except SocialToken.DoesNotExist:
            vimeouser = None
        if vimeouser:
            response = requests.get(
                "https://api.vimeo.com/me/channels?filter=moderated",
                headers={"Authorization": "Bearer {}".format(vimeouser.token)},
            )
            if response.status_code == 200:
                for channel in response.json().get("data", [{}]):
                    benefit, _ = RemoteBenefit.objects.get_or_create(
                        remote_id=channel.get("uri").split("/")[-1],
                        title=channel.get("name"),
                        url=channel.get("link"),
                    )
                    remote_benefits.append(benefit)
        return remote_benefits
