export DIR_UPLOAD="/var/www/normativas-v02/storage/app/public/uploads"
export URL_BASE="http://normativas-v02.com/api/documentos/"
export PDI_ROOT="/home/thiago/desenv/pentaho/pdi-ce-8.2.0.0-342/data-integration"
export ETL_ROOT="/home/thiago/desenv/Normativas/normativas-crawlers-etl/etl"


cd $PDI_ROOT
./kitchen.sh /file $ETL_ROOT/SP.kjb
