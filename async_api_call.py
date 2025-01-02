import aiohttp
import asyncio

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Example Usage
async def main():
    data = await fetch_data("https://api.example.com/resource")
    print(data)

asyncio.run(main())
