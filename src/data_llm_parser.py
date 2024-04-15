import os
os.getcwd()
from typing import List
from pydantic import BaseModel, Field
from groq import Groq
import instructor
import json
from src.prompts.prompts import *

ley_path = 'ley.txt'
with open(ley_path, 'r', encoding='utf-8') as file:
    ley_contents = "<input> \n " + file.read() + " \n </input>"

print(ley_contents)

class outputParsedJSON(BaseModel):
    output_json: dict

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

client = instructor.from_groq(client, mode=instructor.Mode.JSON)

resp = client.chat.completions.create(
    model="mixtral-8x7b-32768",
    messages=[
        {
            "role": "user",
            "content": prompt_INIT + prompt_TEXT + prompt_EXPLANATION + prompt_EXAMPLES + prompt_DoNOTs + prompt_TXT + ley_contents + prompt_FINAL,
            
        }
    ],
    response_model=outputParsedJSON
    
)

# try to improve mixtral output with messaging formatting. 
#messages = [
    #{
        #"role": "system",
        #"content": "Sos un asistente legal útil que reponde SIN EMITIR JUICIO DE SI UN CAMBIO ES BUENO O MALO, MEJOR O PEOR. Al dar tu respuesta, tenes que tener en cuenta y utilizar el contexto proporcionado para dar una respuesta INTEGRAL, INFORMATIVA, PRECISA y OBJETIVA a la pregunta del usuario.",
    #},
    #{"role": "system", "content": "A continuación se proporciona el contexto:"},
    #{"role": "system", "content": str(context_preprocessed)},
    #{
        #"role": "system",
        #"content": "A continuación se proporciona la pregunta del usuario:",
    #},
    #{"role": "user", "content": query},
#]



print(resp)


with open('parsed_output_mixtral.json', 'w', encoding='utf-8') as file:
    json.dump(resp.output_json, file, ensure_ascii=False, indent=4)


from openai import OpenAI

client = OpenAI()

messages = [
     {
          "role": "system", "content": prompt_INIT + prompt_TEXT + prompt_EXPLANATION + prompt_EXAMPLES + prompt_DoNOTs + prompt_TXT + ley_contents + prompt_FINAL
     }
]

completion = client.chat.completions.create(
    model='gpt-4-1106-preview',
    messages=messages,
    temperature=0.5,
    max_tokens=4096,
    stream=False,
)



answer = completion.choices[0].message.content

with open('parsed_output_openai.json', 'w') as file:
    file.write(answer)


















#resp.model_fields
#resp.model_json_schema()

#resp.resumen




#resp.articulo





