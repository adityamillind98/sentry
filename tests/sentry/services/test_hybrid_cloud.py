from sentry.services.hybrid_cloud.organization import (
    ApiOrganizationFlags,
    ApiOrganizationMember,
    ApiOrganizationMemberFlags,
    ApiProject,
    ApiTeam,
    ApiTeamMember,
)
from sentry.testutils import TestCase


class HybridCloudServiceTest(TestCase):
    def test_pydantic(self):
        api_types = [
            ApiTeam,
            ApiTeamMember,
            ApiProject,
            ApiOrganizationMemberFlags,
            ApiOrganizationMember,
            ApiOrganizationFlags,
        ]
        for api_type in api_types:
            schema = ApiTeam.schema_json(indent=2)
            # print(f"\n{api_type.__name__}\n{schema}\n")
            assert schema


# (^@dataclass\nclass (Api\w+)):
# $1(SiloDataInterface):

# (\w+) \| None
# Optional[$1]
