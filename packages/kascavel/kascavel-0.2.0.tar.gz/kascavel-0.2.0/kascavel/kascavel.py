from cleo.application import Application
from hello_command import HelloCommand

application = Application()
application.add(HelloCommand())

# Rodando a aplicação
if __name__ == "__main__":
    application.run()
