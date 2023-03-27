# Desafio Alpha

### Objetivo

O objetivo do sistema é auxiliar um investidor nas suas decisões de comprar/vender ativos. Para tal, ele deve registrar periodicamente a cotação atual de ativos da B3 e também avisar, via e-mail, caso haja oportunidade de negociação.

API utilizada: Alpha Vantage (https://www.alphavantage.co/) 

### Requisitos funcionais 

#### Obrigatórios

Os seguintes requisitos funcionais são necessários:

- Obter periodicamente as cotações de alguma fonte pública qualquer e armazená-las, em uma periodicidade configurável (em minutos)  para cada túnel, para consulta posterior

 
- Expor uma interface web para permitir consultar os preços armazenados, configurar os ativos a serem monitorados e parametrizar os túneis de preço de cada ativo e periodicidade da checagem (em minutos) de cada ativo


- Enviar e-mail para o investidor sugerindo Compra sempre que o preço de um ativo monitorado cruzar o seu limite inferior, e sugerindo Venda sempre que o preço de um ativo monitorado cruzar o seu limite superior

#### Não obrigatórios

Foram adicionados os seguintes requisitos alem dos obrigatórios:

- Busca para as cotações que o usuario queira monitorar