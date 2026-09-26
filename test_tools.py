from core.ai_service import AIService


ai = AIService()

response = ai.generate(
    "Open Chrome using the available tool."
)

print()
print("FINAL RESPONSE:")
print(response)