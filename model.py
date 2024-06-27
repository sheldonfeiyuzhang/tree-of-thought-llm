import os
import openai
import ollama
import backoff 

completion_tokens = prompt_tokens = 0

api_key = os.getenv("OPENAI_API_KEY", "")
if api_key != "":
    openai.api_key = api_key
else:
    print("Warning: OPENAI_API_KEY is not set")
    
api_base = os.getenv("OPENAI_API_BASE", "")
if api_base != "":
    print("Warning: OPENAI_API_BASE is set to {}".format(api_base))
    openai.api_base = api_base

@backoff.on_exception(backoff.expo, openai.error.OpenAIError)
def completions_with_backoff(**kwargs):
    
    #return openai.ChatCompletion.create(**kwargs)
    return ollama.chat(**kwargs)

def gpt(prompt, model="llama2", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
    messages = [{"role": "user", "content": prompt}]
    return chatgpt(messages, model=model, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop)
    

def ollama_chat(messages, model="llama2", temperature=0.7, max_tokens=1000,stop=None):
    response=completions_with_backoff(model=model, messages=messages, options={'temperature':temperature, "num_predict":max_tokens,'stop':stop,}, )
    return response

def chatgpt(messages, model="llama2", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
    global completion_tokens, prompt_tokens
    outputs = []
    while n > 0:
        cnt = min(n, 20)
        n -= cnt
        #res = completions_with_backoff(model=model, messages=messages, options={'temperature':temperature, "num_predict":max_tokens,'stop':stop,}, n=cnt, )
        #outputs.extend([choice["message"]["content"] for choice in res["choices"]])
        for _ in range(cnt):
            print(cnt,messages)
            res=ollama_chat(messages=messages, model=model, temperature=temperature, max_tokens=max_tokens,stop=stop)
            txt=str(res['message']["content"])
            print(txt)
            outputs.append(txt)
        # log completion tokens
        completion_tokens += res['eval_count']
        prompt_tokens += 0
    return outputs
    
def gpt_usage(backend="gpt-4"):
    global completion_tokens, prompt_tokens
    if backend == "gpt-4":
        cost = completion_tokens / 1000 * 0.06 + prompt_tokens / 1000 * 0.03
    elif backend == "gpt-3.5-turbo":
        cost = completion_tokens / 1000 * 0.002 + prompt_tokens / 1000 * 0.0015
    elif backend == 'llama3':
        cost = completion_tokens / 1000 * 0 + prompt_tokens / 1000 * 0
    elif backend == 'llama2':
        cost = completion_tokens / 1000 * 0 + prompt_tokens / 1000 * 0

    return {"completion_tokens": completion_tokens, "prompt_tokens": prompt_tokens, "cost": cost}

def model_checker():
    print('llm ready')


if __name__== '__main__':
    #response = gpt(prompt="Tell me a joke.")
    #print(response)
    response=gpt(prompt="12+12=", n=1, stop=None)
    print(response)
    print(completion_tokens)
    #print(prompt_tokens)