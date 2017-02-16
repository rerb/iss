"""
Parts for the MemberSuite end of the ISS/MemberSuite sync.
"""
import datetime
import logging

from django.conf import settings

from membersuite_api_client.client import ConciergeClient
from membersuite_api_client.organizations.services import OrganizationService


logger = logging.getLogger(__name__)


class MemberSuiteSession(object):

    def __init__(self):
        self.client = ConciergeClient(access_key=settings.MS_ACCESS_KEY,
                                      secret_key=settings.MS_SECRET_KEY,
                                      association_id=settings.MS_ASSOCIATION_ID
                                      )
        self.session_id = self.client.request_session()
        self.concierge_request_header = \
            self.client.construct_concierge_header(
                url="http://membersuite.com/contracts/"
                    "IConciergeAPIService/ExecuteMSQL"
            )


class MemberSuiteObject(object):

    session = None

    def __new__(cls, membersuite_session=None, *args, **kwargs):
        cls.session = membersuite_session or MemberSuiteSession()
        return super(object, cls).__new__(*args, **kwargs)


class AccountList(object):

    @classmethod
    def get_accounts_modified_since(cls, days_ago, session=None, get_all=False):
        """Return all Accounts modified within `days_ago` days."""
        cls.session = session or MemberSuiteSession()
        service = OrganizationService(cls.session.client)
        since_when = datetime.date.today() - datetime.timedelta(days_ago)
        qs = service.get_orgs(since_when=since_when)

        return qs
