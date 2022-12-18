# Author: DanielVii

from Coletores import ColetarInfo
from Telas import Telas
from Calculadores import Calculos

tela = Telas()

coletor = ColetarInfo()

calcular = Calculos()

tela.boas_vindas()
if tela.continuar:
    tela.entregar_informacoes_sobre_o_que_serah_requisitato()

    if tela.continuar:
        coletor.coletar_informacoes_empresa()

        if coletor.continuar:
            coletor.coletar_custos_fixos()

            if coletor.continuar:
                calcular.info_iniciais()

                if calcular.capital_insuf:
                    tela.capital_insuficiente()

                else:
                    tela.resultado_inicial()

                    if tela.continuar:
                        tela.hora_de_coletar()

                        if tela.continuar:
                            coletor.coletar_info_demanda_valor()

                            if coletor.continuar:
                                calcular.preco_ideal()

                                if calcular.valores_inconsistentes:
                                    tela.valores_incosistentes()

                                else:
                                    tela.valores_ideais()

                                    if tela.continuar:
                                        coletor.coletar_info_de_futuro_preco()

                                        if coletor.continuar:
                                            calcular.simulacao_lucro()

                                            tela.simulacao_lucro()
