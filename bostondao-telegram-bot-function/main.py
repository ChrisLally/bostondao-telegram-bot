# to update requirements.txt run: pipreqs --savepath requirements.txt .
import os
import traceback
import asyncio
import requests

async def myFunction(input):
    return input

async def handle_request_async(request):
    if local:
        assert isinstance(request, dict)
        request_json = request
    else:
        request_json = request.get_json(silent=True)

    try:
        if request_json.get("key"):
            return_final = await myFunction(request_json)
            return (return_final, 200)
        elif(request_json.get("key2")):
            return_final = await myFunction(request_json)
            return (return_final, 200)

    except Exception as e:
        print(e)
        traceback.print_exception(type(e), e, e.__traceback__)
        return (str(e), 500)

def handle_request(request):
    return asyncio.run(handle_request_async(request))

async def main():
    result = await handle_request_async({"key": "value"})
    return result

local = False if os.getenv("PRODUCTION") else True

if local:
    result = asyncio.run(main())
    print(result)