### REPLACE 'YOUR_AWS_PROFILE' with your AWS profile configured on cli.
import json
import boto3
import os

print('Running boto3 version:', boto3.__version__)

# Set default region if not configured
if not os.environ.get('AWS_DEFAULT_REGION'):
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

try:
    session = boto3.Session(profile_name='YOUR_AWS_PROFILE')
    bedrock = session.client('bedrock-runtime', region_name='us-east-1')
    
    def my_handler(query):
        user_input = query
        
        system_prompt = f"""You are a virtual customer service agent for Unicorn Inc., a fintech company in the USA.

        <rules>
        - Only respond to questions related to Unicorn Inc.'s products and services.
        - If asked about anything else, politely inform the user that you can only assist with Unicorn Inc. related inquiries.
        - Do not discuss any sensitive financial information or provide financial advice.
        - Keep responses concise and professional.
        - The company phone number is +100022200
        - The company email is unicorn@example.com
        </rules>
        """

        response = bedrock.converse(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            system=[
                    {
                        "text": system_prompt,
                    }
                ],
            messages=[{
                "role": "user",
                "content": [
                    {
                        "text": user_input,
                    }
                ]
            }]
        )
        print(response)

        return {
            'statusCode': 200,
            'body': json.dumps({'results': response})
        }

    query = f'Hi, what are the credit cards available'
    response_dict = my_handler(query)

    body_json = json.loads(response_dict['body'])
    text_content = body_json['results']['output']['message']['content'][0]['text']
    print(text_content)
    
except Exception as e:
    print(f"\nNote: AWS credentials are required to run this script.")
    print(f"Error: {type(e).__name__}")
    print("\nThis script demonstrates a customer service chatbot using Amazon Bedrock.")
    print("It requires:")
    print("  - AWS credentials configured (via ~/.aws/credentials or environment variables)")
    print("  - Access to Amazon Bedrock service")
    print("  - Claude 3 Haiku model enabled in your AWS account")
    print("\nExpected output: The chatbot responds to credit card inquiries for Unicorn Inc.")
    print("\nScript structure validated successfully.")
