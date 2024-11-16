from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

# Định nghĩa route để nhận cookie và user-agent
@app.route('/use-cookie', methods=['POST'])
def use_cookie():
    cookies = request.json.get("cookies", "")
    user_agent = request.json.get("user_agent", "")
    imei = request.json.get("imei", "")

    if not cookies or not user_agent or not imei:
        return jsonify({"error": "Cookies, User-Agent and IMEI is required!"}), 400

    # Thiết lập các options cho Selenium
    options = Options()
    options.add_argument("--headless")  # Headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument(f"user-agent={user_agent}")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get('https://chat.zalo.me/')
    
    # Cài đặt cookie
    cookie_dict = cookies.split(';')
    for cookie in cookie_dict:
        cookie_name_value = cookie.strip().split('=')
        if len(cookie_name_value) == 2:
            driver.add_cookie({"name": cookie_name_value[0], "value": cookie_name_value[1]})

    # Thiết lập IMEI vào localStorage
    driver.execute_script(f"localStorage.setItem('z_uuid', '{imei}');")

    driver.refresh()
    time.sleep(8)

    # Chụp ảnh màn hình dưới dạng base64
    screenshot = driver.get_screenshot_as_base64()
    
    driver.quit()
    
    return jsonify({
        "message": "Successfully!",
        "screenshot": screenshot
    })

# Route để lấy trang web và trả về HTML
@app.route('/', methods=['GET'])
def index():
    url = request.args.get('url', 'https://www.google.com')  # URL mặc định là Google nếu không có tham số
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(url)
    
    # Lấy HTML của trang
    page_html = driver.page_source
    
    driver.quit()
    
    return page_html

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)