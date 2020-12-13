import asyncio
import aiohttp
import http.client
from timeit import default_timer as timer


async def main():
    await httpExample()


async def httpExample():
    statusSet = set()

    urls = [f'https://httpbin.org/status/{status}' for status in range(0, 50)]
    urlPaths = [f'/status/{status}' for status in range(200, 250)]

    print("== HTTP parallel ==\n")
    start = timer()
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=2)) as session:
        statusSet = await asyncio.gather(*[
            fetch(session, url)
            for url in urls
        ])
    end = timer()
    assert len(statusSet) == 50
    print(end-start)

    base = "httpbin.org"
    conn = http.client.HTTPSConnection(base, timeout=2)
    statusSet = set()

    print("\n== HTTP serial ==\n")
    start = timer()
    for url in urlPaths:
        conn.request("GET", url)
        resp = conn.getresponse()
        resp.read()
        statusSet.add(resp.status)

    end = timer()
    assert len(statusSet) == 50
    print(end-start)


async def fetch(session, url):
    async with session.get(url) as resp:
        await resp.read()
        return resp.status

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
