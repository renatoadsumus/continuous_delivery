#!/bin/sh

DIRETORIO_SCRIPTS="$DIRETORIO_SCRIPTS"

cd ..
WORKDIR=`pwd`

echo "###########################"
echo "# Convertendo arquivos para o formato Linux"
echo "###########################"

for file in `find . ! -path "*/.svn/*" -type f`; do
	dos2unix ${file}
done

echo "###########################"
echo "# Criando arquivo httpd.tgz"
echo "###########################"

cd apache/opt/httpd
tar -cvzf "${WORKDIR}/httpd.tgz" --exclude=".project" --exclude-vcs .
ERROR_STATUS=$?

if [ ${ERROR_STATUS} != 0 ]; then
	echo ""
	echo ""
	echo "NAO CRIOU O PACOTE TGZ. "
	echo " 	- REEXECUTE O COMMIT STAGE E CASO O ERRO OCORRA NOVAMENTE ENTRE EM CONTATO COM A EQUIPE DE QA."
	echo ""
	echo ""
	exit 1
fi

cd "${WORKDIR}"

cp ${DIRETORIO_SCRIPTS}/bin/* .

zip httpd httpd.tgz jenkins_deploy_apache.sh deploy_http.sh
ERROR_STATUS=$?

if [ ${ERROR_STATUS} != 0 ]; then
	echo ""
	echo ""
	echo "NAO GEROU O ZIP. "
	echo " 	- REEXECUTE O COMMIT STAGE E CASO O ERRO OCORRA NOVAMENTE ENTRE EM CONTATO COM A EQUIPE DE QA."
	echo ""
	echo ""
	exit 1
fi