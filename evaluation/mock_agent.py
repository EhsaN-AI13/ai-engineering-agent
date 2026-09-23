class MockAgent:

    def __init__(self):
        self.responses = {
            "10 ضربدر 5 چند میشه؟": "50",
            "20 به علاوه 30 چند میشه؟": "50",
            "100 منهای 40 چند میشه؟": "60",
            "20 تقسیم بر 4 چند میشه؟": "5.0",
            "محتویات فایل test.txt را بخوان.": (
                "Python is a powerful programming language."
            )
        }

    def run(self, user_input):
        return self.responses[user_input]