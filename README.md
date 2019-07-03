# normativas-crawlers-etl

=======
## Introdução
Projeto para extração dos documentos para a plataforma Normativas.

h3 Workflow
A extração está sendo realizada através da manipulação da página com Python e API do BeatifulSoup. A saída desse processo inicial é um arquivo .CSV

O arquivo é lido através de um processo de ETL construído no Petanho Data Integration(PDI) para transformação e carga de dados no domínio da aplicaçãpo Normativas. Um modelo CSV encontra-se anexado ao projeto. Priorizar Título, Data, Documento(link), Tipo, Data, Ementa.

## Python
Scripts criado em python com a biblioteca do BeatifulSoup.
https://www.crummy.com/software/BeautifulSoup/bs4/doc/

## ETL
* Pentaho Data Integration (8.2)
* Link <https://sourceforge.net/projects/pentaho/files/Pentaho%208.2/client-tools/pdi-ce-8.2.0.0-342.zip/download>
* Os ETLs devem ser executados via Pan e Kitchen
* Configurar variáveis de ambiente PDI_ROOT e ETL_ROOT

## Produção

* Copiar o arquivo kettle.properties para ~/.kettle/. [~] é a pasta do usuário no SO;
* Alterar as propriedades do arquivo para ambiente de produção.
* Remover o https do servidor

## Execução dos comandos
* As cargas prontas possuem scripts .sh de execução;
* Para limpar uma carga, basta executar o clear-cee.sh, passando a sigla do conselho como parâmetro, por exemplo CEE-AL
./clear-cee.sh CEE-AL
