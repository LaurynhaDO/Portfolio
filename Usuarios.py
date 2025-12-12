from database import conectar

class Usuario:
    @staticmethod
    def criar_usuario(nome, usuario, senha, tipo="usuario"):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO usuarios (nome, usuario, senha, tipo)
            VALUES (?, ?, ?, ?)
        """, (nome, usuario, senha, tipo))

        conn.commit()
        conn.close()

    @staticmethod
    def autenticar(usuario, senha):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nome, tipo 
            FROM usuarios
            WHERE usuario = ? AND senha = ?
        """, (usuario, senha))

        resultado = cursor.fetchone()
        conn.close()
        return resultado
