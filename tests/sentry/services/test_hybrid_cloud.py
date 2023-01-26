from sentry.services.hybrid_cloud.organization import ApiTeam
from sentry.testutils import TestCase


class HybridCloudServiceTest(TestCase):
    def test_pydantic(self):
        schema = ApiTeam.schema_json(indent=2)
        assert schema
