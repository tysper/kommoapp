import aiohttp
import asyncio
import json
from datetime import datetime
import time

domain = input("Please input your domain: ")

base = f"https://{domain}.kommo.com"
ids = []
keys = []


async def get_ids():

    secret_key = input("Please input your Secret Key: ")
    authorization_code = input("Please input your Authorization Code: ")


    async with aiohttp.ClientSession() as session: 
        

        auth_url = base+"/oauth2/access_token"
        auth_body = {
            "client_id": "7ebb8953-c354-42c8-a334-1060daa1a4bc",
            "client_secret": f"{secret_key}",
            "grant_type": "authorization_code",
            "code": f"{authorization_code}",
            "redirect_uri": "https://neutroid.com.br"
        }

        auth_headers = {
        'Content-Type': 'application/json'
        }

        async with session.post(auth_url, headers=auth_headers, json=auth_body) as auth_response:
            response_auth = await auth_response.json()

            if "access_token" in response_auth:
                # print("Access Token "+response_auth["access_token"])
                # print("Refresh Token "+response_auth["refresh_token"])
                print("\n")

                access_token = response_auth["access_token"]
                
                leads_url = base+"/api/v4/leads"
                leads_headers = {
                    "Authorization": f"Bearer {access_token}"
                } 
                async with session.get(leads_url, headers=leads_headers) as leads_response:
                    response_leads = await leads_response.json()
                    leads = response_leads["_embedded"]["leads"] #dict list
                    print(json.dumps(leads, indent=4))

                    for lead in leads:
                        ids.append(lead["id"])
                
                    keys.append(f"{access_token}")
            else:
                print(response_auth)
                print("\n\nPlease try again!\n")
                await get_ids()

#Get the ids from Kommmo
asyncio.run(get_ids())

async def fetch_info(session, id, token):
    async with session.get(f"{base}/api/v4/leads/{id}", headers={"Authorization": f"Bearer {token}"}) as r:
        if r.status != 200:
            r.raise_for_status()
        return await r.json()

async def fetch_all_info(session, ids, token):
    tasks = []
    for id in ids:
        task = asyncio.create_task(fetch_info(session, id, token))
        tasks.append(task)
    res = await asyncio.gather(*tasks)
    return res

async def get_complete_info(limit):
    async with aiohttp.ClientSession() as session:

        for start in range(0, len(ids), limit):
            ti = datetime.now().timestamp()
            end = start+limit
            if end>len(ids):
                end=len(ids)

            # print(f"Start: {start} End:{end}")

            responses = await fetch_all_info(ids=ids[start:end], session=session, token=keys[0])
            for response in responses:
                print(response)

            tf = datetime.now().timestamp()

            # print(f"Time: {(tf-ti)}s")
            #wait a second
            while tf-ti < 1:
                tf = datetime.now().timestamp()

#Fetch the ids in parallel with a limit of 5 requests per second
asyncio.run(get_complete_info(5))