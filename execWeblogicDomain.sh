#!/bin/bash

# Parametros de Ambiente
WLST_HOME=C:/Oracle/Middleware/wlserver_10.3/common/bin

#------------------------------------------------------------------

export WLST_HOME

#------------------------------------------------------------------

echo "Executando a criacao do Domain" #>>$STDOUT
wlst scripts/criarDomain.py