# normativas-crawlers-etl

## ETL
* Pentaho Data Integration (8.2)
* Link <https://sourceforge.net/projects/pentaho/files/Pentaho%208.2/client-tools/pdi-ce-8.2.0.0-342.zip/download>
* Os ETLs devem ser executados via Pan e Kitchen
* Configurar variáveis de ambiente PDI_ROOT e ETL_ROOT

## Produção

* Copiar o arquivo kettle.properties para ~/.kettle/
* Alterar as configurações para ambiente de produção

## Execução dos comandos
* As cargas prontas possuem scripts .sh de execução;
* Para limpar uma carga, basta executar o clear-cee.sh, passando a sigla do conselho como parâmetro, por exemplo CEE-AL
./clear-cee.sh CEE-AL
