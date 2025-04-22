import asyncio
import aiohttp
import json
from stokercloud_api import StokerCloudAPI

async def main():

    async with aiohttp.ClientSession() as session:
        # Create API instance
        api = StokerCloudAPI(session)

        print("Fetching translation file...")
        # Fetch translations
        
        await api.fetch_translations()
        translations = api.translations

        print("Fetching data from StokerCloud...")
        # Fetch StokerCloud data
        await api.fetch_data()
        data = api.data
        if not data:
            print("Failed to fetch data from StokerCloud.")
            return

        print("\n✅ Fetched and parsed data:\n")

        # Helper to look up friendly name
        def get_name(raw_name):
            return translations.get(raw_name, raw_name)

        for category in ["weatherdata", "boilerdata", "hopperdata", "dhwdata", "frontdata"]:
            if category not in data:
                continue

            print(f"\n📦 {category.upper()}")
            for item in data[category]:
                name = get_name(item.get("name", ""))
                value = item.get("value")
                unit = item.get("unit")
                print(f" - {name}: {value} {unit}")

        # Print a few misc values
        print("\n⚙️  Misc:")
        misc = data.get("miscdata", {})
        for key, val in misc.items():
            if isinstance(val, dict):
                print(f" - {key}: {val.get('value')} {val.get('unit', '')}")
            else:
                print(f" - {key}: {val}")

if __name__ == "__main__":
    asyncio.run(main())
