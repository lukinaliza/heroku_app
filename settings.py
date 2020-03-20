TOKEN = "4b2e878b11a7dcf6-d0e5e1700968f6bc-5d1a4fa7e8098131"
#URL = "https://englishbotpro.herokuapp.com/"
# URL = "https://678103ac.ngrok.io"
# URL = "https://endlishbotpro.pythonanywhere.com/"
WEBHOOK = URL + '/incoming'
HELLO_MESSAGE = "Привет. Этот бот предназначен для заучивания иностранных слов\n" \
             "Для начала нажмите на кнопку или напишите 'Старт'"

START_KEYBOARD = {
"Type": "keyboard",
"Buttons": [
	{
	"Columns": 6,
	"Rows": 1,
	"BgColor": "#e6f5ff",
	"BgMedia": "http://link.to.button.image",
	"BgMediaType": "picture",
	"BgLoop": True,
	"ActionType": "reply",
	"ActionBody": "Start",
	"ReplyType": "message",
	"Text": "Старт"
	}
    ]
}

WAIT_KEYBOARD = {
"Type": "keyboard",
"Buttons": [
	{
	"Columns": 6,
	"Rows": 1,
	"BgColor": "#e6f5ff",
	"BgMedia": "http://link.to.button.image",
	"BgMediaType": "picture",
	"BgLoop": True,
	"ActionType": "reply",
	"ActionBody": "Start",
	"ReplyType": "message",
	"Text": "Старт"
	},
    {"Columns": 6,
    "Rows": 1,
    "BgColor": "#e6f5ff",
    "BgMedia": "http://link.to.button.image",
    "BgMediaType": "picture",
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Later",
    "ReplyType": "message",
    "Text": "Чуть позже"
    }
    ]
}

SAMPLE_KEYBOARD = {
"Type": "keyboard",
"Buttons": [
	{
	"Columns": 3,
	"Rows": 1,
	"BgColor": "#e6f5ff",
	"BgMedia": "http://link.to.button.image",
	"BgMediaType": "picture",
	"BgLoop": True,
	"ActionType": "reply",
	"ActionBody": "But1",
	"ReplyType": "message",
	"Text": "Push me!"
	},
    {
        "Columns": 3,
        "Rows": 1,
        "BgColor": "#e6f5ff",
        "BgMedia": "http://link.to.button.image",
        "BgMediaType": "picture",
        "BgLoop": True,
        "ActionType": "reply",
        "ActionBody": "But2",
        "ReplyType": "message",
        "Text": "Push me too!"
    },
    {
        "Columns": 3,
        "Rows": 1,
        "BgColor": "#e6f5ff",
        "BgMedia": "http://link.to.button.image",
        "BgMediaType": "picture",
        "BgLoop": True,
        "ActionType": "reply",
        "ActionBody": "But3",
        "ReplyType": "message",
        "Text": "Push me 3!"
    },
    {
        "Columns": 3,
        "Rows": 1,
        "BgColor": "#e6f5ff",
        "BgMedia": "http://link.to.button.image",
        "BgMediaType": "picture",
        "BgLoop": True,
        "ActionType": "reply",
        "ActionBody": "But4",
        "ReplyType": "message",
        "Text": "Push me 4!"
    },
    {
        "Columns": 6,
        "Rows": 1,
        "BgColor": "#e6f5ff",
        "BgMedia": "http://link.to.button.image",
        "BgMediaType": "picture",
        "BgLoop": True,
        "ActionType": "reply",
        "ActionBody": "showExample",
        "ReplyType": "message",
        "Text": "Пример использования"
    }
    ]
}
