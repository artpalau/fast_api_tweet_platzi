import json

with open("users.json", "r+", encoding="utf-8") as f:
    results = json.loads(f.read())
    print(results)
    for user_data in results:
        print(user_data)
        print(user_data["user_id"])
