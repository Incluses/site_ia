
# Site para a ia

O site serve para prever se o usuario poderia ou não ser um usuario do app

## Documentação da API

#### Faz a previsão se a pessoa vai ser ou não um usuario

```http
  POST /would-use-app
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
comunidade	| string|	Participante da Comunidade LGBTQIA+
faixa_etaria	| string|	Faixa Etária
identidade_genero	| string|	Identidade de Gênero
orientacao_sexual	| string|	Orientação Sexual
cidade_estado	| string|	Cidade/Estado
escolaridade	| string|	Escolaridade
usa_apps_emprego	| string|	Usa Apps para Oportunidades de Emprego?
preferencia_cursos	| string|	Preferência de Cursos
desafios_emprego_genero	| string|	Desafios de Emprego por Gênero
interesse_empreender	| string|	Interesse em Empreender
situacao_mercado_trabalho	| string|	Situação no Mercado de Trabalho
usa_redes_sociais	| string|	Usa Redes Sociais?


## Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar as seguintes variáveis de ambiente no seu .env

`DB_MONGO_URL` 
`DB_MONGO_NAME` 
`DB_MONGO_COLLECTION_IA`


## Instalação das dependências

```bash
  pip install -r requirements.txt
```
    ## Feito por

[Luca Almeida Lucareli](https://github.com/LucaLucareli)

[Olivia Farias Domingues](https://github.com/oliviaworks)
