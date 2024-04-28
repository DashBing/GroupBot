#!/bin/python3

import sys
from gradio_client import Client

client = Client("https://qwen-qwen1-5-72b-chat.hf.space/--replicas/3kh1x/")
result = client.predict(
		"Hello!!",	# str  in 'Input' Textbox component
    [["Hello!",sys.argv[1]]],	# Tuple[str | Dict(file: filepath, alt_text: str | None) | None, str | Dict(file: filepath, alt_text: str | None) | None]  in 'Qwen1.5-72B-Chat' Chatbot component
    "Hello!!",	# str  in 'parameter_9' Textbox component
		api_name="/model_chat"
)
print(result[1][1][1])
