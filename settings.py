TOKEN = "4b174377a427d294-7f4611c4c2ec7fcb-6e508f5b5b241329"
URL = "https://englishbotpro.herokuapp.com/"
# URL = "https://endlishbotpro.pythonanywhere.com/"
WEBHOOK = URL + '/incoming'
HELLO_MESSAGE = "Привет! Я Бот из Англии в четвёртом поколении. Я помогу тебе выучить английский язык. "\
               "Для начала введи Start или нажми на кнопку внизу"

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
	"Text": "Давай начнём!"
	},
    {"Columns": 6,
    "Rows": 1,
    "BgColor": "#e6f5ff",
    "BgMedia": "http://link.to.button.image",
    "BgMediaType": "picture",
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Dismiss",
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
        "Text": "Посмотреть пример использования"
    }
    ]
}
