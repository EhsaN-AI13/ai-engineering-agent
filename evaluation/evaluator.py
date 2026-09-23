class Evaluator:

    def __init__(self, agent):
        self.agent = agent

    def run_case(self, user_input, expected_output, category="unknown"):
        actual_output = self.agent.run(user_input)

        return {
            "input": user_input,
            "expected": expected_output,
            "actual": actual_output,
            "passed": actual_output == expected_output,
            "category": category
        }

    def run_all(self, cases):
        results = []

        for case in cases:
            result = self.run_case(
                case["input"],
                case["expected"],
                case.get("category", "unknown")
            )

            results.append(result)

        return results

    def calculate_score(self, results):
        if not results:
            return 0

        passed = sum(
            1 for result in results
            if result["passed"]
        )

        return passed / len(results)

    def generate_report(self, results):
        score = self.calculate_score(results)

        return {
            "total": len(results),
            "passed": sum(
                1 for result in results
                if result["passed"]
            ),
            "failed": sum(
                1 for result in results
                if not result["passed"]
            ),
            "score": score
        }
    def generate_category_report(self, results):
        categories = {}

        for result in results:
            category = result.get("category", "unknown")

            if category not in categories:
                categories[category] = {
                    "total": 0,
                    "passed": 0,
                    "failed": 0
                }

            categories[category]["total"] += 1

            if result["passed"]:
                categories[category]["passed"] += 1
            else:
                categories[category]["failed"] += 1

        for category in categories:
            total = categories[category]["total"]
            passed = categories[category]["passed"]

            categories[category]["score"] = (
                passed / total if total else 0
            )

        return categories