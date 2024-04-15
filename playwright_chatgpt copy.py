from playwright.sync_api import *
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import asyncio


class ChatGPT:
    def __init__(self, headless: bool) -> None:
        self.chat_url = 'https://chat.openai.com/'
        self.headless = headless

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context(**self.playwright.devices['iPhone 13 Pro Max'], color_scheme='dark', permissions=['clipboard-read', 'clipboard-write'])
        self.page = self.context.new_page()
        self.page.goto(self.chat_url, wait_until='load')

    def test(self):
        self.page.locator('textarea#prompt-textarea').element_handle(timeout=1000)
        self.page.locator('textarea#prompt-textarea').fill('haha')
        self.pause()

    def chat(self, message: str, attempts: int = 0) -> str:
        if attempts >= 2:
            return '發生錯誤，請重試。'
        
        try:
            self.page.locator('textarea#prompt-textarea').element_handle(timeout=1000)
        except:
            self.page.goto(self.chat_url, wait_until='load')
            self.chat(message, attempts + 1)

        # 輸入訊息
        self.page.locator('textarea#prompt-textarea').fill(message)
        # 送出
        self.page.get_by_test_id('send-button').click()
        
        try:
            # 等到ai回答完
            self.page.wait_for_timeout(1000)
            self.page.get_by_test_id('send-button').element_handle()
            # self.page.locator('main button[as="button"]').element_handle()

            # 獲取回應
            self.page.locator('div[data-testid^="conversation"] span > button').last.click() # 點複製按鈕
            response_1 = self.page.evaluate('navigator.clipboard.readText()')
            response_2 = self.page.locator('div[data-message-author-role="assistant"]').last.text_content()
            response = response_1 if response_1 else response_2
            return response
        except:
            return 'Failed'

    def pause(self) -> None:
        if not self.headless:
            self.page.pause()

    def exit(self) -> None:
        self.context.close()
        self.browser.close()
        self.playwright.stop()



def main():
    chatgpt = ChatGPT(headless=False)
    try:
        # chatgpt.test()

        # message = '給我一個python hello world範例'
        message = '𒐫'*3000
        response = chatgpt.chat(message)
        print(response)

        chatgpt.pause()

    finally:
        if chatgpt:
            chatgpt.exit()




""" with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    # context = browser.new_context(**p.devices['Desktop Chrome'], color_scheme='dark', permissions=['clipboard-read', 'clipboard-write'])
    context = browser.new_context(**p.devices['iPhone 13 Pro Max'], color_scheme='dark', permissions=['clipboard-read', 'clipboard-write'])
    # context = browser.new_context(**p.devices['Desktop Firefox'], color_scheme='dark')

    # if os.path.isfile(COOKIES_PATH) and os.stat(COOKIES_PATH).st_size:
    #     with open(COOKIES_PATH, 'rb') as f:
    #         cookies = json.loads(fernet.decrypt(f.read()))
    #         context.add_cookies(cookies)

    page = context.new_page()
    # page.add_init_script(path='hide-webdriver.js')

    def Exit():
        # if context.cookies():
        #     with open(COOKIES_PATH, 'wb') as f:
        #         f.write(fernet.encrypt(json.dumps(context.cookies()).encode('utf-8')))

        context.close()
        browser.close()

    # page.goto('https://bot.sannysoft.com/', wait_until='networkidle')
    # page.screenshot(path='error.jpg')

    try:
        page.goto('https://chat.openai.com/')

        # prompt = '什麼是edging?'
        # prompt = '給我一個python hello world範例'
        prompt = '𒐫'*3000

        # 輸入訊息
        page.locator('textarea#prompt-textarea').fill(prompt)
        # 送出
        page.get_by_test_id('send-button').click()
        
        # 等到ai回答完
        page.wait_for_timeout(1000)
        page.get_by_test_id('send-button').focus()


        # 獲取回應
        page.locator('div[data-testid^="conversation"] span > button').last.click() # 點複製按鈕
        response_1 = page.evaluate('navigator.clipboard.readText()')
        response_2 = page.locator('div[data-message-author-role="assistant"]').last.text_content()
        response = response_1 if response_1 else response_2
        print(response)

    except:
        page.screenshot(path='error.jpg')
    
    page.pause()

    Exit() """


if __name__ == '__main__':
    main()