import aiohttp
import asyncio
import json

domain = input("Please input your domain: ")

async def main():

    secret_key = input("Please input your Secret Key: ")
    authorization_code = input("Please input your Authorization Code: ")


    async with aiohttp.ClientSession() as session: 
        base = f"https://{domain}.kommo.com"

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
            else:
                print(response_auth)
                print("\n\nPlease try again!\n")
                await main()



asyncio.run(main())
