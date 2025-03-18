# from src.orchestrator.orchestrator import ami_graph
# from pprint import pprint
# from langchain_core.messages import HumanMessage
# from datetime import datetime
# import pandas as pd
# import time
# import asyncio
# import os
# import json
# import ast

# async def mem_inference():
#     # Specify a thread
#     user_id = input("USER ID : ")
#     thread_id = input("THREAD ID : ")
#     config = {"recursion_limit": 10, "configurable": {"thread_id": thread_id, "user_id": user_id}}
#     while True:
#     # Specify an input
#         question = input("ASK QUESTION : ")

#         messages = [HumanMessage(content=question)]

#         # Run
#         messages = await ami_graph.invoke({"messages": messages},config)
#         for m in messages['messages']:
#             m.pretty_print()

# async def test_inference():
#     user_id = input("USER ID : ")
#     thread_id = input("THREAD ID : ")
#     COLORS = {
#         "green": "\033[32m",
#         "yellow": "\033[33m",
#         "magenta": "\033[35m",
#         "blue": "\033[34m",
#         "reset": "\033[0m",
#     }

#     while True:
#         # question = question_list[q]
#         metadata = {
#             'user_id' : None,
#             'session_id' : None,
#             'question' : None,
#             'intent': None,
#             'plan' : None,
#             'response' : None,
#             'tool_calls' : [],
#             'output_time' : None,
#             'timestamp' : None
#         }

#         metadata['user_id'] = user_id
#         metadata['session_id'] = thread_id

#         config = {"recursion_limit": 10, "configurable": {"thread_id": thread_id, "user_id": user_id}}
#         question = input("ASK QUESTION : ")
#         temp_question = {
#             "question": question
#         }
#         with open("temp_question.json", "w") as file:
#             json.dump(temp_question, file)
#         color_code = COLORS.get("magenta", COLORS["magenta"])
#         formatted_message = f"{color_code}{question}{COLORS['magenta']}"
#         print(formatted_message, '\n')
#         metadata['question'] = question
    
#         mes = {"messages": [{"role": "user", "content": question}]}
#         async for event in ami_graph.astream(mes, config=config, stream_mode="updates"):
#             for key, value in event.items():
#                 if key != "__end__":
#                     # print(key , value)
#                     if key == 'intent_elaborator':
#                         metadata['intent'] = value['messages']
#                         color_code = COLORS.get("green", COLORS["green"])
#                         formatted_message = f"{color_code}{value['messages']}{COLORS['green']}"
#                         print(formatted_message, '\n')                    
#                     if key == 'task_decomposer':
#                         metadata['plan'] = value['messages']
#                         color_code = COLORS.get("magenta", COLORS["magenta"])
#                         formatted_message = f"{color_code}{value['messages']}{COLORS['magenta']}"
#                         print(formatted_message, '\n')
#                     if key == 'response_generator':
#                         metadata['response'] = value['messages']
#                         print(len(value['messages']))
#                         color_code = COLORS.get("blue", COLORS["blue"])
#                         formatted_message = f"{color_code}{value['messages']}{COLORS['blue']}"
#                         print(formatted_message, '\n')

#         # extract answer
#         ans = metadata['response'][0].split("AIMessage(content=")
#         # print(ans)
#         ans = ans[-1].split(", additional_kwargs=")[0]
        
#         answer = f"Final Answer: {ans}"
#         color_code = COLORS.get("yellow", COLORS["yellow"])
#         formatted_message = f"{color_code}{answer}{COLORS['yellow']}"
#         print(formatted_message, '\n')
                

        

#     # pass
# if __name__ == "__main__":
#     # asyncio.run(mem_inference())

#     asyncio.run(test_inference())
#     # asyncio.run(mem_inf())

#     # asyncio.run(memory_inference())
#     # run()
#     # test()

# import streamlit as st
# import asyncio
# import json
# from src.orchestrator.orchestrator import ami_graph

# # Hardcoded user_id and thread_id
# USER_ID = "12345"
# THREAD_ID = "67890"

# # Streamlit UI
# st.title("AI Question Answering System")
# st.write(f"User ID: {USER_ID}, Thread ID: {THREAD_ID}")

# # Input box for user question
# question = st.text_input("Ask a Question:")

# # Output display placeholders
# intent_placeholder = st.empty()
# plan_placeholder = st.empty()
# response_placeholder = st.empty()
# final_answer_placeholder = st.empty()

# async def get_answer(question):
#     COLORS = {
#         "green": "\033[32m",
#         "yellow": "\033[33m",
#         "magenta": "\033[35m",
#         "blue": "\033[34m",
#         "reset": "\033[0m",
#     }
#     metadata = {
#         'user_id': USER_ID,
#         'session_id': THREAD_ID,
#         'question': question,
#         'intent': None,
#         'plan': None,
#         'response': None,
#         'tool_calls': [],
#         'output_time': None,
#         'timestamp': None
#     }
#     config = {"recursion_limit": 10, "configurable": {"thread_id": THREAD_ID, "user_id": USER_ID}}
    
#     mes = {"messages": [{"role": "user", "content": question}]}
#     async for event in ami_graph.astream(mes, config=config, stream_mode="updates"):
#         for key, value in event.items():
#             if key != "__end__":
#                 if key == 'response_generator':
#                     metadata['response'] = value['messages']
#                     # response_placeholder.write(f"**Response:** {value['messages']}")
    
#     # Extract final answer
#     ans = metadata['response'][0].split("AIMessage(content=")[-1].split(", additional_kwargs=")[0]
#     final_answer_placeholder.write(f"**Final Answer:** {ans}")

# # When the user inputs a question, trigger inference
# if st.button("Get Answer") and question:
#     asyncio.run(get_answer(question))


import streamlit as st
import asyncio
import json
import random
import time
from src.orchestrator.orchestrator import historia

# Function to generate a random user_id and thread_id
def generate_ids():
    return str(random.randint(10000, 99999)), str(random.randint(10000, 99999))

# Initialize session state
if "user_id" not in st.session_state:
    st.session_state["user_id"], st.session_state["thread_id"] = generate_ids()
    st.session_state["last_update"] = time.time()

# Update User ID and Thread ID every 8 minutes (480 seconds)
if time.time() - st.session_state["last_update"] > 480:
    st.session_state["user_id"], st.session_state["thread_id"] = generate_ids()
    st.session_state["last_update"] = time.time()

# Streamlit UI
st.title("Historia AI")
st.write("**Hey, I am Historia, a historical agent AI. You can ask anything around it.**")

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(f"<pre style='font-family: monospace; white-space: pre-wrap;'>{message['content']}</pre>", unsafe_allow_html=True)

# Input box for user question
question = st.chat_input("Ask a question...")

async def chat_response(question):
    config = {"recursion_limit": 10, "configurable": {"thread_id": st.session_state["thread_id"], "user_id": st.session_state["user_id"]}}
    
    mes = {"messages": [{"role": "user", "content": question}]}
    
    with st.chat_message("user"):
        st.markdown(f"<pre style='font-family: monospace; white-space: pre-wrap;'>{question}</pre>", unsafe_allow_html=True)
    
    st.session_state["messages"].append({"role": "user", "content": question})
    
    response_text = ""
    with st.chat_message("assistant"):
        response_container = st.empty()
        async for event in historia.astream(mes, config=config, stream_mode="updates"):
            for key, value in event.items():
                if key != "__end__":
                    if key == 'response_generator':
                        ans = value['messages'][0].split("AIMessage(content=")[-1].split(", additional_kwargs=")[0]
                        for chunk in ans.split():  # Ensure proper word spacing
                            response_text += chunk + " "  # Append streamed chunks
                            response_container.markdown(f"<pre style='font-family: monospace; white-space: pre-wrap;'>{response_text}</pre>", unsafe_allow_html=True)  # Update in real-time
    
    st.session_state["messages"].append({"role": "assistant", "content": response_text})

# When the user inputs a question, trigger inference
if question:
    asyncio.run(chat_response(question))


