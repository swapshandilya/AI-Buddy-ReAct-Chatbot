from groq import Groq
import os

client = Groq(
    api_key=os.getenv('GROQ_API_KEY')
)


# model_id = { 
#     llama31 : 'llama-3.1-405b-reasoning',
#     llama3 : "llama3-8b-8192"
# }

class Agent:

    def __init__(self, sys_prom=""):
        self.messages = []
        self.system = sys_prom

        if(self.system):
            self.messages.append({"role":"system" , "content":self.system})

    def __call__(self,message):
        self.messages.append({"role":"user" , "content":message})
        result = self.execute()
        self.messages.append({"role":"assistant", "content":result})
        return result

    def execute(self):
        chat_completion = client.chat.completions.create(
        messages=self.messages,
        model="llama3-8b-8192",
        )

        response = chat_completion.choices[0].message.content

        return response
