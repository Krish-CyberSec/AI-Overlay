from app.ai.client import ask_ai


question = "Explain what a firewall is in one sentence."

answer = ask_ai(question)

print("\nAI RESPONSE:")
print(answer)