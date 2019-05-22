#export PDI_ROOT="/home/thiago/desenv/pentaho/pdi-ce-8.2.0.0-342/data-integration"
#export ETL_ROOT="/home/thiago/desenv/Normativas/normativas-crawlers-etl/etl"

#PARAM_CEE, por exemplo: CEE-AL, CEE-ES
cd $PDI_ROOT
./pan.sh /file $ETL_ROOT/clearCEE.ktr -param:PARAM_CEE=$1
