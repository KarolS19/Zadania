import aiohttp
import asyncio
import sys
from datetime import datetime, timedelta

async def fetch_exchange_rates(days_back):
    async with aiohttp.ClientSession() as session:
        rates = []
        for i in range(days_back):
            date = (datetime.now() - timedelta(days=i)).strftime('%d.%m.%Y')
            url = f'http://api.nbp.pl/api/exchangerates/tables/A/{date}/?format=json'
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        rates_dict = {'EUR': {}, 'USD': {}}
                        for rate in data[0]['rates']:
                            if rate['code'] == 'EUR' or rate['code'] == 'USD':
                                rates_dict[rate['code']]['sale'] = rate['ask']
                                rates_dict[rate['code']]['purchase'] = rate['bid']
                        rates.append({date: rates_dict})
                    else:
                        rates.append({date: 'Error fetching data'})
            except aiohttp.ClientError as e:
                rates.append({date: f'Error: {str(e)}'})
    return rates

async def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <days_back>")
        return

    try:
        days_back = int(sys.argv[1])
    except ValueError:
        print("Please provide a valid number of days.")
        return

    if days_back <= 0 or days_back > 10:
        print("Please provide a number of days between 1 and 10.")
        return

    rates = await fetch_exchange_rates(days_back)
    print(rates)

if __name__ == '__main__':
    asyncio.run(main())
