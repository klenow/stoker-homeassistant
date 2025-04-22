import aiohttp
import asyncio
import logging

from .const import API_URL, TRANSLATION_URL
#from const import API_URL, TRANSLATION_URL

_LOGGER = logging.getLogger(__name__)

class StokerCloudAPI:
    def __init__(self, session):
        self.session = session
        self.data = {}
        self.translations = {}

    async def fetch_data(self):
        try:
            async with self.session.get(API_URL) as response:
                if response.status == 200:
                    self.data = await response.json()
                else:
                    _LOGGER.error(f"Error fetching data: {response.status}")
        except Exception as e:
            _LOGGER.error(f"Exception fetching data: {e}")

    async def fetch_translations(self):
        try:
            async with self.session.get(TRANSLATION_URL) as response:
                if response.status == 200:
                    self.translations = await response.json()
                else:
                    _LOGGER.error(f"Error fetching translations: {response.status}")
        except Exception as e:
            _LOGGER.error(f"Exception fetching translations: {e}")

    def get_sensor_data(self):
        sensors = []
        for category in ["weatherdata", "boilerdata", "hopperdata", "dhwdata", "frontdata"]:
            items = self.data.get(category, [])
            for item in items:
                sensor_id = item.get("id")
                value = item.get("value")
                unit = item.get("unit")
                name_key = item.get("name")
                name = self.translations.get(name_key, name_key)
                sensors.append({
                    "id": f"{category}_{sensor_id}",
                    "name": name,
                    "value": value,
                    "unit": unit
                })
        return sensors
