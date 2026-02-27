import boto3
brt = boto3.client("bedrock-runtime")

test_question = "Given the list of numbers [2, 3, 4, 5, 6], find all unique pairs whose sum is a prime number. Show your reasoning process."

# Interleaved Thinking System Prompt
interleaved_system_prompt = (
    "You are an AI agent that alternates between thinking and acting. "
    "For each step: reason about which numbers might form pairs, simulate checking their sums, observe whether the sum is prime, and repeat until all pairs are considered. "
    "Present the answer at the end."
)
interleaved_conversation = [
    {"role": "user", "content": [{"text": test_question}]}
]
interleaved_response = brt.converse(
    modelId="amazon.nova-pro-v1:0",
    messages=interleaved_conversation,
    system=[{"text": interleaved_system_prompt}],
    inferenceConfig={"maxTokens": 1000}
)
print("Interleaved Thinking Output:\n", interleaved_response["output"]["message"]["content"][0]["text"])

# Recursive Reasoning System Prompt
recursive_system_prompt = (
    "You are an AI agent that recursively breaks problems into smaller subproblems. "
    "For each pair, calculate the sum, check if it is prime, and if not, move to the next pair. "
    "Continue recursively until all pairs are tested, then list those whose sums are prime."
)
recursive_conversation = [
    {"role": "user", "content": [{"text": test_question}]}
]
recursive_response = brt.converse(
    modelId="amazon.nova-pro-v1:0",
    messages=recursive_conversation,
    system=[{"text": recursive_system_prompt}],
    inferenceConfig={"maxTokens": 1000}
)
print("Recursive Reasoning Output:\n", recursive_response["output"]["message"]["content"][0]["text"])

# Multistage Reasoning System Prompt
multistage_system_prompt = (
    "You are an AI agent that solves problems in clearly defined stages. "
    "Stage 1: List all possible pairs from the given numbers. "
    "Stage 2: For each pair, calculate their sum. "
    "Stage 3: Check which sums are prime numbers. "
    "Stage 4: Present the pairs whose sums are prime."
)
multistage_conversation = [
    {"role": "user", "content": [{"text": test_question}]}
]
multistage_response = brt.converse(
    modelId="amazon.nova-pro-v1:0",
    messages=multistage_conversation,
    system=[{"text": multistage_system_prompt}],
    inferenceConfig={"maxTokens": 1000}
)
print("Multistage Reasoning Output:\n", multistage_response["output"]["message"]["content"][0]["text"])
