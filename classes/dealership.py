class Dealership:
    def __init__(self, nome, localizacao):
        self.nome = nome
        self.localizacao = localizacao
        self.inventario = []

    def adicionar_carro(self, carro):
        self.inventario.append(carro)

    def delete_carro(self, carro):
        self.inventario.remove(carro)

    def listar_inventario(self):
        return [carro.exibir_informacoes() for carro in self.inventario]