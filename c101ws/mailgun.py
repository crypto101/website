"""
Mailgun API calls.
"""
from json import dumps
from os import getenv
from treq import get, post, json_content
from twisted.python import log
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET

PRIVATE_AUTH = "api", getenv("MAILGUN_PRIVATE_API_KEY")
PUBLIC_AUTH = "api", getenv("MAILGUN_PUBLIC_API_KEY")


def subscribe(mailingList, address):
    """Subscribes ``address`` to ``mailingList``.

    """
    url = "https://api.mailgun.net/v2/lists/{}/members".format(mailingList)
    d = post(url, auth=PRIVATE_AUTH, data={
        'subscribed': True,
        'address': address
    })
    return d.addCallback(json_content)



def validate(address):
    """Validates ``address``.

    """
    url = "https://api.mailgun.net/v2/address/validate"
    d = get(url, auth=PUBLIC_AUTH, params={"address": address})
    return d.addCallback(json_content)



class SubscribeResource(Resource):
    def render_POST(self, request):
        """Attempt to subscribe.

        """
        address, = request.args["address"]
        force, = request.args["force"]

        if force:
            self._subscribe(address, request)
        else:
            validate(address).addCallback(self._validated, request)

        return NOT_DONE_YET


    def _validated(self, validation, request):
        """Check validation result and maybe subscribe.

        """
        if not validation["valid"]:
            log.msg("e-mail invalid: {}".format(validation))
            self._respondJSON(request, {
                "success": False,
                "reason": "invalid",
                "suggestion": validation["did_you_mean"]
            })
        else:
            log.msg("e-mail looks valid, subscribing {}".format(validation))
            self._subscribe(validation["address"])


    def _subscribe(self, address, request):
        """Actually (try to) subscribe the address to the mailing list.

        """
        return subscribe(address).addCallback(self._subscribed, request)


    def _subscribed(self, subscribeResponse, request):
        """Reports Mailgun API answer to user.

        """
        log.msg("subscription response: {}".format(subscribeResponse))

        msg = subscribeResponse["message"]
        if msg == "Mailing list member has been created":
            response = {"success": True}
        elif msg.startswith("Address already exists"):
            response = {"success": False, "reason": "duplicate"}
        else:
            response = {"success": False, "reason": "unknown"}

        self._respondJSON(request, response)


    def _respondJSON(self, request, content):
        """Writes content, dumped as JSON, to request and finishes the request.

        """
        request.write(dumps(content))
        request.finish()
