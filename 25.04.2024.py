import aiohttp
import asyncio
import json
from datetime import datetime, timedelta

class NBPApiClient:
    BASE_URL = "http://api.nbp.pl/api/exchangerates/rates/A/EUR,USD"

    async def fetch_exchange_rates(self, days):
        exchange_rates = {}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.BASE_URL) as response:
                    data = await response.json()
                    rates_data = data['rates']
                    for rate_data in rates_data:
                        date = datetime.strptime(rate_data['effectiveDate'], "%Y-%m-%d")
                        exchange_rates[date.strftime("%Y-%m-%d")] = {
                            'EUR': {
                                'sale': rate_data['mid'],
                                'purchase': rate_data['mid']
                            },
                            'USD': {
                                'sale': rate_data['mid'],
                                'purchase': rate_data['mid']
                            }
                        }
            except Exception as e:
                print(f"Error fetching data: {e}")
        return exchange_rates

async def main():
    days = 10  
    api_client = NBPApiClient()
    exchange_rates = await api_client.fetch_exchange_rates(days)
    print(json.dumps(exchange_rates, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
