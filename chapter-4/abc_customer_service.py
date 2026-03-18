"""
ABC Inc. Virtual Customer Service Agent
Uses Bedrock Converse API with a system prompt to restrict responses
to ABC Inc. products and services only. No financial advice.
"""

import boto3
import json

session = boto3.Session(profile_name="REPLACE-WITH-YOUR-AWS-PROFILE")
bedrock_runtime = session.client("bedrock-runtime", region_name="us-east-1")

MODEL_ID = "us.anthropic.claude-sonnet-4-20250514-v1:0"

products = "savings accounts, checking accounts, credit cards, personal loans, and investment portfolios"
services = "online banking, mobile banking, wire transfers, bill payments, and financial planning consultations"

system_prompt = f"""You are a virtual customer service agent for ABC Inc., a fintech company in the USA.
<rules>
- Only respond to questions related to ABC Inc.'s {products} and {services}.
- If asked about anything else, politely inform the user that you can only assist with ABC Inc.- related inquiries.
- Do not discuss any sensitive financial information or provide financial advice.
- Keep responses concise and professional.
- The company phone number is +100022200
- The company email is abc@example.com
</rules>"""

conversation_history = []


def chat(user_message):
    conversation_history.append({
        "role": "user",
        "content": [{"text": user_message}]
    })

    response = bedrock_runtime.converse(
        modelId=MODEL_ID,
        messages=conversation_history,
        system=[{"text": system_prompt}],
        inferenceConfig={"maxTokens": 512, "temperature": 0.5}
    )

    assistant_message = response["output"]["message"]["content"][0]["text"]
    conversation_history.append({
        "role": "assistant",
        "content": [{"text": assistant_message}]
    })
    return assistant_message


def main():
    print("=" * 60)
    print("ABC Inc. Customer Service Agent (System Prompt Guard)")
    print("Type 'quit' to exit")
    print("=" * 60)

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("quit", "exit"):
            print("Thank you for contacting ABC Inc. Goodbye!")
            break
        if not user_input:
            continue

        try:
            reply = chat(user_input)
            print(f"\nAgent: {reply}")
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()
