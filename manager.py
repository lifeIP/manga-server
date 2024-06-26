from src.database.manage import deploy
from routes import run_routes



if __name__ == "__main__":
    print("Ведеите ответ(1-запуск сервера, 2-запуск конфигурации базы данных)")
    answer = input(">>> ")

    if int(answer) == 1:
        run_routes()
    else:
        deploy()