import tls_client
import pandas as pd
import time
import json
import asyncio
from playwright.async_api import async_playwright, Playwright, Request, Response



def _getStockTickersDataFrameByCountry(countryId):
    #  Constant function values
    BASE_URL = "https://api.investing.com/api/financialdata/assets/equitiesByCountry/default"

    HEADERS = {
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://mx.investing.com/',
        'domain-id': 'mx',
        'Origin': 'https://mx.investing.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Priority': 'u=0',
        'TE': 'trailers'
    }

    # Client for doing TLS Requests
    session = tls_client.Session(
        client_identifier="chrome112",
        random_tls_extension_order=True
    )
    
    # Function vars
    pageIndex = 0
    tickerDf = None

    while True:

        params = {
            "fields-list": "id,name,symbol,isCFD,high,low,last,lastPairDecimal,change,changePercent,volume,time,isOpen,url,flag,countryNameTranslated,exchangeId,performanceDay,performanceWeek,performanceMonth,performanceYtd,performanceYear,performance3Year,technicalHour,technicalDay,technicalWeek,technicalMonth,avgVolume,fundamentalMarketCap,fundamentalRevenue,fundamentalRatio,fundamentalBeta,pairType",
            "country-id": countryId,
            "filter-domain": None, # For parameters without a value
            "page": pageIndex,
            "page-size": 100,
            "limit": 0,
            "include-additional-indices": "false",
            "include-major-indices": "false",
            "include-other-indices": "false",
            "include-primary-sectors": "false",
            "include-market-overview": "false"
        }

        response = session.get(
            BASE_URL,
            headers=HEADERS,
            params=params
            ## TODO: Add a proxy to the request
        )

        # Parsing information from bytes -> string -> json
        bytesResponse = response.content
        jsonResponse = json.loads(bytesResponse.decode('utf-8'))

        try:
            if tickerDf is None:
                tickerDf = pd.DataFrame(jsonResponse["data"])
            else:
                tickerDf = pd.concat([tickerDf, pd.DataFrame(jsonResponse["data"])])
        except:
            break

        time.sleep(1)
        pageIndex += 1

    return tickerDf


# Use playwright ot selenium to do an initial request to Investing.com
# Enter https://mx.investing.com/equities/mexico

ONE_TIME_CONSTANT_REQ = True
ONE_TIME_CONSTANT_RES = True

def _getRequestData(request: Request):
    global ONE_TIME_CONSTANT_REQ
    if ONE_TIME_CONSTANT_REQ:
        ONE_TIME_CONSTANT_REQ = False
        print(request.headers)
        print()
    else:
        pass


def _getResponseData(response: Response):
    global ONE_TIME_CONSTANT_RES
    if ONE_TIME_CONSTANT_RES:
        ONE_TIME_CONSTANT_RES = False
        print(response.headers)
        print()
    else:
        pass


def _saveTableHTML(table: str, name):
    with open(name, 'w') as file:
        file.write(table)


def _parseTableHTMLToDataFrame(name):
    with open(name, 'r') as file:
        tableString = file.read()
        tableString = "<table>" + tableString + "</table>"

        df = pd.read_html(tableString)
        return df[0]


# Function running playwright to render the ETFs page
# - We read from the table to get the ticker information and additionl details
async def _run(playwright: Playwright, name):
    chromium = playwright.chromium

    # Initializing browser object (might look into making a singleton)
    browser = await chromium.launch(
        headless=False
        # TODO: Add a proxy
    )
    page = await browser.new_page()

    # ** Leaving for future use **
    # # Subscribe to "request" and "response" events in order to get the data (cookies)
    # page.on("request", lambda request: _getRequestData(request))
    # page.on("response", lambda response: _getResponseData(response))

    # Navigating to specific page
    await page.goto(
            "https://mx.investing.com/etfs/usa-etfs?&issuer_filter=0",
            wait_until="domcontentloaded"
        )
    
    # Extracting html from page
    table = await page.locator('#etfs').inner_html()

    # Saving the htm for later processing
    _saveTableHTML(table, f"{name}.txt")

    # Closing browser after completion
    await browser.close()


# Async function to execute asyn playwright in order to render a page
async def _async_getETFTickersDataFrameByCountry(name):
    async with async_playwright() as playwright:
        await _run(playwright, name)


# Sync function that can be called from anywhere in the code
def _getETFTickersDataFrameByCountry(name):
    # We use asyncio to run the async function
    asyncio.run(_async_getETFTickersDataFrameByCountry(name))


def saveETFTickersByCountry(county_id):
    countryDict = {
        5: "USA",
        7: "Mexico"
    }

    # Calling function to make the requests for etfs information
    _getETFTickersDataFrameByCountry(countryDict[county_id])

    # Save to CSV
    df = _parseTableHTMLToDataFrame(f"{countryDict[county_id]}.txt")

    # Save to csv
    df.to_csv(f'data/csv/etfs_{countryDict[county_id]}.csv', index=False)

    # Save to parquet
    df.to_parquet(f'data/parquet/etfs_{countryDict[county_id]}.parquet', index=False)


def saveStockTickersByCountry(county_id):
    countryDict = {
        5: "USA",
        7: "Mexico"
    }

    #  Calling function to make the requests for stocks information
    df = _getStockTickersDataFrameByCountry(county_id)

    # Save to csv
    df.to_csv(f'data/csv/stocks_{countryDict[county_id]}.csv', index=False)

    # Save to parquet
    df.to_parquet(f'data/parquet/stocks_{countryDict[county_id]}.parquet', index=False)