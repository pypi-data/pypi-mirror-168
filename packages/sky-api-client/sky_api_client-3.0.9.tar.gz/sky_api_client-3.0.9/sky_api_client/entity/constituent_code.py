from sky_api_client.entity.base import Entity
from sky_api_client.entity.registry import EntityRegistry


@EntityRegistry.register('constituent_code')
class ConstituentCode(Entity):
    LIST_URL = '/constituent/v1/constituents/{id}/constituentcodes'
    GET_URL = '/constituent/v1/constituents/constituentcodes/{id}'
    TYPES_URL = '/constituent/v1/constituentcodetypes'
