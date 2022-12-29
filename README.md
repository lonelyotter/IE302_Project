# IE302_Project

A simple image OCR application.

frontend: Weixin mini program

backend: Python fastapi, Baidu OCR

## build

### frontend

1. Open frontend program in Weixin DevTools.

2. Create file `serverURL.js`  and add the following line.

   ```javascript
   export const serverURL = "http://<your backend server>:8000/image"
   ```

3. Build the program.

### backend

1. Create Python virtual environment.

   ```shell
   python3 -m venv .venv
   source .venv/bin/activate
   pip3 install -r requirements.txt
   ```

2. Get your Baidu OCR API key and secret key.

3. Create file `key.py` and add the following lines.

   ```python
   API_KEY = "your API key"
   SECRET_KEY = "your secret key"
   ```

4. Build and run.

   ```shell
   python3 main.py
   ```

   
