# Author: DanielVii

import PySimpleGUI as sg
import mysql.connector as msc


class ColetarInfo:
    def __init__(self):
        self.__tamanho_janela = (510, 350)
        self.__tamanho_texto = (8, 1)
        self.__tipo_fonte = 'Courier 12'
        self.__nome_janela = 'Projeto Fc'

        self.continuar = True
        # Genericos. Seus valores irão mudar de função coletora a função coletora.
        self.__dict_info = dict()

        self.__table_name = str()
        self.__columns_names = str()
        self.__s_repetitions = int()
        self.__s_repetitions_str = str()
        self.__lines_info = list()


    def coletar_informacoes_empresa(self):
        """
        Criará um layout que receberá o preço da materia prima e o capital que o usuario possui.
        Então enviará para o banco de dados.

        """
        self.__table_name = "empresa"
        self.__columns_names = "valor_mp, capital"
        self.__s_repetitions = 2
        self.__transformar_s_repetitions_em_str()

        resposta_invalida = True
        texto_de_erro = sg.Text("\n")

        while resposta_invalida and self.continuar:

            layout = [
                # titulo
                [texto_de_erro],
                [sg.Text(f'{"Sobre a sua empresa":^45}', font=self.__tipo_fonte)],
                # perguntas
                [sg.Text("\n*use virgula para separar os centavos.")],
                [sg.Text('Custo para produzir unidade do produto', font=self.__tipo_fonte)],
                [sg.Input(key='valor_unidade', size=(60, 1))],
                [sg.Text('\n')],
                [sg.Text('Capital', font=self.__tipo_fonte)],
                [sg.Input(key='capital', size=(60, 1))],
                [sg.Text('\n')],
                [sg.Submit('Continuar', size=(6, 1)), sg.Cancel("Cancelar", size=(6, 1))]
            ]

            janela = sg.Window(self.__nome_janela, size=self.__tamanho_janela).layout(layout)

            botao, self.__dict_info = janela.read()

            janela.close()

            if botao == 'Continuar':
                self.__limpar_numeros()
                valor_invalido = self.__checar_validade_dos_numeros()
                if valor_invalido:
                    texto_de_erro = sg.Text('Imformação incorreta. \nNão são aceitos: letras ou números menores que 0.',
                                            font=self.__tipo_fonte, text_color='#ff0000')
                    continue
                else:

                    # criando informações para cada linha da tabela
                    lines_info = list()

                    linha = (self.__dict_info['valor_unidade'], self.__dict_info['capital'])
                    lines_info.append(linha)

                    self.__lines_info = lines_info

                    self.__enviar_para_bd()

                    resposta_invalida = False
            else:
                self.continuar = False

    def coletar_custos_fixos(self):
        """
        Criará um layout que receberá as informações de custo fixo.
        Além de mandar para o banco de dados todas as informações recolhidas.
        """
        self.__table_name = "custo_fixo"
        self.__columns_names = "nome, valor"
        self.__s_repetitions = 2
        self.__transformar_s_repetitions_em_str()
        resposta_invalida = True
        texto_de_erro = sg.Text("\n")

        while resposta_invalida and self.continuar:
            layout = [
                # titulo
                [texto_de_erro],
                [sg.Text(f'{"Digite os valores ":^40}\n{"dos seguintes gastos: ":^43}', font=self.__tipo_fonte)],
                [sg.Text("\n*use virgula para separar os centavos.")],
                # perguntas
                [sg.Text('Salário', size=self.__tamanho_texto, font=self.__tipo_fonte), sg.Input(key='salario')],
                [sg.Text('Água', size=self.__tamanho_texto, font=self.__tipo_fonte), sg.Input(key='agua')],
                [sg.Text('Energia', size=self.__tamanho_texto, font=self.__tipo_fonte), sg.Input(key='energia')],
                [sg.Text('Telefone', size=self.__tamanho_texto, font=self.__tipo_fonte), sg.Input(key='telefone')],
                [sg.Text('Outros', size=self.__tamanho_texto, font=self.__tipo_fonte), sg.Input(key='outros')],
                [sg.Text("\n")],
                [sg.Submit('Continuar', size=(6, 1)), sg.Cancel("Cancelar", size=(6, 1))]
            ]

            janela = sg.Window(self.__nome_janela, size=self.__tamanho_janela).layout(layout)

            botao, self.__dict_info = janela.Read()

            janela.close()

            if botao == 'Continuar':
                self.__limpar_numeros()
                valor_invalido = self.__checar_validade_dos_numeros()
                if valor_invalido:
                    texto_de_erro = sg.Text('Imformação incorreta. \nNão são aceitos: letras ou números menores que 0.',
                                            font=self.__tipo_fonte, text_color='#ff0000')
                    continue
                else:
                    # criando informações para cada linha da tabela
                    lines_info = list()
                    for nome_info, valor_info in self.__dict_info.items():
                        linha = (nome_info, valor_info)
                        lines_info.append(linha)

                    self.__lines_info = lines_info

                    self.__enviar_para_bd()

                    resposta_invalida = False

            else:
                self.continuar = False

    def coletar_info_demanda_valor(self):
        """
        Criará um layout que receberá informações de demanda e preço.

        """
        self.__table_name = "lucro_real"
        self.__columns_names = "mês, valor_produto, demanda"
        self.__s_repetitions = 3
        self.__transformar_s_repetitions_em_str()


        for mes in range(1, 4):

            resposta_invalida = True
            texto_de_erro = sg.Text("\n")

            while resposta_invalida and self.continuar:

                layout = [
                    # titulo
                    [texto_de_erro],
                    [sg.Text(f'{"Sobre os últimos 3 meses":^45}', font=self.__tipo_fonte)],
                    [sg.Text("\n*use virgula para separar os centavos.")],
                    [sg.Text(f'Demando do mês {mes}', font=self.__tipo_fonte)],
                    [sg.Input(key='demanda', size=(60, 1))],
                    [sg.Text('\n')],
                    [sg.Text(f'Preço do produto no mes {mes}', font=self.__tipo_fonte)],
                    [sg.Input(key='valor', size=(60, 1))],
                    [sg.Text('\n')],
                    [sg.Submit('Continuar', size=(6, 1)), sg.Cancel("Cancelar", size=(6, 1))]
                ]

                janela = sg.Window(self.__nome_janela, size=self.__tamanho_janela).layout(layout)

                botao, self.__dict_info = janela.read()

                janela.close()

                if botao == 'Continuar':
                    self.__limpar_numeros()
                    valor_invalido = self.__checar_validade_dos_numeros()
                    if valor_invalido:
                        texto_de_erro = sg.Text('Imformação incorreta.'
                                                '\nNão são aceitos: letras ou números menores que 0.',
                                                font=self.__tipo_fonte, text_color='#ff0000')
                        continue
                    else:
                        # criando informações para cada linha da tabela
                        lines_info = list()

                        linha = (f'{mes}', self.__dict_info["valor"], self.__dict_info["demanda"]) #tupla
                        lines_info.append(linha)

                        self.__lines_info = lines_info

                        self.__enviar_para_bd()

                        resposta_invalida = False
                else:
                    self.continuar = False

    def coletar_info_de_futuro_preco(self):
        """
        Criará um layout e pedirá o preço que o usuario deseja vender o produto.

        """
        self.__table_name = "simulacao_lucro"
        self.__columns_names = "simulacao_valor, estoque_nece, margem_lucro"
        self.__s_repetitions = 3
        self.__transformar_s_repetitions_em_str()

        resposta_invalida = True
        texto_de_erro = sg.Text("\n")

        while resposta_invalida and self.continuar:
            layout = [
                # titulo
                [texto_de_erro],
                [sg.Text(f'{"Com essas informações em mãos, nos diga:":^45}', font=self.__tipo_fonte)],
                # perguntas
                [sg.Text('\n\n')],
                [sg.Text("\n*use virgula para separar os centavos.")],
                [sg.Text('Por quanto você deseja vender o seu produto', font=self.__tipo_fonte)],
                [sg.Input(key='simulacao_valor', size=(70, 1))],
                [sg.Text('\n\n\n\n')],
                [sg.Submit('Continuar', size=(6, 1)), sg.Cancel("Cancelar", size=(6, 1))]
            ]

            janela = sg.Window(self.__nome_janela, size=self.__tamanho_janela).layout(layout)

            botao, self.__dict_info = janela.read()

            janela.close()

            if botao == 'Continuar':
                self.__limpar_numeros()
                valor_invalido = self.__checar_validade_dos_numeros()
                if valor_invalido:
                    texto_de_erro = sg.Text('Imformação incorreta. \nNão são aceitos: letras ou números menores que 0.',
                                            font=self.__tipo_fonte, text_color='#ff0000')
                    continue
                else:

                    # criando informações para cada linha da tabela
                    lines_info = list()

                    linha = (self.__dict_info['simulacao_valor'], 0, 0)
                    lines_info.append(linha)

                    self.__lines_info = lines_info

                    self.__enviar_para_bd()

                    resposta_invalida = False
            else:
                self.continuar = False

    def __checar_validade_dos_numeros(self):
        """
        Checará se os valores dados são números e se são maior ou igual a zero.
        :return: valor_invalida
        """
        for valor in self.__dict_info.values():
            try:
                float(valor)
            except:
                valor_invalido = True
                return valor_invalido

            valor_float = float(valor)

            if valor_float < 0:
                valor_invalido = True
                return valor_invalido

    def __limpar_numeros(self):
        """
        Tirará os pontos dos números e substituirá a virgula por um ponto.
        Além de substituir os espaços vazios por zero.

        """

        for chave, valor in self.__dict_info.items():

            tirar_ponto = valor.replace('.', '')

            trocar_virgula = tirar_ponto.replace(',', '.')

            valor_final = trocar_virgula

            if trocar_virgula == '':
                valor_final = '0'

            self.__dict_info[chave] = valor_final

    def __transformar_s_repetitions_em_str(self):
        """
        Entregará o valor de self.__s_repetitions_str, baseado no self.__s_repetitions
        """
        new_s = ''
        for s in range(1, self.__s_repetitions):
            new_s += '%s, '

        new_s += '%s'

        self.__s_repetitions_str = new_s

    def __enviar_para_bd(self):
        """
        Enviar informações para o banco de dados.
        """
        mydb = msc.connect(host='localhost', database='projeto_fc', user='root', password='')

        if mydb.is_connected():
            cursor = mydb.cursor()
            for linha in self.__lines_info:
                column = f'INSERT INTO {self.__table_name} ({self.__columns_names}) VALUES ({self.__s_repetitions_str})'
                data = linha

                cursor.execute(column, data)
                mydb.commit()

            cursor.close()
            mydb.close()


