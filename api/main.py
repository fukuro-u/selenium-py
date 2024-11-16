from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

@app.route('/use-cookie', methods=['POST'])
def use_cookie():
    # Nhận cookie từ request
    cookies = request.json.get("cookies", [])
    
    if not cookies:
        return jsonify({"error": "Cookies không hợp lệ!"}), 400

    # Thiết lập các options cho chế độ headless
    options = Options()
    options.add_argument("--headless")  # Chạy ở chế độ không hiển thị UI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")  # Cần thiết cho headless trên Linux
    
    # Khởi tạo trình duyệt Chrome với Selenium
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    
    # Truy cập vào Zalo Web (hoặc trang web cần tự động hóa)
    driver.get('https://chat.zalo.me/')
    
    # Thêm cookie vào trình duyệt
    for cookie in cookies:
        driver.add_cookie({"name": cookie["name"], "value": cookie["value"]})

    # Tải lại trang để xác nhận cookie đã được thêm vào
    driver.refresh()

    # Chờ vài giây để trang tải xong
    time.sleep(5)

    # Chụp ảnh màn hình để kiểm tra kết quả (hoặc thực hiện tác vụ khác)
    screenshot = driver.get_screenshot_as_base64()  # Ảnh chụp màn hình dưới dạng base64

    # Đóng trình duyệt
    driver.quit()

    # Trả về kết quả, ví dụ là ảnh chụp màn hình
    return jsonify({
        "message": "Tác vụ hoàn tất.",
        "screenshot": screenshot
    })


if __name__ == "__main__":
    app.run(debug=True)
