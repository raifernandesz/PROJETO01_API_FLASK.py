from flask import Flask, jsonify, request
import threading
import requests
import time

app = Flask(__name__)

# -------------------------
# "Banco de dados" em memória
# -------------------------
alunos = [
    {"id": 1, "nome": "Clara", "idade": 20},
    {"id": 2, "nome": "Bianca", "idade": 18}
]

# -------------------------
# ROTAS DA API
# -------------------------

@app.route("/")
def home():
    return "📚 API de Alunos funcionando com sucesso!!!"

# GET - Listar todos os alunos
@app.route("/alunos", methods=["GET"])
def listar_alunos():
    return jsonify(alunos)

# POST - Adicionar aluno
@app.route("/alunos", methods=["POST"])
def adicionar_aluno():
    novo_aluno = request.get_json()
    alunos.append(novo_aluno)
    return jsonify({"mensagem": "Aluno adicionado com sucesso!", "aluno": novo_aluno}), 201

# PUT - Atualizar aluno pelo ID
@app.route("/alunos/<int:id>", methods=["PUT"])
def atualizar_aluno(id):
    for aluno in alunos:
        if aluno["id"] == id:
            dados = request.get_json()
            aluno.update(dados)
            return jsonify({"mensagem": "Aluno atualizado!", "aluno": aluno})
    return jsonify({"erro": "Aluno não encontrado!"}), 404

# DELETE - Remover aluno pelo ID
@app.route("/alunos/<int:id>", methods=["DELETE"])
def deletar_aluno(id):
    for aluno in alunos:
        if aluno["id"] == id:
            alunos.remove(aluno)
            return jsonify({"mensagem": "Aluno removido com sucesso!"})
    return jsonify({"erro": "Aluno não encontrado!"}), 404

# -------------------------
# MENU DE TERMINAL
# -------------------------

API_URL = "http://127.0.0.1:5000/alunos&quot;"

def menu():
    time.sleep(1)  # espera a API subir
    while True:
        print("\n===== 📚 MENU API DE ALUNOS =====")
        print("1 - Listar alunos")
        print("2 - Adicionar aluno")
        print("3 - Atualizar aluno")
        print("4 - Remover aluno")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            resposta = requests.get(API_URL)
            print("\nAlunos cadastrados:", resposta.json())

        elif opcao == "2":
            id = int(input("ID: "))
            nome = input("Nome: ")
            idade = int(input("Idade: "))
            novo_aluno = {"id": id, "nome": nome, "idade": idade}
            resposta = requests.post(API_URL, json=novo_aluno)
            print(resposta.json())

        elif opcao == "3":
            id = int(input("ID do aluno a atualizar: "))
            nome = input("Novo nome (ou Enter p/ manter): ")
            idade = input("Nova idade (ou Enter p/ manter): ")
            dados = {}
            if nome: dados["nome"] = nome
            if idade: dados["idade"] = int(idade)
            resposta = requests.put(f"{API_URL}/{id}", json=dados)
            print(resposta.json())

        elif opcao == "4":
            id = int(input("ID do aluno a remover: "))
            resposta = requests.delete(f"{API_URL}/{id}")
            print(resposta.json())

        elif opcao == "0":
            print("👋 Encerrando menu...")
            break
        else:
            print("⚠️ Opção inválida! Tente novamente.")

# -------------------------
# EXECUÇÃO
# -------------------------

if __name__ == "__main__":
    # Inicia a API em thread separada
    t = threading.Thread(target=lambda: app.run(debug=False, use_reloader=False))
    t.daemon = True
    t.start()

    # Executa o menu no terminal
    menu()
