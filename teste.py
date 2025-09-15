from sqlmodel import Session, select
from database import engine  # Importa a engine que você configurou

print("Tentando se conectar ao banco de dados...")

try:
    # O 'with' garante que a sessão será fechada corretamente
    with Session(engine) as session:
        # Executa uma consulta muito simples: "SELECT 1"
        # Isso não toca em nenhuma tabela, é só um "ping" no banco.
        session.exec(select(1))
    
    # Se o código chegou até aqui sem erros, a conexão foi um sucesso!
    print("✅ Conexão com o banco de dados bem-sucedida!")

except Exception as e:
    # Se qualquer erro ocorrer durante a tentativa de conexão ou consulta...
    print("❌ Falha ao conectar ao banco de dados.")
    print(f"Erro: {e}")

finally:
    print("Teste de conexão finalizado.")
