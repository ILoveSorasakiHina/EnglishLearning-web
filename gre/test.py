import openai    

openai.api_key = ''

completion = openai.ChatCompletion.create(
model="gpt-3.5-turbo",
messages=[
        {"role": "teacher", "content": "apple banana lemon orange請就這四個單字出一個克漏字選擇題"}
    ]
)
print(completion)