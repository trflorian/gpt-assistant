import os
import openai

def setup_opeanai():
    openai.organization = "org-NxrmkQD0vuaMOkyXICvK1vh9"
    openai.api_key = os.getenv("OPENAI_API_KEY")

def get_chat_response(user_request, system_text, chat_history=[]):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_text},
            # TODO insert chat_history
            {"role": "user", "content": user_request},
        ]
    )
    return response['choices'][0]['message']['content']

def main():
    setup_opeanai()

    with open('prompts/system_text_request_type.txt') as f:
        system_text = '\n'.join(f.readlines())

    print('Enter your prompt:')
    request_text = input()

    response = get_chat_response(request_text, system_text)

    print(response)

if __name__ == '__main__':
    main()
