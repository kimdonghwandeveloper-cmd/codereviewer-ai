from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_llm_integration():
    # 간단한 버그가 있는 코드
    buggy_code = """
def calculate_average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers) 
    # Bug: Division by zero if numbers is empty
    """
    
    response = client.post(
        "/api/analyze",
        json={
            "code": buggy_code,
            "language": "python",
            "use_ai": True
        }
    )
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return

    data = response.json()
    print("=== Analysis Result ===")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    if "ai_feedback" in data and data["ai_feedback"]:
        print("\n[SUCCESS] AI Feedback received.")
    else:
        print("\n[FAIL] No AI Feedback found.")

if __name__ == "__main__":
    test_llm_integration()
