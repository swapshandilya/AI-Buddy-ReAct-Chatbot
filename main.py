import prompt as pt 
import requests
import agents
import functions as fn
import re
import streamlit as st


def invoke_agent(sys_prom , question, tools, timeout):

    skkit = agents.Agent(sys_prom)

    # reg_action = re.compile(r'Action:\s*(\w+):\s*(.*)', re.DOTALL)
    reg_action= re.compile('^Action: (\w+): (.*)$')

    i=0
    nex=question

    while (i< timeout):
        i+=1

        result = skkit(nex)
        # print(result)
        st.write(result)
        st.write('\n')


        actions = [reg_action.match(a) for a in result.split('\n') if reg_action.match(a)]

        if(actions):

            action, para = actions[0].groups()
            # print('action=>', action)

            if action not in tools:
                raise Exception("Unknown action: {}: {}".format(action, para))

            if(action=="run_code"):
                
                match = re.search(r'```Python-exe\n(.*?)```', result, re.DOTALL)
                if match:
                    code = match.group(1).strip()
                    # print(f'Captured Code:\n{code}')
                    result = fn.run_code(code)

                observation = result
                
            else:
                observation = tools[action](para)

            # print(f'Observation1: {observation}')
            nex = f'Observation: {observation}'
            st.write(f'Observation: {observation}')
        else: 
            return 
      
        

    return 

sys_prom=pt.get_system_prompt()


# question = "Run a python code for finding largest number in an array. Take an example array yourself. Also verify if the code is wrong, give it a thought and correct it again."
# question = "Who won bronze medal in hockey in olympics 2024?"
# question = "What is 5 multiplied by 400 added to 2?"


# Streamlit app

# Streamlit Interface
st.title("Hi, I'm Skkit—your AI Buddy!")

# System prompt and question input
question = st.text_input("Tell me!")

# Timeout and tool selection
timeout = st.slider("Timeout", 1, 30, 5)
tools = {
    "search_web": fn.search_web,
    "calculate": fn.calculate,
    "run_code": fn.run_code
}

if st.button("Run Agent"):
    if sys_prom and question:
        invoke_agent(sys_prom, question, tools, timeout)
    else:
        st.warning("Please provide both a system prompt and a question.")
