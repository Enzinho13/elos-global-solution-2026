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



compras = []


def formar_compra_coletiva():
    print()
    print("COMPRAS COLETIVAS")
    encontrou = False

    # Bairros com índice maior são atendidos primeiro.
    bairros_ordenados = sorted(bairros, key=lambda b: b["indice"], reverse=True)

    for bairro in bairros_ordenados:
        produtos = []

        for demanda in demandas:
            pendente = demanda["caixas"] - demanda.get("reservadas", 0)

            if demanda["bairro"] == bairro["nome"] and pendente > 0:
                if demanda["produto"] not in produtos:
                    produtos.append(demanda["produto"])

        for produto in produtos:
            encontrou = True
            participantes = []
            total = 0

            for demanda in demandas:
                pendente = demanda["caixas"] - demanda.get("reservadas", 0)

                if demanda["bairro"] == bairro["nome"] and demanda["produto"] == produto and pendente > 0:
                    participantes.append(demanda)
                    total += pendente

            print()
            print(produto.title(), "-", bairro["nome"], "-", total, "caixas solicitadas")

            for demanda in participantes:
                pendente = demanda["caixas"] - demanda.get("reservadas", 0)
                print(" ", demanda["comerciante"], "-", pendente, "caixa(s)")

            if total < 10:
                print("Grupo incompleto. Faltam", 10 - total, "caixa(s).")
                continue

            oferta_escolhida = None

            for oferta in ofertas:
                if oferta["produto"] == produto and oferta["caixas"] >= 10:
                    oferta_escolhida = oferta
                    break

            if oferta_escolhida is None:
                print("Sem match: não existe oferta com pelo menos 10 caixas disponíveis.")
                continue

            disponivel = oferta_escolhida["caixas"]
            cotas = []

            for demanda in participantes:
                pendente = demanda["caixas"] - demanda.get("reservadas", 0)
                quantidade = min(pendente, disponivel)

                if quantidade > 0:
                    demanda["reservadas"] = demanda.get("reservadas", 0) + quantidade

                    if demanda["reservadas"] == demanda["caixas"]:
                        demanda["status"] = "RESERVADA"
                    else:
                        demanda["status"] = "PARCIAL"

                    cotas.append((demanda["id"], quantidade))
                    disponivel -= quantidade

            reservado = oferta_escolhida["caixas"] - disponivel
            oferta_escolhida["caixas"] = disponivel
            oferta_escolhida["status"] = "RESERVADO"

            compra = {
                "id": len(compras) + 1,
                "produto": produto,
                "bairro": bairro["nome"],
                "caixas": reservado,
                "cotas": cotas,
                "status": "AGUARDANDO CONFIRMAÇÃO"
            }

            compras.append(compra)

            if reservado == total:
                print("Match completo!", reservado, "caixas reservadas.")
            else:
                print("Match parcial!", reservado, "de", total, "caixas reservadas.")
                print("O restante continua pendente.")

            print("Compra", compra["id"], "aguardando confirmação manual.")

    if not encontrou:
        print("Não existem demandas pendentes para agrupar.")


def confirmar_compra():
    if len(compras) == 0:
        print("Nenhuma compra coletiva foi criada.")
        return

    print()
    print("COMPRAS COLETIVAS")

    for compra in compras:
        print(compra["id"], "-", compra["produto"], "-", compra["bairro"],
              "-", compra["caixas"], "caixas -", compra["status"])

    numero = ler_inteiro("Número da compra para confirmar: ", 1)

    for compra in compras:
        if compra["id"] == numero:
            if compra["status"] == "CONFIRMADA":
                print("Essa compra já foi confirmada.")
                return

            print("Confirmar as cotas dos comerciantes:")

            for id_demanda, quantidade in compra["cotas"]:
                for demanda in demandas:
                    if demanda["id"] == id_demanda:
                        resposta = input(
                            demanda["comerciante"] + " - " +
                            str(quantidade) + " caixas (s/n): "
                        ).strip().lower()

                        if resposta != "s":
                            print("Confirmação pendente. As caixas seguem reservadas.")
                            return

            compra["status"] = "CONFIRMADA"
            print("Compra", numero, "confirmada!")
            print("Janela de 30 minutos apenas simulada, sem cronômetro real.")
            return

    print("Compra não encontrada.")


while True:
    print("\n=== ELOS ===")
    print("1 - Cadastrar demanda")
    print("2 - Cadastrar oferta")
    print("3 - Listar demandas")
    print("4 - Listar ofertas")
    print("5 - Formar compra coletiva")
    print("6 - Confirmar compra coletiva")
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
        case "5":
            formar_compra_coletiva()
        case "6":
            confirmar_compra()
        case "0":
            print("Programa encerrado.")
            break
        case _:
            print("Opção inválida.")
