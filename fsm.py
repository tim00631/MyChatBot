from transitions.extensions import GraphMachine
from utils import send_text_message, send_image_url
import config
import time
import random
random.seed(time)
PTT_URL = "https://www.ptt.cc"


class TocMachine(GraphMachine):

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )

    def initial_to_intro(self, event):
        if event.get("message") and event['message'].get("text"):
        # if event.get("message"):
            text = event['message']['text']
            return text.lower() == '開始'
        return False
    def intro_to_get(self, event):
        if event.get("message") and event['message'].get("text"):
        # if event.get("message"):
            text = event['message']['text']
            return text.lower() == '抽卡'
        return False
    def intro_to_beauty(self, event):
        if event.get("message") and event['message'].get("text"):
        # if event.get("message"):
            text = event['message']['text']
            return text.lower() == '表特'
        return False

    def intro_to_money(self, event):
        if event.get("message") and event['message'].get("text"):
        # if event.get("message"):
            text = event['message']['text']
            return text.lower() == '省錢'
        return False

    def ready_to_get(self, event):
        #if event.get("message"):
        if event.get("message") and event['message'].get("text"):
            text = event['message']['text']
            return text.lower() == '抽卡'
        return False

    def ready_to_beauty(self, event):
        #if event.get("message"):
        if event.get("message") and event['message'].get("text"):
            text = event['message']['text']
            return text.lower() == '表特'
        return False

    def ready_to_money(self, event):
        # if event.get("message"):
        if event.get("message") and event['message'].get("text"):
            text = event['message']['text']
            return text.lower() == '省錢'
        return False

    def ready_to_intro(self, event):
        #if event.get("message"):
        if event.get("message") and event['message'].get("text"):
            text = event['message']['text']
            return text.lower() == 'help'
        return False

    def on_enter_intro(self, event):
        print("I'm entering intro")
        sender_id = event['sender']['id']
        send_text_message(sender_id, "指令集:\n抽卡\n表特\n省錢\nhelp\n")
        send_text_message(sender_id, "請輸入你要的功能\n")

    def on_enter_ready(self):
        print("I'm entering ready")

    def on_enter_get(self, event):
        print("I'm entering get")
        sender_id = event['sender']['id']
        send_image_url(sender_id, random.choice(config.img_urls))
        self.go_back()

    def on_enter_beauty(self, event):
        print("I'm entering beauty")
        articles = []
        current_page = config.get_web_page(PTT_URL + '/bbs/Beauty/index.html')
        if current_page:
            date = time.strftime("%m/%d").lstrip('0')  # Today's date format, to fit PTT URL format.
            current_articles, prev_url = config.get_articles(dom=current_page, date=date, threshold=0)
            while current_articles:  # if current page has articles we want to add
                articles += current_articles  # add them
                current_page = config.get_web_page(PTT_URL + prev_url)  # ready to previous page
                current_articles, prev_url = config.get_articles(current_page, date, 0)  # Go!
            sender_id = event['sender']['id']
            message = "今日貼文:\n\n"
            for x in articles:
                message = message + x["title"] + "\n"  # Title
                message = message + PTT_URL + x["href"] + "\n"  # Hyperlink
                message = message + "推文數:" + str(x["push_count"]) + "\n"  # Push_Count
            send_text_message(sender_id, message)
        self.go_back()

    def on_enter_money(self, event):
        print("I'm entering Life is money")
        sender_id = event['sender']['id']
        message = config.money()
        send_text_message(sender_id, message)
        self.go_back()
