# Author: DanielVii

import PySimpleGUI as sg
import mysql.connector as msc


class Telas:
    def __init__(self):
        self.continuar = True

        self.__tamanho_janela = (510, 350)
        self.__tamanho_texto = (8, 1)
        self.__tipo_fonte = 'Courier 12'
        self.__nome_janela = 'Projeto Fc'

        # Genericos do layout
        self.__layout = list()

        # Generico. Coletar dados
        self.__table_name = str()


    def boas_vindas(self):
        self.__layout = [
            [sg.Text('\n')],
            [sg.Text(f'{"Seja bem-vindo(a) ao Projeto Facilite!":^45}', font=self.__tipo_fonte)],
            [sg.Text('\n'*3)],
            [sg.Text('Estamos aqui para facilitar o começo de sua \nempresa e aumentar o lucro de suas vendas.',
                     font=self.__tipo_fonte)],
            [sg.Text('\n'*3)],
            [sg.Text(f'Vamos começar!', font=self.__tipo_fonte)]
        ]
        self.__tela_generica()

    def entregar_informacoes_sobre_o_que_serah_requisitato(self):
        self.__layout = [
            [sg.Text('\n'*2)],
            [sg.Text('Para começar, \nprecisaremos de algumas informações:', font=self.__tipo_fonte)],
            [sg.Text('\n')],
            [sg.Text('- O custo para fazer a unidade \n  do seu produto.', font=self.__tipo_fonte)],
            [sg.Text('- O tanto de dinheiro que sua empresa tem,\n  ou seja, seu capital.', font=self.__tipo_fonte)],
            [sg.Text('- O custo fixo mensal de sua empresa.', font=self.__tipo_fonte)],
            [sg.Text('\n'*1)]
        ]
        self.__tela_generica()

    def capital_insuficiente(self):
        self.__layout = [
            [sg.Text('\n'*3)],
            [sg.Text('O seu capital é insuficiente para começar a empresa. :(')],
            [sg.Text('\n'*11)]
        ]
        self.__tela_generica()

    def resultado_inicial(self):
        self.__table_name = 'inicio'
        lista_capacidade_producao_e_preco_medio = self.__pegar_informacao_do_bd()

        ultima_linha = lista_capacidade_producao_e_preco_medio[-1]

        # [0] - id, [1] - capacidade produ, [2] - preço médio

        capacidade_produ = ultima_linha[1]

        preco_medio = ultima_linha[2]

        self.__layout = [
            [sg.Text('\n')],
            [sg.Text(f'{"Informações para começar":^45}', font=self.__tipo_fonte)],
            [sg.Text('\n')],
            [sg.Text(f'- Com o seu capital é possivel produzir', font=self.__tipo_fonte)],
            [sg.Text(f'  {capacidade_produ} unidades.', font=self.__tipo_fonte)],
            [sg.Text('- Cada unidade terá o custo de produção de', font=self.__tipo_fonte)],
            [sg.Text(f'  R$ {preco_medio:.2f}.', font=self.__tipo_fonte)],
            [sg.Text('  Levando em consideração todos os seus custos.', font=self.__tipo_fonte)],
            [sg.Text('\n')]
        ]
        self.__tela_generica()

    def hora_de_coletar(self):
        self.__layout = [
            [sg.Text('\n')],
            [sg.Text(f'{"Hora de entrar em ação!":^45}', font=self.__tipo_fonte)],
            [sg.Text('\n')],
            [sg.Text('- Para aprimorarmos o desempenho de suas vendas', font=self.__tipo_fonte)],
            [sg.Text('  vamos precisar de mais informações.', font=self.__tipo_fonte)],
            [sg.Text('  Elas são: a demanda mensal e o preço unitario,', font=self.__tipo_fonte)],
            [sg.Text('  dos ultimos 3 meses. ', font=self.__tipo_fonte)],
            [sg.Text('\n'*3)]
        ]

        self.__tela_generica()

    def valores_incosistentes(self):
        self.__layout = [
            [sg.Text('\n' * 3)],
            [sg.Text('Os valores dados são inconsistentes. Tente novamente. ')],
            [sg.Text('\n' * 11)]
        ]
        self.__tela_generica()

    def valores_ideais(self):
        self.__table_name = 'valores_ideais'
        lista_valores_ideais = self.__pegar_informacao_do_bd()

        ultima_linha = lista_valores_ideais[-1]

        # [0] - id, [1] - preço ideal, [2] - estoque necessario, [3] - raiz um, [4] - raiz dois, [5] - lucro ideal

        preco_ideal = ultima_linha[1]
        estoque_nec = ultima_linha[2]
        raiz_um = ultima_linha[3]
        raiz_dois = ultima_linha[4]
        lucro_ideal = ultima_linha[5]

        self.__layout = [
            [sg.Text('\n')],
            [sg.Text(f'{"Aprimorando as vendas":^45}', font=self.__tipo_fonte)],
            [sg.Text('\n')],
            [sg.Text('- Você terá lucro quando o preço do produto', font=self.__tipo_fonte)],
            [sg.Text(f'  for maior que R$ {raiz_um:.2f} e menor que R$ {raiz_dois:.2f}', font=self.__tipo_fonte)],
            [sg.Text('- O seu maior lucro ocorrerá quando o produto', font=self.__tipo_fonte)],
            [sg.Text(f'  estiver ao preço de R$ {preco_ideal:.2f}. Será um lucro', font=self.__tipo_fonte)],
            [sg.Text(f'  de: R$ {lucro_ideal:.2f}', font=self.__tipo_fonte)],
            [sg.Text(f'- Será necessário um estoque de {estoque_nec} unidades,', font=self.__tipo_fonte)],
            [sg.Text('  caso sua escolha seja pelo lucro máximo.', font=self.__tipo_fonte)]
        ]
        self.__tela_generica()

    def simulacao_lucro(self):
        self.__table_name = 'simulacao_lucro'
        lista_simulacao = self.__pegar_informacao_do_bd()

        ultima_linha = lista_simulacao[-1]

        #[0] - id, [1] - valor dado, [2] - estoque necessario, [3] - possivel lucro

        valor_dado = ultima_linha[1]
        estoque_nec = ultima_linha[2]
        possivel_lucro = ultima_linha[3]

        self.__layout = [
            [sg.Text('\n')],
            [sg.Text(f'{"Simulando futuros lucros":^45}', font=self.__tipo_fonte)],
            [sg.Text('\n')],
            [sg.Text(f'- Você terá um lucro de R$ {possivel_lucro:.2f}, quando o', font=self.__tipo_fonte)],
            [sg.Text(f'  seu produto estiver ao preço de R$ {valor_dado:.2f}.', font=self.__tipo_fonte)],
            [sg.Text(f'- Será necessário um estoque de {estoque_nec} unidades', font=self.__tipo_fonte)],
            [sg.Text('  para suprir a demanda.', font=self.__tipo_fonte)],
            [sg.Text('\n'*4)]
        ]

        self.__tela_generica()

    def __tela_generica(self):
        layout_botoes = [
            [sg.Submit("Continuar", size=(8, 1)), sg.Cancel("cancelar", size=(8, 1))]
        ]
        self.__layout.extend(layout_botoes)
        janela = sg.Window(self.__nome_janela, size=self.__tamanho_janela).layout(self.__layout)

        botao, ___ = janela.read()

        if botao == 'cancelar':
            self.continuar = False

        janela.close()

    def __pegar_informacao_do_bd(self):
        """

        :return: Retornar os resultados da tabela em uma lista
        """
        mydb = msc.connect(host='localhost', database='projeto_fc', user='root', password='')

        if mydb.is_connected():
            cursor = mydb.cursor()

            get_information = f"SELECT * FROM {self.__table_name} "

            cursor.execute(get_information)

            resultado = cursor.fetchall()

            cursor.close()
            mydb.close()

            return resultado
