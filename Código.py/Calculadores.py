# Author: DanielVii

import mysql.connector as msc
from decimal import Decimal



class Calculos:
    def __init__(self):
        self.continuar = True
        self.capital_insuf = False
        self.valores_inconsistentes = False
        # Calculo inicial
        self.__custo_fixo_total = Decimal()
        self.__estoque_possivel = int()
        self.__custo_total = Decimal()
        self.__preco_medio = Decimal()
        self.__precomp = Decimal()

        # calculo preço ideal
        self.__a = Decimal()
        self.__b = Decimal()
        self.__meses_analisados = 3
        self.__raiz_um = Decimal()
        self.__raiz_dois = Decimal()
        self.__preco_ideal = Decimal()
        self.__estoque_necessario = int()
        self.__lucro_ideal = Decimal()

        # genericos para calculos
        self.__preco_g = Decimal()
        self.__estoque_g = int()
        self.__lucro_g = Decimal()

        # Genericos para buscar info no bd. Irão mudar de valor de acordo com a necessidade
        self.__table_name = str()

        # Genericos para entregar info ao bd.
        self.__table_name = str()
        self.__columns_names = str()
        self.__s_repetitions = int()
        self.__s_repetitions_str = str()
        self.__lines_info = tuple()

    def info_iniciais(self):
        """
        Função que agrupará as que calcularão as informações iniciais. Então mandará elas para o BD.
        """
        self.__calcular_valor_fixo_total()

        self.__calcular_quantos_produtos_podem_ser_feitos()

        self.__calcular_preco_medio_do_produto()

        # infos para adicionar no BD
        self.__table_name = 'inicio'
        self.__columns_names = 'cap_pro, custo_med'
        self.__s_repetitions = 2
        self.__transformar_s_repetitions_em_str()

        self.__lines_info = (self.__estoque_possivel, self.__preco_medio)

        self.__enviar_para_bd()

    def preco_ideal(self):
        """
        Retornará ao BD as informações sobre preço ideal e o estoque necessario pra produzi-lo,
        além do preço onde o lucro será zero.
        """

        self.__calcular_a_e_b()

        self.__calcular_os_dois_precos_que_zeram_o_lucro()

        #preco_g já foi declarado na função calcular_os_dois_precos...

        estoque_necessario = self.__calcular_quantidade_em_relacao_ao_preco()

        lucro_ideal = self.__calcular_lucro_em_relacao_ao_preco()

        # infos para adicionar no BD
        self.__table_name = 'valores_ideais'
        self.__columns_names = 'preco, estoque_nec, raiz_um, raiz_dois, lucro_ideal'
        self.__s_repetitions = 5
        self.__transformar_s_repetitions_em_str()

        self.__lines_info = (self.__preco_ideal, estoque_necessario, self.__raiz_um, self.__raiz_dois, lucro_ideal)

        self.__enviar_para_bd()

    def simulacao_lucro(self):
        self.__table_name = 'simulacao_lucro'

        lista_simulacao_lucro = self.__pegar_informacao_do_bd()

        ultima_linha_simulacao_lucro = lista_simulacao_lucro[-1]

        # [0] = id, [1] = preço_dado, [2] = estoque_necessario, [3] = margem_de_lucro

        self.__preco_g = ultima_linha_simulacao_lucro[1]

        estoque_necessario = self.__calcular_quantidade_em_relacao_ao_preco()

        lucro_provavel = self.__calcular_lucro_em_relacao_ao_preco()

        # infos para adicionar no BD
        self.__table_name = 'simulacao_lucro'
        self.__columns_names = 'simulacao_valor, estoque_nece, margem_lucro'
        self.__s_repetitions = 3
        self.__transformar_s_repetitions_em_str()

        self.__lines_info = (self.__preco_g, estoque_necessario, lucro_provavel)

        self.__enviar_para_bd()

    def __calcular_a_e_b(self):
        """
        Calculará o 'a' usando: a = (soma(P.D) - N.Pm.Dm)/(soma(p^2) - N.(Pm)^2)
        e 'b' usando: b = Dm - a.Pm
        """

        self.__table_name = 'lucro_real'
        lista_valor_produto_demanda = self.__pegar_informacao_do_bd()

        soma_valor_produto = Decimal()
        soma_demanda = int()

        soma_produto_vezes_demanda = Decimal()
        soma_produto_ao_quadrado = Decimal()
        # pegará infos dos últimos 3 meses
        for info_mes in lista_valor_produto_demanda[-3:]:
            # info_mes[0] = id, info_mes[1] = mês, info_mes[2] = valor_produto, info_mes[3] = demanda
            produto = Decimal(info_mes[2])
            demanda = int(info_mes[3])

            soma_valor_produto += produto
            soma_demanda += demanda

            soma_produto_vezes_demanda += (produto * demanda)
            soma_produto_ao_quadrado += (produto ** 2)

        media_produto = soma_valor_produto / self.__meses_analisados
        media_demanda = soma_demanda // self.__meses_analisados
        try:
            self.__a = ((soma_produto_vezes_demanda - self.__meses_analisados * media_produto * media_demanda) /
                        (soma_produto_ao_quadrado - self.__meses_analisados * media_produto**2))

            self.__b = (media_demanda - self.__a * media_produto)
        except:
            self.valores_inconsistentes = True
    def __calcular_os_dois_precos_que_zeram_o_lucro(self):
        """
        Será usado a formula: L(p) = a.p^2 + (b - a*preco_materia_prima).p - CF - b*preco_m_p
        Além de calcular os dois preços que irão zerar o lucro, essa função também calculará o preço ideal.
        """

        # a,b e c da formula de Bhaskara
        a = self.__a
        b = self.__b - self.__a * self.__precomp
        c = -self.__custo_fixo_total - self.__b * self.__precomp

        delta = b**2 - 4 * a * c

        self.__raiz_um = (-b + delta ** (Decimal(1 / 2))) / (2 * a)
        self.__raiz_dois = (-b - delta ** (Decimal(1 / 2))) / (2 * a)

        if self.__raiz_um < 0 or self.__raiz_dois < 0:
            self.valores_inconsistentes = True

        preco_ideal = (self.__raiz_um + self.__raiz_dois)/2

        self.__preco_ideal = preco_ideal

        self.__preco_g = preco_ideal

    def __calcular_quantidade_em_relacao_ao_preco(self):
        """
        Usará a formula: q(p) = a.p + b
        Calculará o estoque necessario, a depender do preço do produto.
        :return: Estoque necessario.
        """

        estoque_necessario = self.__a*self.__preco_g + self.__b

        return estoque_necessario

    def __calcular_lucro_em_relacao_ao_preco(self):
        """
        Usará a formula: L(p) = a.p^2 + (b - a*preco_materia_prima).p - CF - b*preco_m_p
        :Return: lucro
        """
        lucro = (self.__a*self.__preco_g**2 + (self.__b - self.__a*self.__precomp)*self.__preco_g
                 - self.__custo_fixo_total - self.__b*self.__precomp)

        return lucro

    def __calcular_valor_fixo_total(self):
        """
        Somará os 5 valores que compõem o custo fixo.
        """
        self.__table_name = 'custo_fixo'
        lista_info_custos_fixos = self.__pegar_informacao_do_bd()

        soma_valores = Decimal()

        # pegará  as 5 ultimas informações da coluna 'valor' e adicionará em uma  lista
        for info in lista_info_custos_fixos[-5:]:
            # info[0]- id, info[1]- nome, info[2]- valor
            soma_valores += Decimal(info[2])

        self.__custo_fixo_total = soma_valores

    def __calcular_quantos_produtos_podem_ser_feitos(self):
        """
        usará a formula: C(q) = custo_fixo + valor_materia_prima.q
        A função também calculará o valor total que será gasto.
        Além de ter 2 checks para saber se o programa central deve continuar.
        """

        self.__table_name = 'empresa'
        list_infos_precoMP_capital = self.__pegar_informacao_do_bd()

        ultima_linha_da_tabela = list_infos_precoMP_capital[-1]

        self.__precomp = Decimal(ultima_linha_da_tabela[1])
        capital = Decimal(ultima_linha_da_tabela[2])

        if capital <= self.__custo_fixo_total:
            self.__estoque_possivel = 1
            self.capital_insuf = True

        else:
            if self.__precomp == 0:
                self.__estoque_possivel = 99999999

            else:
                self.__estoque_possivel = (capital - self.__custo_fixo_total) // self.__precomp

                if self.__estoque_possivel == 0:
                    self.capital_insuf = True

            self.__custo_total = (self.__custo_fixo_total + self.__precomp * self.__estoque_possivel)

    def __calcular_preco_medio_do_produto(self):
        """
        Usará a formula: Pm = (custo_total)/estoque
        """
        self.__preco_medio = self.__custo_total / self.__estoque_possivel

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

            column = f'INSERT INTO {self.__table_name} ({self.__columns_names}) VALUES ({self.__s_repetitions_str})'
            data = self.__lines_info

            cursor.execute(column, data)
            mydb.commit()

            cursor.close()
            mydb.close()
