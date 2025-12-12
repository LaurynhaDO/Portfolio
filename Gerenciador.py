from Estoque import Estoque
from database import conectar

class Gerenciador:

    def __init__(self):
        print("Gerenciador de Estoque inicializado.")

    def cadastrar_novo_item(self, nome, categoria):
        novo = Estoque(nome, categoria)
        print(f"✅ Item '{novo._nome}' cadastrado com ID: {novo._id}")
        return novo

    def _instancia_existente(self, id_formatado):
        for it in Estoque.itens:
            if it._id == id_formatado:
                return it
        return None

    def pesquisar_item(self, termo):
        conn = conectar()
        cursor = conn.cursor()
        termo_str = str(termo).strip()

        if termo_str.isdigit():
            id_int = int(termo_str)
            cursor.execute(
                "SELECT id, nome, categoria, quantidade, valor_unitario FROM itens WHERE id = ?",
                (id_int,)
            )
            row = cursor.fetchone()
            conn.close()

            if not row:
                return []

            id_db, nome, categoria, quantidade, valor = row
            id_formatado = f"{id_db:04d}"

            inst = self._instancia_existente(id_formatado)
            if inst:
                return [inst]

            item = Estoque(nome, categoria, item_id=id_db, quantidade=quantidade, valor=valor, from_db=True)
            Estoque.itens.append(item)
            return [item]

        termo_like = f"%{termo_str.title()}%"
        cursor.execute("""
            SELECT id, nome, categoria, quantidade, valor_unitario
            FROM itens
            WHERE nome LIKE ? OR categoria LIKE ?
            ORDER BY nome
        """, (termo_like, termo_like))

        rows = cursor.fetchall()
        conn.close()

        resultados = []
        for id_db, nome, categoria, quantidade, valor in rows:
            id_formatado = f"{id_db:04d}"

            inst = self._instancia_existente(id_formatado)
            if inst:
                resultados.append(inst)
            else:
                item = Estoque(nome, categoria, item_id=id_db, quantidade=quantidade, valor=valor, from_db=True)
                Estoque.itens.append(item)
                resultados.append(item)

        return resultados

    def listar_todos_os_itens(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, categoria, quantidade, valor_unitario FROM itens ORDER BY nome")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("\nNenhum item em estoque.")
            return

        print("\n=== 📋 ESTOQUE ATUAL ===")
        for id_db, nome, categoria, quantidade, valor in rows:
            id_formatado = f"{id_db:04d}"

            inst = self._instancia_existente(id_formatado)
            if inst:
                inst.exibir_informacoes()
            else:
                item = Estoque(nome, categoria, item_id=id_db, quantidade=quantidade, valor=valor, from_db=True)
                Estoque.itens.append(item)
                item.exibir_informacoes()
        print("=======================\n")

    def remover_item(self, item_id_str):
        if not item_id_str.isdigit():
            print("ID inválido.")
            return False

        id_int = int(item_id_str)

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM movimentacoes WHERE item_id = ?", (id_int,))
        cursor.execute("DELETE FROM itens WHERE id = ?", (id_int,))
        apagados = cursor.rowcount

        conn.commit()
        conn.close()

        id_formatado = f"{id_int:04d}"
        inst = self._instancia_existente(id_formatado)
        if inst:
            try:
                Estoque.itens.remove(inst)
            except ValueError:
                pass

        if apagados:
            print(f"🗑️ Item {id_formatado} removido.")
            return True
        else:
            print("❌ Item não encontrado.")
            return False

    def gerar_relatorio_simples(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT quantidade, valor_unitario FROM itens")
        rows = cursor.fetchall()
        conn.close()

        total_diferentes = len(rows)
        total_quantidade = sum(r[0] for r in rows) if rows else 0
        total_valor = sum(r[0] * r[1] for r in rows) if rows else 0.0

        print("\n📊 RELATÓRIO SIMPLES DE ESTOQUE")
        print("-----------------------------------")
        print(f"| Produtos Diferentes: {total_diferentes:<10}|")
        print(f"| Quantidade Total:    {total_quantidade:<10}|")
        print(f"| Valor Total (R$):    {total_valor:10.2f}|")
        print("-----------------------------------\n")
