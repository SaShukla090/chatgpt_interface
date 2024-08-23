from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from flask import Flask, render_template, request, jsonify
import time

# Flask setup
app = Flask(__name__)

# Headless Chrome setup
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options)

# Open ChatGPT
driver.get("https://chat.openai.com/chat")
time.sleep(5)  # Adjust sleep time based on your network speed

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    user_input = request.json['input']
    
    # Find the chat input box and send the message
    chat_input = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
    chat_input.send_keys(user_input + Keys.RETURN)
    
    # Wait for the response
    time.sleep(5)  # Adjust based on your needs

    # Extract the last message from the chat
    messages = driver.find_elements(By.XPATH, '//div[contains(@class,"flex flex-grow items-start gap-4")]')
    last_message = messages[-1].text

    return jsonify({'response': last_message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
