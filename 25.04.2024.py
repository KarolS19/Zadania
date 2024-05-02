import aiohttp
import asyncio
import json
from datetime import datetime, timedelta

class NBPApiClient:
    BASE_URL = "http://api.nbp.pl/api/exchangerates/tables/A/"

    async def fetch_exchange_rates(self, days):
        exchange_rates = []
        async with aiohttp.ClientSession() as session:
            for i in range(days):
                date = datetime.now() - timedelta(days=i)
                formatted_date = date.strftime("%Y-%m-%d")
                url = f"{self.BASE_URL}{formatted_date}"
                try:
                    async with session.get(url) as response:
                        data = await response.json()
                        exchange_rate_data = self.extract_eur_usd_rate(data)
                        exchange_rates.append({formatted_date: exchange_rate_data})
                except Exception as e:
                    print(f"Error fetching data for {formatted_date}: {e}")
        return exchange_rates

    def extract_eur_usd_rate(self, data):
        rates = data[0]['rates']
        eur_data = next((rate for rate in rates if rate['code'] == 'EUR'), None)
        usd_data = next((rate for rate in rates if rate['code'] == 'USD'), None)
        if eur_data and usd_data:
            return {
                'EUR': {
                    'sale': eur_data['mid'],
                    'purchase': eur_data['mid']
                },
                'USD': {
                    'sale': usd_data['mid'],
                    'purchase': usd_data['mid']
                }
            }
        return None

async def main():
    days = 10  # number of days to fetch exchange rates for
    api_client = NBPApiClient()
    exchange_rates = await api_client.fetch_exchange_rates(days)
    print(json.dumps(exchange_rates, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
