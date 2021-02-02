# Author: DanielVii

import PySimpleGUI as Sg
import mysql.connector as msc


class Telas:
    def __init__(self):
        self.continuar = True

        self.__tamanho_janela = (510, 350)
        self.__tamanho_texto = (8, 1)
        self.__tipo_fonte = 'Courier 12'
        self.__nome_janela = 'Projeto Fc'

        # Genericos do layout
        self.__titulo = str()
        self.__body_text = list()
        self.__espaco_entre_titulo_e_body = int()
        self.__body = dict()

        self.__body_standard()

        # Genericos Coletar dados
        self.__table_name = str()

    def boas_vindas(self):

        self.__titulo = 'Seja bem-vindo(a) ao Projeto Facilite!'

        self.__espaco_entre_titulo_e_body = 2

        self.__body_text = [
            'Estamos aqui para facilitar o começo de sua',
            'empresa e aumentar o lucro de suas vendas.',
            '',
            '',
            '',
            'Vamos começar!'
        ]

        self.__tela_generica()

    def entregar_informacoes_sobre_o_que_serah_requisitato(self):

        self.__titulo = 'Para começar'

        self.__espaco_entre_titulo_e_body = 1

        self.__body_text = [
            'precisaremos de algumas informações: ',
            '',
            '- O custo para fazer a unidade do seu produto.',
            '- O tanto de dinheiro que sua empresa tem,',
            '  ou seja, seu capital.',
            '- O custo fixo mensal de sua empresa.'
        ]

        self.__tela_generica()

    def capital_insuficiente(self):

        self.__titulo = 'O seu capital é insuficiente.'

        self.__espaco_entre_titulo_e_body = 2

        self.__body_text = [
            '- Com o seu capital atual não é possível ',
            '  se sustentar e fabricar um produto.'
        ]

        self.__tela_generica()

    def resultado_inicial(self):
        self.__table_name = 'inicio'
        lista_capacidade_producao_e_preco_medio = self.__pegar_informacao_do_bd()

        ultima_linha = lista_capacidade_producao_e_preco_medio[-1]

        # [0] - id, [1] - capacidade produ, [2] - preço médio

        capacidade_produ = ultima_linha[1]

        preco_medio = ultima_linha[2]

        self.__titulo = "Informações para começar"

        self.__espaco_entre_titulo_e_body = 1

        self.__body_text = ['- Com o seu capital é possivel produzir',
                            f'  {capacidade_produ} unidades.',
                            '- Cada unidade terá o custo de produção de',
                            f'  R$ {preco_medio:.2f}.',
                            '  Levando em consideração todos os seus custos.'
                            ]

        self.__tela_generica()

    def hora_de_coletar(self):
        self.__titulo = 'Hora de entrar em ação!'

        self.__espaco_entre_titulo_e_body = 1

        self.__body_text = [
            '- Para aprimorarmos o desempenho de suas vendas',
            '  vamos precisar de mais informações.',
            '',
            'Elas são:',
            '- Demanda mensal, dos ultimos 3 meses.',
            '- preço da unidade em cada mês'
        ]

        self.__tela_generica()

    def valores_incosistentes(self):

        self.__titulo = 'Os valores dados são inconsistentes.'

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

        self.__titulo = "Aprimorando as vendas"

        self.__espaco_entre_titulo_e_body = 1

        self.__body_text = [
            '- Você terá lucro quando o preço do produto',
            f'  for maior que R$ {raiz_um:.2f} e menor que R$ {raiz_dois:.2f}',
            '- O seu maior lucro ocorrerá quando o produto',
            f'  estiver ao preço de R$ {preco_ideal:.2f}. Será um lucro',
            f'  de: R$ {lucro_ideal:.2f}',
            f'- Será necessário um estoque de {estoque_nec} unidades,',
            '  caso sua escolha seja pelo lucro máximo.'
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

        self.__titulo = 'Simulando futuros lucros'

        self.__espaco_entre_titulo_e_body = 1

        self.__body_text = [
            f'- Você terá um lucro de R$ {possivel_lucro:.2f}, quando o',
            f'  seu produto estiver ao preço de R$ {valor_dado:.2f}.',
            f'- Será necessário um estoque de {estoque_nec} unidades',
            '  para suprir a demanda.'
        ]

        self.__tela_generica()

    def __tela_generica(self):

        self.__colocar_texto_no_body()

        botoes = [Sg.Submit("Continuar", size=(8, 1)), Sg.Cancel("cancelar", size=(8, 1))]

        layout = [
            [Sg.Text('\n')],
            [Sg.Text(f'{self.__titulo:^45}', font=self.__tipo_fonte)],
            [Sg.Text(self.__body['parte_1'], font=self.__tipo_fonte)],
            [Sg.Text(self.__body['parte_2'], font=self.__tipo_fonte)],
            [Sg.Text(self.__body['parte_3'], font=self.__tipo_fonte)],
            [Sg.Text(self.__body['parte_4'], font=self.__tipo_fonte)],
            [Sg.Text(self.__body['parte_5'], font=self.__tipo_fonte)],
            [Sg.Text(self.__body['parte_6'], font=self.__tipo_fonte)],
            [Sg.Text(self.__body['parte_7'], font=self.__tipo_fonte)],
            [Sg.Text(self.__body['parte_8'], font=self.__tipo_fonte)],
            botoes
        ]

        janela = Sg.Window(self.__nome_janela, size=self.__tamanho_janela).layout(layout)

        botao, ___ = janela.read()

        if botao == 'cancelar':
            self.continuar = False

        self.__clean()
        janela.close()

    def __body_standard(self):
        for parte in range(1, 9):
            self.__body[f'parte_{parte}'] = ''

    def __colocar_texto_no_body(self):
        part_to_start = 1 + self.__espaco_entre_titulo_e_body

        posicao_do_texto_dado = 0
        for parte in range(part_to_start, 9):
            try:
                self.__body[f'parte_{parte}'] = self.__body_text[posicao_do_texto_dado]

                posicao_do_texto_dado += 1
            except IndexError:
                break

    def __clean(self):
        self.__titulo = ''
        self.__espaco_entre_titulo_e_body = 0
        self.__body_text = [
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            ''
        ]
        self.__colocar_texto_no_body()

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

