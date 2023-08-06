from typing import Dict

from montecarlodata.common.data import OnboardingConfiguration
from montecarlodata.config import Config
from montecarlodata.errors import manage_errors, complain_and_abort
from montecarlodata.integrations.onboarding.base import BaseOnboardingService
from montecarlodata.integrations.onboarding.fields import EXPECTED_DBT_CLOUD_RESPONSE_FIELD, \
    EXPECTED_ADD_CONNECTION_RESPONSE_FIELD, DBT_CLOUD_CONNECTION_TYPE
from montecarlodata.queries.onboarding import TEST_DBT_CLOUD_CRED_MUTATION, ADD_CONNECTION_MUTATION


class DbtCloudOnboardingService(BaseOnboardingService):
    def __init__(self, config: Config, **kwargs):
        super().__init__(config, **kwargs)

    @manage_errors
    def onboard_dbt_cloud(self, **kwargs) -> None:
        self.onboard(validation_query=TEST_DBT_CLOUD_CRED_MUTATION,
                     validation_response=EXPECTED_DBT_CLOUD_RESPONSE_FIELD,
                     connection_query=ADD_CONNECTION_MUTATION,
                     connection_response=EXPECTED_ADD_CONNECTION_RESPONSE_FIELD,
                     connection_type=DBT_CLOUD_CONNECTION_TYPE, **kwargs)
