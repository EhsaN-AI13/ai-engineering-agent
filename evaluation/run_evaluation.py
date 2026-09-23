from evaluation.cases import EVALUATION_CASES
from evaluation.evaluator import Evaluator
from evaluation.mock_agent import MockAgent


agent = MockAgent()

evaluator = Evaluator(agent)

results = evaluator.run_all(EVALUATION_CASES)

report = evaluator.generate_report(results)

category_report = evaluator.generate_category_report(results)

print("Evaluation Report")
print("------------------")

for result in results:
    status = "PASS" if result["passed"] else "FAIL"

    print(
        f"[{status}] {result['input']}"
    )

print()
print("Category Report")
print("------------------")

for category, data in category_report.items():
    print(f"{category}:")
    print(f"  Total: {data['total']}")
    print(f"  Passed: {data['passed']}")
    print(f"  Failed: {data['failed']}")
    print(f"  Score: {data['score']:.2%}")
    print()

print()
print(f"Total: {report['total']}")
print(f"Passed: {report['passed']}")
print(f"Failed: {report['failed']}")
print(f"Score: {report['score']:.2%}")