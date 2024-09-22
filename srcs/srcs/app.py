import openai
import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
# Função para buscar um modelo de contrato genérico
def buscar_modelo_contrato(tipo_contrato):
    # Aqui, você pode usar uma base de dados local ou uma API para buscar o modelo
    modelos = {
        "compra_venda": "Contrato de Compra e Venda: [modelo básico]",
        "prestacao_servicos": "Contrato de Prestação de Serviços: [modelo básico]",
        "locacao": "Contrato de Locação: [modelo básico]"
    }
    return modelos.get(tipo_contrato, "Modelo de contrato não encontrado.")

# Função para gerar contrato personalizado
def gerar_contrato_personalizado(tipo_contrato, detalhes):
    modelo_base = buscar_modelo_contrato(tipo_contrato)
    sistema_prompt = "Você é um assistente jurídico especializado na criação de contratos."
    user_prompt = f"{sistema_prompt}\n\nO usuário deseja um contrato de {tipo_contrato}. Ele forneceu os seguintes detalhes: {detalhes}. Baseado no modelo: {modelo_base}, gere um contrato completo e adicione cláusulas específicas conforme necessário."
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        contents=[
            {"role": "user", "parts": [{"text": user_prompt}]}
        ],
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=2000,
            temperature=0.3,
        )
    )
    return response.text

# Interface Streamlit
st.title("Gerador de Contratos Personalizados")

tipo_contrato = st.selectbox("Selecione o tipo de contrato:", ["compra_venda", "prestacao_servicos", "locacao"])
detalhes = st.text_area("Forneça os detalhes do contrato (nomes, valores, prazos, etc.):")

if st.button("Gerar Contrato"):
    if detalhes:
        contrato = gerar_contrato_personalizado(tipo_contrato, detalhes)
        st.write("Contrato Gerado:")
        st.text_area("", contrato, height=500)
    else:
        st.write("Por favor, insira os detalhes do contrato.")

