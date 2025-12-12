from database import criar_tabelas
from Usuarios import Usuario

criar_tabelas()

# Criação do admin padrão
Usuario.criar_usuario("Administrador", "admin", "1234", "admin")
print("Admin criado com sucesso!")
