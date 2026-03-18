"""
XYZ LLC Email Sensitive Entity Detection
Uses Bedrock Converse API to identify and redact sensitive data elements
from customer service email threads.
"""

import boto3
import os

session = boto3.Session(profile_name="REPLACE-WITH-YOUR-AWS-PROFILE")
bedrock_runtime = session.client("bedrock-runtime", region_name="us-east-1")

MODEL_ID = "us.anthropic.claude-sonnet-4-20250514-v1:0"

# Read the email from file
email_file = os.path.join(os.path.dirname(__file__), "email_sample.txt")
with open(email_file, "r") as f:
    email_text = f.read()

# Example emails for few-shot prompting
email_examples = """
Example 1:
Original Email:
From: John Smith <johns@example.com>
To: support@xyz.com
Subject: Order Inquiry

Hi, my name is John Smith and I need help with my order.

Intent: Order Inquiry
Sensitive Entities: Full Name (John Smith), Email (johns@example.com, support@xyz.com)
"""

# Entities to detect
entities = """
- Full Name (first name, last name, or full name of any person)
- Email Address (any email address found in the email)
- Phone Number (any phone number)
- Account Number (any account or reference number)
- Physical Address (any mailing or street address)
"""

# Template for the user message with placeholders
prompt_template = (
    "## Task\n"
    "You MUST identify SENSITIVE data elements from the E-MAIL provided to you.  \n\n"
    "## Context\n"
    "The email consists of interactions from external customers with customer service "
    "representatives of XYZ, a medical device manufacturer and seller.  \n\n"
    "EXAMPLES: {email_examples} \n\n"
    "ENTITIES: {entities} \n\n"
    "E-MAIL: {email} \n\n\n"
    "## Model Instructions\n"
    "-You MUST use the EXAMPLES provided to arrive at the right intent for a given email.\n"
    "-You MUST use the ENTITIES to find all the sensitive elements of interest in the email.\n"
    "-COUNT the number of exchanges between XYZ customer reps and external customers in the E-MAIL thread.\n"
    "-Replace ALL the sensitive entities from the E-MAIL using *****.  \n\n"
    "## Response Style and Output Format Requirement\n"
    "-You MUST respond in text format.  \n"
    "-In your response, DO NOT start with \"Let me analyze the email and determine the intent\".  \n"
    "-You MUST generate the response with a confidence score (0-100%) based on the CONTEXT and "
    "EXAMPLES provided to you.\n\n"
    "## Success Criteria\n"
    "-Entity detection MUST focus on extracting ALL ENTITIES found in the email\n"
    "-Output text generated MUST replace sensitive ENTITIES with *****"
)

user_message = prompt_template.format(
    email_examples=email_examples,
    entities=entities,
    email=email_text,
)


def detect_sensitive_entities():
    """Send the email to Bedrock for sensitive entity detection and redaction."""
    response = bedrock_runtime.converse(
        modelId=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [{"text": user_message}],
            }
        ],
        inferenceConfig={"maxTokens": 2048, "temperature": 0.0},
    )

    return response["output"]["message"]["content"][0]["text"]


def main():
    print("=" * 60)
    print("XYZ LLC - Email Sensitive Entity Detection")
    print("Using Bedrock Converse API")
    print("=" * 60)

    print(f"\nReading email from: {email_file}")
    print("-" * 60)
    print(email_text)
    print("-" * 60)

    print("\nAnalyzing email for sensitive entities...\n")
    result = detect_sensitive_entities()
    print(result)


if __name__ == "__main__":
    main()
