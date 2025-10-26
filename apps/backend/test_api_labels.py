#!/usr/bin/env python3
"""Test Wikidata API label fetching."""

import asyncio
import aiohttp
import json

async def test_api():
    ids = ["Q90", "Q142", "Q46"]
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbgetentities",
        "ids": "|".join(ids),
        "props": "labels",
        "languages": "en",
        "format": "json"
    }
    
    print(f"Testing Wikidata API with IDs: {ids}")
    print(f"URL: {url}")
    print(f"Params: {params}\n")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                print(f"Status: {response.status}")
                if response.status == 200:
                    data = await response.json()
                    print(f"\nResponse:\n{json.dumps(data, indent=2)}")
                    
                    entities = data.get("entities", {})
                    labels = {}
                    for entity_id, entity_data in entities.items():
                        if "labels" in entity_data and "en" in entity_data["labels"]:
                            labels[entity_id] = entity_data["labels"]["en"]["value"]
                    
                    print(f"\nExtracted labels: {labels}")
                else:
                    print(f"Error: {await response.text()}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_api())
