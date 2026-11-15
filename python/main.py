# ELOS - cadastros iniciais
# Dados usados apenas durante a execução do programa.

bairros = [
    {"nome": "Itaquera", "indice": 0.30},
    {"nome": "Guaianases", "indice": 0.60},
    {"nome": "Cidade Tiradentes", "indice": 0.90}
]

# Os índices acima são exemplos de teste, não dados oficiais.

demandas = []
ofertas = []


def ler_texto(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto != "":
            return texto
        print("Esse campo não pode ficar vazio.")


def ler_inteiro(mensagem, minimo):
    while True:
        try:
            numero = int(input(mensagem))
            if numero >= minimo:
                return numero
            print("O número deve ser maior ou igual a", minimo)
        except ValueError:
            print("Digite um número inteiro válido.")


def ler_preco(mensagem):
    while True:
        try:
            preco = float(input(mensagem).replace(",", "."))
            if 0 < preco < 1000000:
                return preco
            print("Digite um preço maior que zero.")
        except ValueError:
            print("Digite um preço válido.")


def escolher_bairro():
    while True:
        print("\nBairros:")
        for i in range(len(bairros)):
            print(i + 1, "-", bairros[i]["nome"])

        escolha = ler_inteiro("Escolha o bairro: ", 1)
        if escolha <= len(bairros):
            return bairros[escolha - 1]
        print("Bairro inválido.")


def cadastrar_demanda():
    print("\nCADASTRO DE DEMANDA")
    comerciante = ler_texto("Nome do comércio: ")
    produto = ler_texto("Produto: ").lower()
    caixas = ler_inteiro("Quantidade de caixas: ", 1)
    bairro = escolher_bairro()

    demanda = {
        "id": len(demandas) + 1,
        "comerciante": comerciante,
        "produto": produto,
        "caixas": caixas,
        "bairro": bairro["nome"],
        "indice": bairro["indice"],
        "status": "ABERTA"
    }

    demandas.append(demanda)
    print("Demanda", demanda["id"], "cadastrada com sucesso!")


def cadastrar_oferta():
    print("\nCADASTRO DE OFERTA")
    fornecedor = ler_texto("Nome do fornecedor: ")
    produto = ler_texto("Produto: ").lower()

    print("1 - Venda")
    print("2 - Doação")
    tipo = input("Tipo de oferta: ").strip()

    if tipo == "2":
        print("Doações não são aceitas no sistema B2B.")
        return
    elif tipo != "1":
        print("Tipo de oferta inválido.")
        return

    caixas = ler_inteiro("Quantidade de caixas: ", 1)
    dias = ler_inteiro("Dias restantes de validade: ", 0)

    if dias < 3:
        print("Oferta recusada: validade menor que 3 dias.")
        return
    elif dias <= 5:
        categoria = "Liquidação Rápida"
    else:
        categoria = "Comercialização Padrão"

    preco_normal = ler_preco("Preço regular por caixa: R$ ")
    preco_oferta = ler_preco("Preço ofertado por caixa: R$ ")

    if categoria == "Liquidação Rápida":
        if preco_oferta < 2:
            print("Oferta recusada: preço abaixo da comissão simulada de R$ 2,00.")
            return
        elif preco_oferta >= preco_normal:
            print("Oferta recusada: liquidação precisa custar menos que o preço regular.")
            return

    oferta = {
        "id": len(ofertas) + 1,
        "fornecedor": fornecedor,
        "produto": produto,
        "caixas": caixas,
        "dias": dias,
        "categoria": categoria,
        "preco": preco_oferta,
        "status": "DISPONÍVEL"
    }

    ofertas.append(oferta)
    print("Oferta", oferta["id"], "cadastrada:", categoria)


def listar_demandas():
    print("\nDEMANDAS")
    if len(demandas) == 0:
        print("Nenhuma demanda cadastrada.")

    for demanda in demandas:
        print(demanda["id"], "-", demanda["comerciante"], "-",
              demanda["produto"], "-", demanda["caixas"], "caixas -",
              demanda["bairro"], "- índice:", demanda["indice"],
              "-", demanda["status"])


def listar_ofertas():
    print("\nOFERTAS")
    if len(ofertas) == 0:
        print("Nenhuma oferta cadastrada.")

    for oferta in ofertas:
        print(oferta["id"], "-", oferta["fornecedor"], "-",
              oferta["produto"], "-", oferta["caixas"], "caixas -",
              oferta["categoria"], "- R$", format(oferta["preco"], ".2f"))


while True:
    print("\n=== ELOS ===")
    print("1 - Cadastrar demanda")
    print("2 - Cadastrar oferta")
    print("3 - Listar demandas")
    print("4 - Listar ofertas")
    print("0 - Sair")

    opcao = input("Escolha: ").strip()

    match opcao:
        case "1":
            cadastrar_demanda()
        case "2":
            cadastrar_oferta()
        case "3":
            listar_demandas()
        case "4":
            listar_ofertas()
        case "0":
            print("Programa encerrado.")
            break
        case _:
            print("Opção inválida.")
