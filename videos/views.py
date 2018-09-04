import logging
import requests
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialToken
from django.utils.crypto import get_random_string
from patronage.views import PatronageView

logger = logging.getLogger(__file__)


class VimeoPatronageView(PatronageView):
    remote_app = 'vimeo'

    def create_remote_benefit(self):
        code = get_random_string(length=8)
        ebuser = SocialToken.objects.get(
            account__user=self.request.user, app__provider="vimeo"
        )
        # r = requests.get(
        #     "https://www.eventbriteapi.com/v3/users/me/organizations/",
        #     headers={"Authorization": "Bearer {}".format(ebuser.token)},
        # )
        # organization_id = r.json().get("organizations", [{}])[0].get("id")
        # r = requests.post(
        #     "https://www.eventbriteapi.com/v3/organizations/{}/discounts/".format(
        #         organization_id
        #     ),
        #     data={
        #         "discount.code": code,
        #         "discount.type": "coded",
        #         "discount.percent_off": "100",
        #     },
        #     headers={"Authorization": "Bearer {}".format(ebuser.token)},
        # )
        # return r.json()["id"], code
