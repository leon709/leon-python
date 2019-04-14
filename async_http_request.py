#!/usr/bin/env python3
# areq.py
# require: python 3.7+

"""Asynchronously get links embedded in multiple pages' HMTL."""

import asyncio
import logging
import re
import sys
from typing import IO
import urllib.error
import urllib.parse
import json
import aiofiles
import aiohttp
from aiohttp import ClientSession

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("areq")
logging.getLogger("chardet.charsetprober").disabled = True

# HREF_RE = re.compile(r'href="(.*?)"')

tmpl1 = '''
<tr><td width='100px' ></td><td> {id} <a href='{officialURL}' target='_blank'>官网</a> &nbsp; {status}</td></tr>
<tr><td>brand:</td><td>{brand}</td></tr>
<tr><td>name:</td><td>{name} | {nameCN}</td></tr>
<tr><td>category:</td><td>{category}</td></tr>
<tr><td>分类:</td><td>{cats}</td></tr>
<tr><td colspan='2' style='border-bottom:1px solid;'>{image_html}</td></tr>
'''


async def fetch_data(url: str, session: ClientSession, **kwargs) -> str:
    """GET request wrapper to fetch page HTML.

    kwargs are passed to `session.request()`.
    """

    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    logger.info("Got response [%s] for URL: %s", resp.status, url)
    data = await resp.json()
    # resp.text()  # for html
    return data


async def parse(url: str, category_base: dict, session: ClientSession, **kwargs) -> set:
    """Find HREFs in the HTML of `url`."""
    prod_html = ''
    try:
        prod = await fetch_data(url=url, session=session, **kwargs)
    except (
        aiohttp.ClientError,
        aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        logger.error(
            "aiohttp exception for %s [%s]: %s",
            url,
            getattr(e, "status", None),
            getattr(e, "message", None),
        )
        return prod_html
    except Exception as e:
        logger.exception("Non-aiohttp exception occured:  %s", getattr(e, "__dict__", {}))
        return prod_html
    else:
        prod['nameCN'] = prod.get('nameCN', '')
        prod['cats'] = "<br> ".join([c + ': ' + category_base.get(c, c) for c in prod.get('categoryIds', [])])
        # first_img_url = prod['images'][0]['thumbnail']['url']
        # r = requests.post('http://localhost:5001/what', json={'url': first_img_url}).json()
        prod['image_html'] = imgs_table([i['thumbnail']['url'] for i in prod.get('images', [])])
        prod['status'] = ''
        if prod['inventoryStatus'] != "AVAILABLE":
            prod['status'] = "<font color='red'> {} <font>".format(prod['inventoryStatus'])
        prod_html = tmpl1.format(**prod)
        return prod_html


async def write_one(file: IO, url: str, category_map: dict, **kwargs) -> None:
    """Write the found HREFs from `url` to `file`."""
    res = await parse(url=url, category_base=category_map, **kwargs)
    if not res:
        return None
    async with aiofiles.open(file, "a") as f:
        await f.write(res)
        logger.info("Wrote results for source URL: %s", url)


async def bulk_crawl_and_write(file: IO, pids: list, category_map: dict, **kwargs) -> None:
    """Crawl & write concurrently to `file` for multiple `urls`."""
    async with ClientSession() as session:
        tasks = []
        for p in pids:
            url = 'https://xxx.com/api/xxx/' + p
            tasks.append(
                write_one(file=file, url=url, category_map=category_map, session=session, **kwargs)
            )
        await asyncio.gather(*tasks)


def load_cats():
    cats = {}
    with open('/Users/leon/eclipse-workspace/MyLab/tools/categories.txt') as f:
        for l in f:
            c = l.strip().split(' ', 1)
            cats[c[0]] = c[1]
    return cats


def imgs_table(urls):
    imgs = []
    for u in urls:
        imgs.append(u"<img src='{}' width='100' />".format(u))
    return ''.join(imgs)


def load_from_file(pidsfile):
    try:
        prods = json.load(open(pidsfile))
    except Exception:
        prods = [l.strip() for l in open(pidsfile) if l.strip()]
    return prods


if __name__ == "__main__":
    import pathlib
    import sys

    assert sys.version_info >= (3, 7), "Script requires Python 3.7+."
    here = pathlib.Path(__file__).parent
    # print(here)
    # with open(here.joinpath("pidlist")) as infile:
    #    urls = set(map(str.strip, infile))

    pidlist = load_from_file('pidlist')
    category_mapping = load_cats()
    outpath = here.joinpath("prod_list.html")
    with open(outpath, "w") as outfile:
        outfile.write("<html><body><table style='border: 1px solid;border-collapse:collapse;' width='800'>\n")

    asyncio.run(bulk_crawl_and_write(file=outpath, pids=pidlist, category_map=category_mapping))

    with open(outpath, "a") as outfile:
        outfile.write('</table></body></html>\n')
