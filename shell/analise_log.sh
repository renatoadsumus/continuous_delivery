#!/bin/bash

echo ""
echo ""

JAR_ANALISADOR_LOGS="/opt/analisador-log-1.2.0.jar"
DATA_HORA_INICIO_ANALISE=$(grep -o '[0-9\:\ -]*' data-hora-deploy.properties)

## PARAMETROS ======================================================

Servidor=$1
DiretorioCompartilhamento=$2
PerfilExecucao=$3
QuantidadeTop=$4


## VALIDACAO =====================================================

if [ $# -ne 4 ]; then
        echo ""
        echo "########################"
        echo "## QUANTIDADE DE PARAMETROS INVALIDOS [Voce informou: $# parametros]"
        echo "########################"
        echo ""

        exit 1;
fi


mkdir analise

scp -r ${Servidor}:${DiretorioCompartilhamento}/mix/busca-classificados.log analise/
java -cp ${JAR_ANALISADOR_LOGS} core.Processar ./analise/busca-classificados.log analise GRAILS ${PerfilExecucao} "${DATA_HORA_INICIO_ANALISE}" ${QuantidadeTop} "" ""

scp -r ${Servidor}:${DiretorioCompartilhamento}/mix/busca-mix.log analise/
java -cp ${JAR_ANALISADOR_LOGS} core.Processar ./analise/busca-mix.log analise GRAILS ${PerfilExecucao} "$DATA_HORA_INICIO_ANALISE" ${QuantidadeTop} "" ""

scp -r ${Servidor}:${DiretorioCompartilhamento}/mix/definicoes-sistema.log analise/
java -cp ${JAR_ANALISADOR_LOGS} core.Processar ./analise/definicoes-sistema.log analise GRAILS ${PerfilExecucao} "$DATA_HORA_INICIO_ANALISE" ${QuantidadeTop} "" ""

scp -r ${Servidor}:${DiretorioCompartilhamento}/mix/hibernate.log analise/
java -cp ${JAR_ANALISADOR_LOGS} core.Processar ./analise/hibernate.log analise GRAILS ${PerfilExecucao} "$DATA_HORA_INICIO_ANALISE" ${QuantidadeTop} "" ""

scp -r ${Servidor}:${DiretorioCompartilhamento}/mix/mail-service.log analise/
java -cp ${JAR_ANALISADOR_LOGS} core.Processar ./analise/mail-service.log analise GRAILS ${PerfilExecucao} "$DATA_HORA_INICIO_ANALISE" ${QuantidadeTop} "" ""

scp -r ${Servidor}:${DiretorioCompartilhamento}/mix/system-out.log analise/
java -cp ${JAR_ANALISADOR_LOGS} core.Processar ./analise/system-out.log analise GRAILS ${PerfilExecucao} "$DATA_HORA_INICIO_ANALISE" ${QuantidadeTop} "" ""

scp -r ${Servidor}:${DiretorioCompartilhamento}/access_log.log analise/
java -cp ${JAR_ANALISADOR_LOGS} core.Processar ./analise/access_log.log analise WEBLOGIC ${PerfilExecucao} "$DATA_HORA_INICIO_ANALISE" ${QuantidadeTop} " /mais/" ""
