from bottle import route, run, request, abort, static_file
from fsm import TocMachine
import config
config.init()
PTT_URL = "https://www.ptt.cc"
VERIFY_TOKEN = "123"
machine = TocMachine(
    states=[
        'initial',
        'intro',
        'ready',
        'get',
        'beauty',
        'money'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'initial',
            'dest': 'intro',
            'conditions': 'initial_to_intro'

        },
        {
            'trigger': 'advance',
            'source': 'intro',
            'dest': 'get',
            'conditions': 'intro_to_get'
        },
        {
            'trigger': 'advance',
            'source': 'intro',
            'dest': 'beauty',
            'conditions': 'intro_to_beauty'
        },
        {
            'trigger': 'advance',
            'source': 'intro',
            'dest': 'money',
            'conditions': 'intro_to_money'
        },

        {
            'trigger': 'advance',
            'source': 'ready',
            'dest': 'get',
            'conditions': 'ready_to_get'
        },
        {
            'trigger': 'advance',
            'source': 'ready',
            'dest': 'beauty',
            'conditions': 'ready_to_beauty'
        },
        {
            'trigger': 'advance',
            'source': 'ready',
            'dest': 'money',
            'conditions': 'ready_to_money'
        },
        {
            'trigger': 'advance',
            'source': 'ready',
            'dest': 'intro',
            'conditions': 'ready_to_intro'
        },

        {
            'trigger': 'go_back',
            'source': [
                'get',
                'beauty',
                'money'
            ],
            'dest': 'ready'
        }
    ],
    initial='initial',
    auto_transitions=False,
    show_conditions=True,
    ignore_invalid_triggers=True
)

machine.get_graph().draw('fsm.png', prog='dot', format='png')
config.save_image()

@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge

    else:
        abort(403)


@route("/webhook", method="POST")
def webhook_handler():
    body = request.json
    print('\nFSM STATE: ' + machine.state)
    print('REQUEST BODY: ')
    print(body)

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        machine.advance(event)
        return 'OK'


if __name__ == "__main__":
    run(host="localhost", port=5000, debug=True)
