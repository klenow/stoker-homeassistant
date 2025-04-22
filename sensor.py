from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from datetime import timedelta
import logging

from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL
from .stokercloud_api import StokerCloudAPI

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    session = async_get_clientsession(hass)
    api = StokerCloudAPI(session)
    await api.fetch_translations()

    async def async_update_data():
        await api.fetch_data()
        return api.get_sensor_data()

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(seconds=DEFAULT_UPDATE_INTERVAL),
    )

    await coordinator.async_config_entry_first_refresh()

    sensors = []
    for sensor_data in coordinator.data:
        sensors.append(StokerCloudSensor(coordinator, sensor_data))

    async_add_entities(sensors, True)

class StokerCloudSensor(Entity):
    def __init__(self, coordinator, sensor_data):
        self.coordinator = coordinator
        self._id = sensor_data["id"]
        self._name = sensor_data["name"]
        self._unit = sensor_data["unit"]
        self._state = sensor_data["value"]

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return self._id

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return self._unit

    async def async_update(self):
        await self.coordinator.async_request_refresh()
