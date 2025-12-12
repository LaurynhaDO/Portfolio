from Gerenciador import Gerenciador
from database import criar_tabelas
from Usuarios import Usuario

def exibir_menu(admin=False):
    print("\n==============================")
    print("📦 SISTEMA DE CONTROLE DE ESTOQUE")
    print("==============================")
    print("1. Cadastrar Novo Item")
    print("2. Fazer Movimentação (Entrada/Saída)")
    print("3. Pesquisar Item")
    print("4. Listar Todos os Itens")
    print("5. Gerar Relatório")
    print("6. Remover Item")
    print("7. Visualizar Movimentações")
    if admin:
        print("8. Cadastrar Novo Usuário (ADMIN)")
    print("9. Sair")

def cadastrar_usuario_interface(admin):
    print("\n--- CADASTRO DE USUÁRIO ---")

    if not admin:
        print("❌ Apenas administradores podem cadastrar usuários.")
        return

    nome = input("Nome: ").strip()
    usuario = input("Usuário: ").strip()
    senha = input("Senha: ").strip()
    tipo = input("Tipo (admin/usuario): ").strip().lower()

    if tipo not in ("admin", "usuario"):
        print("❌ Tipo inválido.")
        return

    if not nome or not usuario or not senha:
        print("❌ Todos os campos são obrigatórios.")
        return

    try:
        Usuario.criar_usuario(nome, usuario, senha, tipo)
        print(f"✅ Usuário '{usuario}' criado com sucesso!")
    except Exception as e:
        print("Erro ao criar usuário:", e)

def cadastrar_item_interface(ger):
    print("\n--- CADASTRO DE NOVO ITEM ---")
    nome = input("Nome: ").strip()
    categoria = input("Categoria: ").strip()
    valor_unitario = input("Valor unitário: ").strip()

    if not nome or not categoria:
        print("❌ Nome e categoria obrigatórios.")
        return

    novo = ger.cadastrar_novo_item(nome, categoria)

    if valor_unitario:
        try:
            novo.definir_valor(float(valor_unitario))
            print("Valor definido com sucesso!")
        except:
            print("⚠️ Valor inválido.")

def encontrar_item_por_id(ger, item_id):
    r = ger.pesquisar_item(item_id)
    return r[0] if r else None

def fazer_movimentacao_interface(ger):
    print("\n--- MOVIMENTAÇÃO DE ESTOQUE ---")
    item_id = input("ID: ").strip()

    item = encontrar_item_por_id(ger, item_id)
    if not item:
        print("❌ Item não encontrado.")
        return

    print(f"Item: {item._nome} (Atual: {item._quantidade})")
    tipo = input("E = Entrada | S = Saída: ").upper()

    if tipo not in ("E", "S"):
        print("❌ Tipo inválido.")
        return

    try:
        qtd = int(input("Quantidade: "))
        if qtd <= 0:
            raise ValueError
    except:
        print("❌ Quantidade inválida.")
        return

    colaborador = input("Colaborador: ")
    if tipo == "E":
        item.entrada(qtd, colaborador)
    else:
        item.saida(qtd, colaborador)

def pesquisar_item_interface(ger):
    termo = input("Termo de busca: ").strip()
    if not termo:
        print("❌ Campo vazio.")
        return

    resultados = ger.pesquisar_item(termo)

    if not resultados:
        print("Nenhum item encontrado.")
        return

    for it in resultados:
        it.exibir_informacoes()

def listar_todos_interface(ger):
    ger.listar_todos_os_itens()

def gerar_relatorio_interface(ger):
    ger.gerar_relatorio_simples()

def remover_item_interface(ger):
    item_id = input("ID: ").strip()
    if item_id:
        ger.remover_item(item_id)

def visualizar_movimentacoes_interface(ger):
    item_id = input("ID: ").strip()
    item = encontrar_item_por_id(ger, item_id)
    if item:
        item.listar_movimentacoes()

def executar_programa():
    criar_tabelas()

    print("\n===== LOGIN =====")
    user = input("Usuário: ").strip()
    senha = input("Senha: ").strip()

    dados = Usuario.autenticar(user, senha)

    if not dados:
        print("❌ Usuário ou senha incorretos.")
        return

    user_id, nome, tipo = dados
    admin = (tipo.lower() == "admin")

    print(f"\nBem-vindo(a), {nome} ({tipo}).")

    ger = Gerenciador()

    while True:
        exibir_menu(admin)

        opc = input("\nEscolha: ").strip()

        if opc == "1":
            cadastrar_item_interface(ger)
        elif opc == "2":
            fazer_movimentacao_interface(ger)
        elif opc == "3":
            pesquisar_item_interface(ger)
        elif opc == "4":
            listar_todos_interface(ger)
        elif opc == "5":
            gerar_relatorio_interface(ger)
        elif opc == "6":
            if admin:
                remover_item_interface(ger)
            else:
                print("🚫 Proibido para usuários comuns.")
        elif opc == "7":
            visualizar_movimentacoes_interface(ger)
        elif opc == "8" and admin:
            cadastrar_usuario_interface(admin)
        elif opc == "9":
            print("Encerrando... Até mais!")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    executar_programa()
