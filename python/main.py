import math

# ELOS - cadastros iniciais
# Dados usados apenas durante a execução do programa.

bairros = [
    {"nome": "Itaquera"},
    {"nome": "Guaianases"},
    {"nome": "Cidade Tiradentes"}
]


demandas = []
ofertas = []


def ler_texto(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto != "":
            return texto
        print("Esse campo não pode ficar vazio.")


def ler_produto():
    while True:
        produto = ler_texto("Produto: ").lower()

        for letra in produto:
            if letra.isalpha():
                return produto

        print("Informe um alimento, como banana ou tomate.")


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
    produto = ler_produto()
    caixas = ler_inteiro("Quantidade de caixas: ", 1)
    bairro = escolher_bairro()

    demanda = {
        "id": len(demandas) + 1,
        "comerciante": comerciante,
        "produto": produto,
        "caixas": caixas,
        "bairro": bairro["nome"],
        "status": "ABERTA"
    }

    demandas.append(demanda)
    print("Demanda", demanda["id"], "cadastrada com sucesso!")


def cadastrar_oferta():
    print("\nCADASTRO DE OFERTA")
    fornecedor = ler_texto("Nome do fornecedor: ")
    produto = ler_produto()

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
              demanda["bairro"], "-", demanda["status"])


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

    # Agrupa os pedidos por bairro e produto.
    bairros_ordenados = bairros

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


# Modelo matematico de qualidade da ELOS
Q0 = 100.0
Q_MIN = 80.0
K_CONTROLADO = 0.015
K_ESTRESSE = 0.085

veiculos = []


def ler_decimal(pergunta, minimo, maximo):
    while True:
        try:
            numero = float(input(pergunta).replace(",", "."))

            if math.isfinite(numero) and minimo <= numero <= maximo:
                return numero

        except ValueError:
            pass

        print("Digite um numero entre", minimo, "e", maximo)


def calcular_qualidade(horas, temperatura):
    if temperatura < 15:
        return None

    if temperatura <= 30:
        taxa = K_CONTROLADO
    else:
        taxa = K_ESTRESSE

    return Q0 * math.exp(-taxa * horas)


def simular_qualidade():
    print("\nQUALIDADE ESTIMADA DA ROTA")

    horas = ler_decimal("Tempo em horas (0 a 24): ", 0, 24)
    temperatura = ler_decimal("Temperatura (0 a 100 C): ", 0, 100)

    if temperatura < 15:
        print("Temperatura aceita, mas sem coeficiente definido abaixo de 15 C.")
        print("Rota nao aprovada pelo modelo matematico.")
        return

    if temperatura <= 30:
        taxa = K_CONTROLADO
    else:
        taxa = K_ESTRESSE

    qualidade = calcular_qualidade(horas, temperatura)
    tempo_maximo = -math.log(Q_MIN / Q0) / taxa

    print("Qualidade estimada: {:.2f}%".format(qualidade))
    print("Tempo limite no modelo: {:.2f} horas".format(tempo_maximo))

    if qualidade >= Q_MIN:
        print("APROVADA pelo modelo matematico.")
    else:
        print("BLOQUEADA pelo modelo matematico.")

    print("Resultado simulado, sem certificacao sanitaria.")


def ler_horario():
    while True:
        horario = input("Chegada prevista (HH:MM): ").strip()
        partes = horario.split(":")

        if len(partes) == 2:
            try:
                hora = int(partes[0])
                minuto = int(partes[1])

                if 0 <= hora <= 23 and 0 <= minuto <= 59:
                    return "{:02d}:{:02d}".format(hora, minuto)

            except ValueError:
                pass

        print("Horario invalido. Exemplo: 07:30")


def cadastrar_veiculo():
    print("\nCADASTRAR VEICULO")

    nome = ler_texto("Identificacao do veiculo: ")
    rota = input("Possui rota fixa? (s/n): ").strip().lower()

    if rota != "s":
        print("Cadastro recusado. Apenas rotas fixas.")
        return

    bairro = escolher_bairro()
    dia = ler_texto("Dia da semana: ")
    chegada = ler_horario()
    capacidade = ler_inteiro("Capacidade ociosa em caixas: ", 1)
    horas = ler_decimal("Duracao da rota (horas): ", 0.01, 24)
    temperatura = ler_decimal("Temperatura prevista (0 a 100 C): ", 0, 100)

    veiculo = {
        "nome": nome,
        "bairro": bairro["nome"],
        "dia": dia,
        "chegada": chegada,
        "capacidade": capacidade,
        "horas": horas,
        "temperatura": temperatura
    }

    veiculos.append(veiculo)
    print("Veiculo cadastrado com sucesso!")


def alocar_compra():
    print("\nALOCAR COMPRA EM ROTA FIXA")

    confirmadas = []

    for compra in compras:
        if compra["status"] == "CONFIRMADA":
            confirmadas.append(compra)
            print(compra["id"], "-", compra["produto"], "-",
                  compra["bairro"], "-", compra["caixas"], "caixas")

    if len(confirmadas) == 0:
        print("Nenhuma compra confirmada.")
        return

    numero = ler_inteiro("Numero da compra: ", 1)
    escolhida = None

    for compra in confirmadas:
        if compra["id"] == numero:
            escolhida = compra

    if escolhida is None:
        print("Compra nao encontrada.")
        return

    for veiculo in veiculos:
        if veiculo["bairro"] != escolhida["bairro"]:
            continue

        if veiculo["chegada"] > "08:00":
            continue

        if veiculo["capacidade"] < escolhida["caixas"]:
            continue

        qualidade = calcular_qualidade(
            veiculo["horas"], veiculo["temperatura"]
        )

        if qualidade is None or qualidade < Q_MIN:
            continue

        veiculo["capacidade"] -= escolhida["caixas"]
        escolhida["status"] = "ALOCADA"

        print("Alocacao confirmada!")
        print("Veiculo:", veiculo["nome"])
        print("Bairro:", veiculo["bairro"])
        print("Dia:", veiculo["dia"])
        print("Chegada:", veiculo["chegada"])
        print("Qualidade estimada: {:.2f}%".format(qualidade))
        print("Capacidade restante:", veiculo["capacidade"], "caixas")
        return

    print("Nenhuma rota compativel encontrada.")
    print("Verifique bairro, horario, capacidade ou qualidade.")


while True:
    print("\n=== ELOS ===")
    print("1 - Cadastrar demanda")
    print("2 - Cadastrar oferta")
    print("3 - Listar demandas")
    print("4 - Listar ofertas")
    print("5 - Formar compra coletiva")
    print("6 - Confirmar compra coletiva")
    print("7 - Estimar qualidade da rota")
    print("8 - Cadastrar veiculo")
    print("9 - Alocar compra")
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
        case "7":
            simular_qualidade()
        case "8":
            cadastrar_veiculo()
        case "9":
            alocar_compra()
        case "0":
            print("Programa encerrado.")
            break
        case _:
            print("Opção inválida.")
