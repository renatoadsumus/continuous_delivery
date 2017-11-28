#!/bin/bash

echo ""
echo ""

## PARAMETROS ======================================================

#Aplicacao='empregos'
#AplicacaoParar=''
#Usuario='deploytst'
#Senha='d3p10y'
#Dominio='int-classificados.ogmaster.local'
#Porta='8080'
#TempoEsperar=5

Usuario=$1
Senha=$2
Dominio=$3
Porta=$4
Aplicacao=$5
AplicacaoParar=$6
TempoEsperar=$7

## VALIDACAO =====================================================

if [ $# -ne 7 ]; then
        echo ""
        echo "########################"
        echo "## QUANTIDADE DE PARAMETROS INVALIDOS [Voce informou: $# parametros]"
        echo "## Os parametros sao:"
        echo "## - Usuario de deploy do Tomcat Manager"
        echo "## - Senha do usuario de deploy do Tomcat Manager"
        echo "## - Dominio do Tomcat "
        echo "## - Porta do Tomcat "
        echo "## - Aplicacao que sera implantada"
        echo "## - Aplicacao que deve ser parada e reiniciada apos o deploy (Ex.: healtcheck) [Deixar em branco caso nao exista]"
        echo "## - Tempo de espara apos executar o deploy e parar/reninicar a aplicacao do parametro anterior "
        echo "########################"
        echo ""

        exit 1;
fi

## COMANDOS  ======================================================

ComandoListar='/manager/list'
ComandoDeploy='/manager/deploy?war=file:/tmp/'${Aplicacao}'.war&path=/'${Aplicacao}
ComandoUndeploy='/manager/undeploy?path=/'${Aplicacao}
ComandoStopHealtcheck='/manager/stop?path=/'${AplicacaoParar}
ComandoStartHealtcheck='/manager/start?path=/'${AplicacaoParar}

Credenciais=${Usuario}:${Senha}
Url=${Dominio}:${Porta}

## EXECUCAO  ======================================================

echo ""
echo "########################"
echo "## INICIANDO O DEPLOY NO TOMCAT DA APLICACAO "${AplicacaoParar}
echo "## Usuario "${Usuario}
echo "## Dominio "${Dominio}
echo "## Porta "${Porta}
echo "########################"
echo ""



if [ -n "${AplicacaoParar}" ]; then
        echo ""
        echo "########################"
        echo "## PARANDO APLICACAO "${AplicacaoParar}
        echo "########################"
        echo ""

        urlExecutar=http://${Url}${ComandoStopHealtcheck}
        curl -u ${Credenciais} ${urlExecutar} ||  exit 1

        sleep ${TempoEsperar}
fi

echo ""
echo "########################"
echo "## EXECUTANDO UNDEPLOY DA APLICACAO "${Aplicacao}
echo "########################"
echo ""

urlExecutar=http://${Url}${ComandoUndeploy}
curl -u ${Credenciais} ${urlExecutar} ||  exit 1

#echo ""
#echo "########################"
#echo "## COPIANDO O NOVO PACOTE PARA DEPLOY"
#echo "########################"
#echo ""

#comandoCopiar='cp '${Aplicacao}.war' /tmp/'${Aplicacao}.war
#echo "Comando copiar: "${comandoCopiar}
#eval ${comandoCopiar}

echo ""
echo "########################"
echo "## EXECUTANDO DEPLOY DA APLICACAO "${Aplicacao}
echo "########################"
echo ""

urlExecutar=http://${Url}${ComandoDeploy}
curl -u ${Credenciais} ${urlExecutar} ||  exit 1

sleep ${TempoEsperar}

if [ -n "${AplicacaoParar}" ]; then

        echo ""
        echo "########################"
        echo "## INICIANDO APLICACAO "${AplicacaoParar}
        echo "########################"
        echo ""

        urlExecutar=http://${Url}${ComandoStartHealtcheck}
        curl -u ${Credenciais} ${urlExecutar} ||  exit 1

        sleep ${TempoEsperar}

fi

echo ""
echo "########################"
echo "## LISTA DAS APLICACOES NO TOMCAT"
echo "########################"
echo ""

urlExecutar=http://${Url}${ComandoListar}
curl -u ${Credenciais} ${urlExecutar} ||  exit 1

echo ""
echo ""