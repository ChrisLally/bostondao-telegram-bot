# to update requirements.txt run: pipreqs --savepath requirements.txt .
import os
import traceback
import asyncio
import requests
import json
from dotenv import load_dotenv  # Import the load_dotenv function

local = False if os.getenv("PRODUCTION") else True
# Load environment variables from the .env file only if running locally
if local:
    load_dotenv()

telegram_api_key=os.getenv("TELEGRAM_API_KEY")

async def respondToMessage(input_json):
    chatId=input_json["message"]["chat"]["id"]
    text="the python function got your message! "+input_json["message"]["text"]+" AND here is all the data we got and can work with: "+json.dumps(input_json)
    get_url=f"https://api.telegram.org/bot{telegram_api_key}/sendMessage?chat_id={chatId}&text={text}"
    print('getting', get_url)
    requests.get(get_url)
    
    return "ok"

async def handle_request_async(request):
    if local:
        assert isinstance(request, dict)
        request_json = request
    else:
        request_json = request.get_json(silent=True)
        
    print("got request!")
    print(request_json)
    
    try:
        if request_json.get("message"):
            return_final = await respondToMessage(request_json)
            return (return_final, 200)
        else:
            print('no message in payload')
            return ('no message in payload', 500)

    except Exception as e:
        print(e)
        traceback.print_exception(type(e), e, e.__traceback__)
        return (str(e), 500)

def handle_request(request):
    return asyncio.run(handle_request_async(request))

async def main():
    example_request={'update_id': 7551784, 'message': {'message_id': 45, 'from': {'id': 755872907, 'is_bot': False, 'first_name': 'Chris', 'last_name': 'Lally | Fide.id', 'username': 'chrislally', 'language_code': 'en'}, 'chat': {'id': 755872907, 'first_name': 'Chris', 'last_name': 'Lally | Fide.id', 'username': 'chrislally', 'type': 'private'}, 'date': 1698847077, 'text': 'test2'}} 
    result = await handle_request_async(example_request)
    return result


if local:
    result = asyncio.run(main())
    print(result)