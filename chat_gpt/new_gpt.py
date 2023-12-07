import openai


async def generate_response(client: openai.Client, message_history: list):
    with open("./chat_gpt/api_key.txt", "r") as f:
        openai.api_key = f.read().strip('\n')

    response = await client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=message_history,
        temperature=0)
