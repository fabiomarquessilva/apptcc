from transformers import pipeline

# Carregar o modelo gratuito da Hugging Face
print("Carregando o modelo de IA... Isso pode levar alguns segundos.")
chatbot = pipeline("text-generation", model="tiiuae/falcon-7b-instruct")

def gerar_resposta(mensagem):
    """ Gera uma resposta baseada na mensagem do usuário. """
    resposta = chatbot(mensagem, max_length=200, do_sample=True)
    return resposta[0]['generated_text']

# Início do Chatbot
print("\n🤖 Chatbot IA - Digite 'sair' para encerrar\n")

while True:
    usuario = input("Você: ")
    if usuario.lower() == "sair":
        print("Chatbot: Até mais! 👋")
        break
    
    resposta = gerar_resposta(usuario)
    print(f"Chatbot: {resposta}\n")
