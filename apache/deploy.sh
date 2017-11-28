#!/bin/sh
GO_PIPELINE_NAME="$GO_PIPELINE_NAME"

echo "###########################"
echo "# Descompactando o httpd.zip"
echo "###########################"

cd ..
cd cruise-output

unzip httpd.zip
ERROR_STATUS=$?

if [ ${ERROR_STATUS} != 0 ]; then
	echo ""
	echo ""
	echo "NAO DESCOMPACTOU O ZIP. "
	echo " 	- ENTRE EM CONTATO COM A EQUIPE DE QA."
	echo ""
	echo ""
	exit 1
fi

scp -r httpd.tgz jenkins_deploy_apache.sh deploy_http.sh tfsservice@infojenkins2:/home/tfsservice/${GO_PIPELINE_NAME}
ERROR_STATUS=$?

if [ ${ERROR_STATUS} != 0 ]; then
	echo ""
	echo ""
	echo "FALHA AO TRANSFERIR OS ARQUIVOS "
	echo " 	- ENTRE EM CONTATO COM A EQUIPE DE QA."
	echo ""
	echo ""
	exit 1
fi

ssh tfsservice@infojenkins2 "cd $GO_PIPELINE_NAME; chmod +x ./jenkins_deploy_apache.sh; dos2unix jenkins_deploy_apache.sh; ./jenkins_deploy_apache.sh \"$GO_PIPELINE_NAME\""
ERROR_STATUS=$?

if [ ${ERROR_STATUS} != 0 ]; then
	echo ""
	echo ""
	echo "FALHA AO EXECUTAR O DEPLOY NO AMBIENTE "
	echo " 	- ENTRE EM CONTATO COM A EQUIPE DE QA."
	echo ""
	echo ""
	exit 1
fi