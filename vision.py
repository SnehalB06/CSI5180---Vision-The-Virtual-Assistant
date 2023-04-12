import time
import openai
import gradio as gr
from load_key_from_config import getConfigKey
from ner_test import getNER
from weather import weather_keyword_list, getWeather
from stocks import stock_keyword_list, getStocks
from oc_transpo_bus import bus_keyword, processBusRequest
from news import news_keywords_list, processNewsRequest
from google_drive_load_file import summary_keywords, processSummaryRequest


openai.api_key = getConfigKey("opanaiAPI")

messages = [{"role": "system", "content": "You are a virtual assistant chatbot. Your name is Vision. You will help users with general queries."}]


def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})

    tokens = getNER(user_input)

    if any(word in user_input for word in weather_keyword_list):
        gpe_entities = [ent.text for ent in tokens if ent.label_ == 'GPE']
        if gpe_entities:
            chat_response = getWeather(gpe_entities[0])
    
    elif any(word in user_input for word in stock_keyword_list):
        org_entities = [ent.text for ent in tokens if ent.label_ == 'ORG']
        if org_entities:
            chat_response = getStocks(org_entities[0])

    elif any(word in user_input for word in bus_keyword):
        chat_response = processBusRequest(user_input)
    
    elif any(word in user_input for word in news_keywords_list):
        chat_response = processNewsRequest(user_input)
    
    elif any(word in user_input for word in summary_keywords):
        chat_response = processSummaryRequest(user_input)

    else:
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = messages
        )   
        chat_response = response["choices"][0]["message"]["content"]

    messages.append({"role": "assistant", "content": chat_response})
    return chat_response

demo = gr.Interface(fn=CustomChatGPT, inputs = "text", outputs = "text", title = "Vision - The Virtual Assistant")
demo.launch()
# demo.launch(share=True)