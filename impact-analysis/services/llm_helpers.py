
import openai
import requests
import json

# openai.api_key = "your-api-key"  # Replace or secure via env var
# Define the API endpoint gpt_35_turbo 
url="https://agai-platform-api.dev.int.proquest.com/large-language-models/gpt_4o"

# Define the headers
headers = {
    "Content-Type": "application/json",
    "x-auth-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiV29TIFJlc2VhcmNoIEludGVsbGlnZW5jZSIsImJ1c2luZXNzX2lkIjoxLCJpc3N1ZWRfZGF0ZSI6IjA0LzI0LzIwMjQsIDE0OjU2OjU2In0.djZ8Lukkkl-Do4weZdKPXK6UuwR7JDmieo9bEw1gWg0"
}

def summarize_paper(title, abstract):
    prompt = f"Summarize this paper in plain English:\nTitle: {title}\nAbstract: {abstract}"
    '''response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()'''
    return call_llm(prompt)

def generate_insight_summary(papers):
    titles = "\n".join([p["title"] for p in papers])
    prompt = f"Analyze the following paper titles and summarize key trends in 200 words:\n{titles}"
    '''response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()'''
    return call_llm(prompt)


def call_llm_openai(prompt):   
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def call_llm(prompt):   
    data =  {
            "prompt": prompt,
            "max_tokens": 1000,
            "temperature": 0,
            "num_results": 1,
            "streaming": 0,
            "top_p": 0.9, 
            "top_k": 1
        }
    
    response = requests.post(url, headers=headers, json=data)
    json_object = response.json()
    # Process the response and write to the output file
    if 'results' in json_object:
        result = json_object['results'][0]['completion']
    else:
        result = response.text

    return result