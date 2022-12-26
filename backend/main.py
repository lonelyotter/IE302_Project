from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import json
import base64
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus
import ssl
from key import API_KEY, SECRET_KEY

ssl._create_default_https_context = ssl._create_unverified_context

OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"

TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'


def fetch_token():
    """
    获取token
    """
    params = {
        'grant_type': 'client_credentials',
        'client_id': API_KEY,
        'client_secret': SECRET_KEY
    }
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)

    result_str = result_str.decode()

    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print('please overwrite the correct API_KEY and SECRET_KEY')
        exit()


def request(url, data):
    """
    调用远程服务
    """
    req = Request(url, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        result_str = result_str.decode()
        return result_str
    except URLError as err:
        print(err)


app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def index():
    return {"message": "Hello World"}


@app.post('/image')
async def image(img: UploadFile = File(...)):
    filename = img.filename
    print(filename)
    try:
        content = await img.read()
        token = fetch_token()
        image_url = OCR_URL + "?access_token=" + token
        text = ""
        result = request(image_url,
                         urlencode({'image': base64.b64encode(content)}))
        result = json.loads(result)
        for words in result['words_result']:
            text = text + words['words'] + ' '
        return text

    except Exception as e:
        return "error"


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
