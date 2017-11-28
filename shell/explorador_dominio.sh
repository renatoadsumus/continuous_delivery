#!/bin/bash

# https://www.digitalocean.com/community/tutorials/how-to-find-broken-links-on-your-website-using-wget-on-debian-7
## PARAMETROS ======================================================

Dominio=$1
Profundidade=$2


wget --no-check-certificate --spider -r -nd -nv -l ${Profundidade} -o urls_acessadas.log  ${Dominio} || echo FORAM ENCONTRADOS ERROS NA BUSCA

grep -B1 'broken link!' urls_acessadas.log

exit 0