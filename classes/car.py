class Carro:
   def __init__(self, marca, modelo, ano):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano

   def exibir_informacoes(self):
        return f"{self.ano} {self.marca} {self.modelo}"
    
   def atualizar_modelo(self, novo_modelo):
      self.modelo = novo_modelo

   def atualizar_ano(self, novo_ano):
      self.ano = novo_ano

   def atualizar_marca(self, nova_marca):
      self.marca = nova_marca
    
   def 