from datetime import datetime
from database import conectar

class Estoque:
    itens = []
    ultimo_id = 0  

    def __init__(self, nome, categoria, item_id=None, quantidade=0, valor=0, from_db=False):
        if item_id is None:
            Estoque.ultimo_id += 1
            self._id = f"{Estoque.ultimo_id:04d}"
            self._nome = nome.title()
            self._categoria = categoria.title()
            self._quantidade = 0
            self._valor_unitario = 0.0
            self._movimentacoes = []
            Estoque.itens.append(self)
            self.salvar_item_no_banco()
        else:
            self._id = f"{int(item_id):04d}"
            self._nome = nome.title()
            self._categoria = categoria.title()
            self._quantidade = int(quantidade)
            self._valor_unitario = float(valor)
            self._movimentacoes = []
            if not from_db:
                Estoque.itens.append(self)

    def salvar_item_no_banco(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO itens (id, nome, categoria, quantidade, valor_unitario)
            VALUES (?, ?, ?, ?, ?)
        """, (int(self._id), self._nome, self._categoria, self._quantidade, self._valor_unitario))
        conn.commit()
        conn.close()

    def atualizar_item_banco(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE itens
            SET quantidade = ?, valor_unitario = ?
            WHERE id = ?
        """, (self._quantidade, self._valor_unitario, int(self._id)))
        conn.commit()
        conn.close()

    def registrar_movimentacao(self, tipo, quantidade, colaborador):
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        mov = {
            "tipo": tipo,
            "quantidade": quantidade,
            "colaborador": colaborador,
            "data": data
        }
        self._movimentacoes.append(mov)

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO movimentacoes (item_id, tipo, quantidade, colaborador, data_mov)
            VALUES (?, ?, ?, ?, ?)
        """, (int(self._id), tipo, quantidade, colaborador, data))
        conn.commit()
        conn.close()

    def listar_movimentacoes(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tipo, quantidade, colaborador, data_mov
            FROM movimentacoes
            WHERE item_id = ?
            ORDER BY id ASC
        """, (int(self._id),))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("\nNenhuma movimentação registrada.\n")
            return

        print(f"\n📜 Movimentações do item {self._nome} (ID {self._id}):")
        for tipo, qdt, colaborador, data in rows:
            print(f" - {tipo} | Qtd: {qdt} | Colaborador: {colaborador} | Data: {data}")
        print("")

    def entrada(self, quantidade, colaborador):
        self._quantidade += int(quantidade)
        self.atualizar_item_banco()
        self.registrar_movimentacao("Entrada", int(quantidade), colaborador)

    def saida(self, quantidade, colaborador):
        quantidade = int(quantidade)
        if quantidade > self._quantidade:
            print("❌ Estoque insuficiente!")
            return
        self._quantidade -= quantidade
        self.atualizar_item_banco()
        self.registrar_movimentacao("Saída", quantidade, colaborador)

    def definir_valor(self, valor):
        self._valor_unitario = float(valor)
        self.atualizar_item_banco()

    def exibir_informacoes(self):
        print(f"\n📦 Item: {self._nome}")
        print(f"🆔 ID: {self._id}")
        print(f"📂 Categoria: {self._categoria}")
        print(f"🔢 Quantidade: {self._quantidade}")
        print(f"💲 Valor unitário: R$ {self._valor_unitario:.2f}")
        print(f"💰 Valor total: R$ {self._quantidade * self._valor_unitario:.2f}\n")
