## 1. Problema de negócio

Contexto do Problema de Negócio

Parabéns! Você acaba de ser contratado como Cientista de Dados da empresa Fome Zero, e a sua principal tarefa nesse momento é ajudar o CEO Kleiton Guerra a identificar pontos chaves da empresa, respondendo às perguntas que ele fizer utilizando dados!

A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.

### Geral
	1. Quantos restaurantes únicos estão registrados?
	2. Quantos países únicos estão registrados?
	3. Quantas cidades únicas estão registradas?
	4. Qual o total de avaliações feitas?
	5. Qual o total de tipos de culinária registrados?

### Pais
	1. Qual o nome do país que possui mais cidades registradas?
	2. Qual o nome do país que possui mais restaurantes registrados?
	3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?
	4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?
	5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
	6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?
	7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?
	8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?
	9. Qual o nome do país que possui, na média, a maior nota média registrada?
	10. Qual o nome do país que possui, na média, a menor nota média registrada?
	11. Qual a média de preço de um prato para dois por país?

### Cidade
	1. Qual o nome da cidade que possui mais restaurantes registrados?
	2. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?
	3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?
	4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
	5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?
	6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?
	7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas?
	8. Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?

### Restaurantes
	1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
	2. Qual o nome do restaurante com a maior nota média?
	3. Qual o nome do restaurante que possui o maior valor de uma prato para duas pessoas?
	4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação?
	5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação?
	6. Os restaurantes que aceitam pedido online são também, na média, os  restaurantes que mais possuem avaliações registradas?
	7. Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?
	8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas (BBQ)?

### Tipos de Culinária
	1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?
	2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?
	3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação?
	4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a menor média de avaliação?
	5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a maior média de avaliação?
	6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a menor média de avaliação?
	7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a maior média de avaliação?
	8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a menor média de avaliação?
	9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a maior média de avaliação?
	10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a menor média de avaliação?
	11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas pessoas?
	12. Qual o tipo de culinária que possui a maior nota média?
	13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas?

O CEO também pediu que fosse gerado um dashboard que permitisse que ele
visualizasse as principais informações das perguntas que ele fez. O CEO precisa
dessas informações o mais rápido possível, uma vez que ele também é novo na
empresa e irá utilizá-las para entender melhor a empresa Fome Zero para conseguir
tomar decisões mais assertivas.
Seu trabalho é utilizar os dados que a empresa Fome Zero possui e responder as
perguntas feitas do CEO e criar o dashboard solicitado.

## 2 - Premissas assumidas para a análise

	1- Marketplace foi o modelo de negócio assumido
	2- As 3 Visões do negócio foram: Visão País, Visão Cidades e Visão Tipos de Culinária e Restaurantes

	3 - Estratégia da solução

O painel estratégico foi desenvolvido utilizando as metricas que refletem as 3 principais visões do modelo de négio da empresa:

	1- Visão da distribuição do serviço prestado por País
	2- Visão da distribuição do serviço prestado por Cidade
	3- Visão do rank por Tipos de Culinária e Restaurantes

Cada Visão é representada pelo seguinte conjunto de métricas.

### 1- Visão da distribuição do serviço prestado por País

	a) Quantidade de restaurante por país 
	b) Quantidade de Cidade por país
	c) Média de avaliações feitas por país
	d) Média de preço de um prato para 2 pessoas por país
	e) Média de avaliação por país 
	f) Quantidade de culinária distinta por país
	g) Quantidade de Restaurante com tipo de preço 4 por país
	h) Rank dos países com mais restaurantes que fazem entrega
	i) Rank dos países com mais restaurantes que aceitam pedidos online
	j) Rank dos países com mais restaurantes que aceitam reserva

### 2- Visão da distribuição do serviço prestado por Cidade

	a) Quantidade de restaurante por Cidade 
	b) Restaurantes com avaliação acima de 4 por Cidade
	c) Restaurantes com avaliação menor que 2,5 por Cidade
	d) Restaurantes com culinária distinta por Cidade
	h) Rank das cidades com mais restaurantes que fazem entrega
	i) Rank das cidades com mais restaurantes que aceitam pedidos online
	j) Rank das cidades com mais restaurantes que aceitam reserva

### 3- Visão do rank por Tipos de Culinária e Restaurantes

	a) Tipos de Culinária com maior média de avaliação 
	b) Tipos de Culinária com maior nota de avaliação
	c) Tipos de Culinária que aceitam pedidos online e fazem entrega
	d) Resturantes com maior média de avaliação 
	e) Resturantes com maior número de avaliação
	f) Resturantes com maior valor de um prato para 2 pessoas

## 4- Top 3 Insigths
	O países com mais restaurantes não são aqueles que entregam o maior número de avaliações
	Um prato mais caro não esta realzionado as maiores médias de valiação por páis
	Ter uma grande quantidade de pratos distintos não faz a cidade obter uma nóta média acima de 4

## 5- O produto final do projeto

	Painel online, hospedado em um cloud e disponivel ara acesso em qualquer dispositivo conectado a internet.
	
	O painel pode ser acessado através do link: https://brunohenrique-bruno-henrique-ftc-projeto-final-home-nbonw8.streamlit.app/

## 6- Conclusão
	O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para que o CEO tenha um retrato da distribuição dos restaurantes cadastrados, assim como o comparar as avaliações entre eles.

## 7- Próximos passos
	1- Reduzir o número de metricas
	2- Adicionar novas visões de negócio
