import re
import textwrap
from time import time, sleep
from quickstart import getFileContent
import openai
from load_key_from_config import getConfigKey

summary_keywords = ['summarize', 'summary', 'research paper']

def processSummaryRequest(text):
    link_regex = r"https://drive\.google\.com/file/d/\S+"

    link = re.search(link_regex, text).group()
    return getFileandSummarize(link)

openai.api_key = getConfigKey('opanaiAPI')

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def gpt3_completion(prompt, engine='text-davinci-002', temp=0.6, top_p=1.0, tokens=2000, freq_pen=0.25, pres_pen=0.0, stop=['<<END>>']):
    max_retry = 5
    retry = 0
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            text = re.sub('\s+', ' ', text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            # print('Error communicating with OpenAI:', oops)
            sleep(1)    

def getFileandSummarize(query):
    
    fileContent = getFileContent(query)

    chunks = textwrap.wrap(fileContent, 4000)

    result = list()
    count = 0
    for chunk in chunks:
        count = count + 1
        prompt = open_file('Database/prompt.txt').replace('<<SUMMARY>>', chunk)
        prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
        summary = gpt3_completion(prompt)
        # print('\n\n\n', count, 'of', len(chunks), ' - ', summary)
        result.append(summary)
    summarized_result = '\n\n'.join(result)
    if(len(summarized_result) < 20):
        return "An error Occured. Please Try Again. Check Authentications"
    else:
        return summarized_result
     
# file_link = 'https://drive.google.com/file/d/1q9SW1aM7igJafLuvgY1JUMtfD7uyA4ZX/view?usp=share_link'
# print(getFileandSummarize(file_link))
    