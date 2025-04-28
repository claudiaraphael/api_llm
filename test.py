from fastapi import FastAPI, Depends, HTTPException, Header
import os
import ollama
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
api_key = os.getenv("API_KEY")

# Middleware to check for API key
def verify_api_key(x_api_key: str = Header(None)):
    credits = API_KEY_CREDITS.get(x_api_key, 0)

    if credits <= 0:
        raise HTTPException(status_code=401, detail="Invalid API Key, or no credits")
    return x_api_key


#############################################################
# Entendendo a função:
# A função `verify_api_key` é um middleware que verifica se a chave de API fornecida no cabeçalho da solicitação é válida.
# Se a chave não for válida ou se os créditos associados a ela forem zero ou negativos, a função lança uma exceção HTTP 401 (não autorizado). Caso contrário, a função retorna a chave de API.
# Essa função é usada para proteger rotas da API, garantindo que apenas usuários com uma chave de API válida possam acessar os recursos.
#############################################################

# Função para verificar o número de créditos
def verify_api_key(x_api_key: str = Header(None)):   
    
    # Verifica se a chave de API está presente no dicionário
    credits = API_KEY_CREDITS.get(x_api_key,0)
    
    if credits <= 0:
        # Se não houver créditos, lança uma exceção HTTP 401
        raise HTTPException(status_code=401, detail="Invalid API Key, or no credits")
    
    # Retorna a chave de API se for válida
    return x_api_key

# Endpoint for generating responses using the Mistral model.
@app.post("/generate")


# Function to generate a response using the Mistral model
def generate(prompt: str, x_api_key: str = Depends(verify_api_key)):
    # The number of credits for the API key is decremented by 1 after each request.
    API_KEY_CREDITS[x_api_key] -= 1

    # Generate a response using the Mistral model from the Ollama library.
    # The ollama.chat function is called with the model name and the user's prompt.
    # The response is returned in JSON format.
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return {"response": response["message"]["content"]}



