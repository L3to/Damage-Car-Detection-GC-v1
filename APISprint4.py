import json
import base64
from google.auth import default
from google.auth.transport.requests import Request
import requests
import os

# 1. Configurações e IDs
ENDPOINT_ID = "" #Seu endpoint
PROJECT_ID = ""  #Seu project id
IMAGE_PATH = "/content/drive/MyDrive/Colab Notebooks/*"  # Caminho da imagem

# Verificar se a imagem é do tipo .webp
if IMAGE_PATH.lower().endswith('.webp'):
    print("Essa imagem não é compatível.")
    exit(1)

# Verificar se o arquivo de imagem existe
if not os.path.isfile(IMAGE_PATH):
    print(f"Erro: Arquivo '{IMAGE_PATH}' não encontrado.")
    exit(1)

# 2. Carregar e codificar a imagem em base64
try:
    with open(IMAGE_PATH, "rb") as image_file:
        image_content = base64.b64encode(image_file.read()).decode("utf-8")
except Exception as e:
    print(f"Erro ao abrir ou ler o arquivo da imagem: {e}")
    exit(1)

# 3. Criar payload JSON
input_data = {
    "instances": [{
        "content": image_content
    }],
    "parameters": {
        "confidenceThreshold": 0.5,
        "maxPredictions": 5
    }
}

# 4. Obter token de autenticação
credentials, project = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
credentials.refresh(Request())
auth_token = credentials.token

# 5. Definir a URL do endpoint
url = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/us-central1/endpoints/{ENDPOINT_ID}:predict"

# 6. Configurar cabeçalhos da solicitação
headers = {
    "Authorization": f"Bearer {auth_token}",
    "Content-Type": "application/json"
}

# 7. Enviar a solicitação
try:
    response = requests.post(url, headers=headers, json=input_data)
except requests.RequestException as e:
    print(f"Erro ao fazer a solicitação HTTP: {e}")
    exit(1)

# 8. Verificar a resposta
if response.status_code == 200:
    predictions = response.json().get("predictions", [])

    if not predictions:
        print("Nenhuma previsão retornada. Verifique a imagem e o modelo.")
    else:
        prediction = predictions[0]

        # Tentar obter os valores de displayNames e confidences com segurança
        display_names = prediction.get('displayNames', [])
        confidences = prediction.get('confidences', [])

        if not display_names or not confidences:
            print("O modelo não conseguiu tratar esta imagem.")
        else:
            display_name = display_names[0]
            confidence = confidences[0]

            # Verificar a confiança da predição
            if confidence < 0.6:
                print("O sistema não pode fazer a previsão com precisão.")
            else:
                # Dicionário de preços
                carros = {
                    "Toyota Corolla": {"Parabrisas": 500, "Compartimento do motor": 1500, "Lateral": 1200, "Capô": 1300, "Parachoque": 700},
                    "Honda Civic": {"Parabrisas": 550, "Compartimento do motor": 1550, "Lateral": 1250, "Capô": 1350, "Parachoque": 750},
                    "Ford Focus": {"Parabrisas": 600, "Compartimento do motor": 1600, "Lateral": 1300, "Capô": 1400, "Parachoque": 800},
                    "Chevrolet Cruze": {"Parabrisas": 650, "Compartimento do motor": 1650, "Lateral": 1350, "Capô": 1450, "Parachoque": 850},
                    "Volkswagen Jetta": {"Parabrisas": 700, "Compartimento do motor": 1700, "Lateral": 1400, "Capô": 1500, "Parachoque": 900},
                    "Nissan Sentra": {"Parabrisas": 620, "Compartimento do motor": 1580, "Lateral": 1320, "Capô": 1420, "Parachoque": 820},
                    "Hyundai Elantra": {"Parabrisas": 640, "Compartimento do motor": 1620, "Lateral": 1380, "Capô": 1520, "Parachoque": 840},
                    "Kia Cerato": {"Parabrisas": 630, "Compartimento do motor": 1590, "Lateral": 1360, "Capô": 1460, "Parachoque": 830},
                    "Renault Kwid": {"Parabrisas": 400, "Compartimento do motor": 1200, "Lateral": 1000, "Capô": 900, "Parachoque": 600},
                    "Fiat Argo": {"Parabrisas": 480, "Compartimento do motor": 1300, "Lateral": 1100, "Capô": 950, "Parachoque": 650},
                    "Peugeot 208": {"Parabrisas": 500, "Compartimento do motor": 1350, "Lateral": 1150, "Capô": 1000, "Parachoque": 700},
                    "Citroën C3": {"Parabrisas": 520, "Compartimento do motor": 1400, "Lateral": 1200, "Capô": 1050, "Parachoque": 720},
                    "Toyota Yaris": {"Parabrisas": 550, "Compartimento do motor": 1450, "Lateral": 1250, "Capô": 1100, "Parachoque": 740},
                    "Honda HR-V": {"Parabrisas": 600, "Compartimento do motor": 1500, "Lateral": 1300, "Capô": 1150, "Parachoque": 800},
                    "Ford EcoSport": {"Parabrisas": 570, "Compartimento do motor": 1480, "Lateral": 1280, "Capô": 1130, "Parachoque": 780},
                    "Chevrolet Tracker": {"Parabrisas": 650, "Compartimento do motor": 1550, "Lateral": 1350, "Capô": 1200, "Parachoque": 820},
                    "Volkswagen T-Cross": {"Parabrisas": 680, "Compartimento do motor": 1600, "Lateral": 1400, "Capô": 1250, "Parachoque": 850},
                    "Hyundai Creta": {"Parabrisas": 700, "Compartimento do motor": 1650, "Lateral": 1450, "Capô": 1300, "Parachoque": 870},
                }
                
                # Dicionário para converter displayNames para português
                partes_em_portugues = {
                    "windshield": "Parabrisas",
                    "engine_compartment": "Compartimento do motor",
                    "lateral": "Lateral",
                    "hood": "Capô",
                    "bumper": "Parachoque"
                }

                # Traduzir displayName para português
                parte_danificada = partes_em_portugues.get(display_name, display_name)

                # Imprimir tabela de preços de forma bonita
                print("\nTabela de Preços de Reparo:")
                print(f"{'Modelo':<30}{'Parte':<30}{'Preço (R$)':<15}")
                print("="*75)
                for carro, precos in carros.items():
                    print(f"{carro:<30}{parte_danificada:<30}{precos.get(parte_danificada, 'N/A'):<15}")

                # Permitir escolha de carro
                carro_escolhido = input("\nEscolha o carro: ")
                if carro_escolhido in carros:
                    preco_reparo = carros[carro_escolhido].get(parte_danificada)

                    if preco_reparo is not None:
                        print(f"\nParte danificada: {parte_danificada.capitalize()}")
                        print(f"Preço do reparo para {carro_escolhido}: R${preco_reparo}")
                    else:
                        print("Parte do carro não encontrada na tabela de preços.")
                else:
                    print("Carro não encontrado na tabela.")
else:
    print(f"Erro na solicitação: {response.status_code} - {response.text}")

print("Resposta do modelo:", response.json())
