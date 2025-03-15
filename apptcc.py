import streamlit as st
import openai
import os
import time

# Configura a chave da API do OpenAI a partir de uma variável de ambiente.
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_tcc(theme, databases=""):
    """
    Gera o TCC utilizando a API do OpenAI (ChatGPT) a partir do tema e das bases de dados (opcional).
    
    Parâmetros:
    - theme: tema do TCC informado pelo usuário.
    - databases: string com as bases de dados (separadas por vírgula) para fundamentação (opcional).
    
    Retorna:
    - O texto gerado do TCC ou None em caso de erro.
    """
    prompt = (
        f"Você é um assistente acadêmico e especialista em elaboração de TCCs. "
        f"A partir do tema \"{theme}\", elabore um Trabalho de Conclusão de Curso completo, "
        f"que contenha os seguintes capítulos:\n"
        f"1. Introdução\n"
        f"2. Revisão de Literatura\n"
        f"3. Metodologia\n"
        f"4. Desenvolvimento\n"
        f"5. Conclusões\n"
        f"6. Referências Bibliográficas\n\n"
        f"Se o usuário forneceu bases de dados, utilize-as para referenciar e fundamentar as informações. "
        f"Bases de dados: {databases}. Caso contrário, utilize as principais bases acadêmicas de sua escolha.\n\n"
        f"O trabalho deve ser original, bem estruturado e seguir as normas acadêmicas. "
        f"Formate o texto com títulos e subtítulos de forma clara."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # ou "gpt-4" se disponível e desejado
            messages=[
                {"role": "system", "content": "Você é um assistente acadêmico."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500,
            n=1
        )
        # Acessa o conteúdo da resposta
        tcc_text = response.choices[0].message['content']
        return tcc_text
    except Exception as e:
        st.error(f"Erro ao gerar o TCC: {e}")
        return None

def main():
    st.title("Gerador Automático de TCC")
    st.markdown("""
    ### Bem-vindo ao Gerador Automático de TCC!
    
    Este aplicativo utiliza a API do ChatGPT para gerar um TCC completo a partir do tema informado.
    Informe o tema do seu TCC e, opcionalmente, as bases de dados que deseja utilizar para a pesquisa.
    """)
    
    # Entrada de dados
    theme = st.text_input("Informe o tema do TCC:")
    databases = st.text_input("Bases de dados (opcional, separe por vírgula):")
    
    if st.button("Gerar TCC"):
        if not theme.strip():
            st.error("Por favor, informe um tema para o TCC.")
        else:
            with st.spinner("Gerando TCC, por favor aguarde..."):
                tcc_result = generate_tcc(theme, databases)
                # Simula um pequeno tempo extra para feedback visual
                time.sleep(1)
            if tcc_result:
                st.success("TCC gerado com sucesso!")
                st.markdown("### Seu TCC:")
                st.text_area("TCC Gerado:", value=tcc_result, height=600)
                st.download_button(
                    label="Baixar TCC como .txt",
                    data=tcc_result,
                    file_name="TCC.txt",
                    mime="text/plain"
                )
            else:
                st.error("Não foi possível gerar o TCC. Tente novamente.")

if __name__ == "__main__":
    if openai.api_key is None:
        st.error("A chave da API do OpenAI não foi definida. Configure a variável de ambiente OPENAI_API_KEY.")
    else:
        main()
