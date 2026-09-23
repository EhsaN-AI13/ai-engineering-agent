class ToolSelector:

    def __init__(self, registry):
        self.registry = registry

    def select(self, user_input):
        user_input = user_input.lower()

        if "تعداد کلمات" in user_input or "چند کلمه" in user_input:
            return "count_words"

        if any(
            symbol in user_input
            for symbol in ["+", "-", "*", "/"]
        ):
            return "calculator"

        if any(
            keyword in user_input
            for keyword in [
                "جمع",
                "بعلاوه",
                "تفریق",
                "منهای",
                "ضرب",
                "ضربدر",
                "تقسیم",
                "تقسیم بر"
            ]
        ):
            return "calculator"

        return None