from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)

@app.route('/use-cookie', methods=['POST'])
def use_cookie():

    cookies = request.json.get("cookies", "")
    user_agent = request.json.get("user_agent", "")
    imei = request.json.get("imei", "")

    if not cookies or not user_agent or not imei:
        return jsonify({"error": "Cookies, User-Agent and IMEI is required!"}), 400

    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument(f"user-agent={user_agent}")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get('https://chat.zalo.me/')
    
    cookie_dict = cookies.split(';')
    for cookie in cookie_dict:
        cookie_name_value = cookie.strip().split('=')
        if len(cookie_name_value) == 2:
            driver.add_cookie({"name": cookie_name_value[0], "value": cookie_name_value[1]})

    # driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
    #     'headers': {
    #         'imei': imei
    #     }
    # })

    driver.execute_script(f"localStorage.setItem('z_uuid', '{imei}');")


    driver.refresh()

    time.sleep(8)

    screenshot = driver.get_screenshot_as_base64()

    driver.quit()

    return jsonify({
        "message": "Successfully!",
        "screenshot": screenshot
    })

@app.route('/', methods=['GET'])
def home():
    
    url = request.args.get('url', 'https://www.google.com')

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)

    time.sleep(5)

    screenshot = driver.get_screenshot_as_base64()

    driver.quit()

    return f'''
        <html>
            <body>
                <h1>Google Screenshot</h1>
                <img src="data:image/png;base64,{screenshot}" alt=" Screenshot"/>
            </body>
        </html>
    '''

if __name__ == "__main__":
    app.run(debug=True)