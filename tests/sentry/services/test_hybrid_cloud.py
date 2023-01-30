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
            schema = api_type.schema_json(indent=2)
            print(f"{api_type.__name__}\n{schema}\n")  # noqa
            assert schema


# (^@dataclass\nclass (Api\w+)):
# $1(SiloDataInterface):

# (\w+) \| None
# Optional[$1]
