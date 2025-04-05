
# %%
import requests
import json

# %%
corpus_of_documents = [
    "Take a leisurely walk in the park and enjoy the fresh air.",
    "Visit a local museum and discover something new.",
    "Attend a live music concert and feel the rhythm.",
    "Go for a hike and admire the natural scenery.",
    "Have a picnic with friends and share some laughs.",
    "Explore a new cuisine by dining at an ethnic restaurant.",
    "Take a yoga class and stretch your body and mind.",
    "Join a local sports league and enjoy some friendly competition.",
    "Attend a workshop or lecture on a topic you're interested in.",
    "Visit an amusement park and ride the roller coasters."
]

def jaccard_similarity(query, document):
    query = query.lower().split(" ")
    document = document.lower().split(" ")
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))
    return len(intersection)/len(union)


def return_response(query, corpus):
    similarities = []
    for doc in corpus:
        similarity = jaccard_similarity(query, doc)
        similarities.append(similarity)
    return corpus_of_documents[similarities.index(max(similarities))]

# %%

user_input = "I dont like to hike"
relevant_document = return_response(user_input, corpus_of_documents)
full_response = []
prompt = """
You are a bot that makes recommendations for activities. You answer in very short sentences and do not include extra information.
This is the recommended activity: {relevant_document}
The user input is: {user_input}
Compile a recommendation to the user based on the recommended activity and the user input.
"""

# https://github.com/jmorganca/ollama/blob/main/docs/api.md
# %% [generating response from ollama model and streaming the output]
url = 'http://localhost:11434/api/generate'
data = {
    "model": "gemma3:12b",
    "prompt": prompt.format(user_input=user_input, relevant_document=relevant_document),
    "stream": True  # Make sure streaming is enabled
}
headers = {'Content-Type': 'application/json'}
response = requests.post(url, data=json.dumps(data), headers=headers, stream=True)

try:
    print("Generated response: ", end="", flush=True)
    for line in response.iter_lines():
        if line:
            decoded_line = json.loads(line.decode('utf-8'))
            chunk = decoded_line['response']
            print(chunk, end="", flush=True)  # Print each token as it arrives
            full_response.append(chunk)  # Still collect the full response if needed
    print()  # Add a newline at the end
finally:
    response.close()

# If you still need the complete response for later use
complete_response = ''.join(full_response)
