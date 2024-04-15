from playwright.async_api import *
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
import asyncio

class ChatGPT:
    def __init__(self, headless: bool) -> None:
        self.chat_url = 'https://chat.openai.com/'
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.is_running = False

    def __red_text(self, text) -> str:
        return f"```ansi\n\u001b[0;31m{text}\n```"
        
    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(**self.playwright.devices['iPhone 13 Pro Max'], color_scheme='dark', permissions=['clipboard-read', 'clipboard-write'])
        self.page = await self.context.new_page()
        await self.page.goto(self.chat_url, wait_until='load')
        self.is_running = True

    async def test(self):
        await self.page.locator('textarea#prompt-textarea').element_handle(timeout=1000)
        await self.page.locator('textarea#prompt-textarea').fill('haha')
        # self.pause()

    async def __wait_response_1(self):
        try:
            await self.page.get_by_test_id('send-button').element_handle()
        except PlaywrightTimeoutError:
            pass
        
    async def __wait_response_2(self):
        try:
            await self.page.locator('main button[as="button"]').element_handle()
        except PlaywrightTimeoutError:
            pass

    async def chat(self, message: str, attempts: int = 0) -> str:
        if not self.is_running:
            await self.start()
        if attempts >= 2:
            return self.__red_text('發生錯誤，請重試。')
        
        try:
            await self.page.locator('textarea#prompt-textarea').element_handle(timeout=1000)
        except:
            await self.context.clear_cookies()
            await self.page.goto(self.chat_url, wait_until='load')
            await self.chat(message, attempts + 1)

        # 輸入訊息
        await self.page.locator('textarea#prompt-textarea').fill(message)
        # 送出
        await self.page.get_by_test_id('send-button').click()
        
        # 等到ai回答完
        await self.page.wait_for_timeout(1000)
        tasks = [self.__wait_response_1(), self.__wait_response_2()]
        tasks = [asyncio.create_task(task) for task in tasks]

        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        for task in pending:
            task.cancel()

        try:
            # 獲取回應
            await self.page.locator('div[data-testid^="conversation"] span > button').last.click() # 點複製按鈕
            response_1 = await self.page.evaluate('navigator.clipboard.readText()')
            response_2 = await self.page.locator('div[data-message-author-role="assistant"]').last.text_content()
            response = response_1 or self.__red_text(response_2)
            return response
        except:
            await self.page.screenshot(path='error.jpg')
            return 'Failed'
        
    async def screenshot(self, path = None, full_page = None) -> bytes:
        return await self.page.screenshot(path=path, full_page=full_page)

    async def pause(self) -> None:
        if not self.headless:
            await self.page.pause()

    async def stop(self) -> None:
        if self.is_running:
            await self.context.close()
            await self.browser.close()
            await self.playwright.stop()
            self.is_running = False



async def main():
    chatgpt = ChatGPT(headless=False)
    try:
        await chatgpt.start()
        # await chatgpt.test()


        message = '給我一個python hello world範例，給兩種回應'
        # message = '什麼是edging'
        response = await chatgpt.chat(message)
        print(response)

        await chatgpt.pause()

    finally:
        if chatgpt:
            await chatgpt.stop()




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
    asyncio.run(main())