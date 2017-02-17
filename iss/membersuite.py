"""
Parts for the MemberSuite end of the ISS/MemberSuite sync.
"""
from django.conf import settings

from membersuite_api_client.client import ConciergeClient
from membersuite_api_client.organizations.services import OrganizationService
from membersuite_api_client.memberships.services import MembershipService


class MemberSuiteSession(object):

    def __init__(self):
        self.client = ConciergeClient(access_key=settings.MS_ACCESS_KEY,
                                      secret_key=settings.MS_SECRET_KEY,
                                      association_id=settings.MS_ASSOCIATION_ID
                                      )
        self.session_id = self.client.request_session()
        self.org_service = OrganizationService(self.client)
        self.mem_service = MembershipService(self.client)
