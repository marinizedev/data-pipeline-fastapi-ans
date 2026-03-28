# Interface de API

Este documento descreve as decisões técnicas relacionadas à construção da API responsável por disponibilizar os dados processados no pipeline.

O objetivo da API é permitir acesso estruturado às informações de operadoras e despesas, possibilitando consultas paginadas, filtros e análises estatísticas de forma performática e organizada.

---

## Identificador das Operadoras

Embora o dataset contenha o campo CNPJ, esse identificador encontra-se parcialmente mascarado na fonte de dados.

Por esse motivo, foi utilizado o campo:

`reg_ans`

como identificador único das operadoras, por apresentar consistência e unicidade entre os registros.

Essa escolha garante integridade referencial entre as tabelas e estabilidade nas consultas da API.

---

## Escolha do framework

Framework utilizado:

`FastAPI` 

### Justificativa

O FastAPI foi escolhido por oferecer:
- alta performance baseada em ASGI
- sintaxe simples e moderna
- validação automática de dados
- geração automática de documentação interativa (Swagger/OpenAPI)
- fácil integração com Python e SQLAlchemy

A escolha contribui para um backend mais organizado, com menor necessidade de código repetitivo e maior clareza na definição das rotas.

---

## Estratégia de Paginação

Abordagem utilizada:

paginação baseada em offset

Exemplo de parâmetros:
- page
- limit

### Justificativa:

A paginação por offset apresenta:
- implementação simples 
- boa compatibilidade com consultas SQL tradicionais
- facilidade de consumo no frontend
- desempenho adequado ao volume de dados do projeto

Essa abordagem reduz a quantidade de dados retornados por requisição, melhorando tempo de resposta da API.

---

## Estratégia de Cálculo das Estatísticas

As métricas estatísticas são previamente calculadas durante a etapa de transformação de dados, utilizando Python e Pandas, e posteriormente armazenadas na tabela `despesas_agregadas`.

A API realiza consultas diretamente nesses dados já processados.

### Justificativa:

- reduz custo computacional nas requisições da API
- melhora tempo de resposta
- evita recálculo desnecessário das métricas
- mantém consistência entre análises e dados disponibilizados
- simplifica a lógica das rotas da API

Essa abordagem mantém a API mais performática e garante alinhamento com o pipeline de dados.

---

## Estrutura de resposta da API

Formato adotado:

```json
{
  "data": [],
  "page": 1,
  "limit": 10,
  "total": 100
}
```

### Justificativa:

A inclusão de metadados junto aos dados permite:
- implementação simples de paginação no frontend
- redução de chamadas adicionais à API
- melhor controle da navegação entre páginas
- padronização das respostas

---

## Estratégia de Busca

A busca foi implementada no servidor.

Campos suportados:
- reg_ans
- razao_social

### Justificativa:

A busca no backend evita:
- transferência de grandes volumes de dados para o cliente
- processamento desnecessário no frontend
- degradação de performance em tabelas extensas

Essa abordagem melhora escalabilidade e eficiência das consultas.

---

## Performance das Consultas

Estratégias adotadas:
- paginação no backend
- limitação de registros retornados por requisição
- uso de índices nas colunas utilizadas em filtros
- separação entre dados consolidados e agregados

Essas medidas reduzem tempo de resposta e melhoram a experiência de consumo da API.

## Tratamento de Estados da Aplicação

A API foi estruturada para permitir tratamento adequado dos seguintes estados:

### carregamento

Retorno estruturado que permite exibição de indicador de loading no cliente

### erro

Retorno de mensagens claras em casos de falha de consulta ou parâmetros inválidos

### ausência de resultados

Retorno de lista vazia quando não há correspondência para os filtros informados.

Essa padronização facilita integração com diferentes interfaces de consumo.

---

## Escopo da Interface de Consumo

A API foi desenvolvida de forma independente da interface gráfica, permitindo integração com diferentes clientes, como:
- aplicações web
- dashboards analíticos
- notebooks Python
- ferramentas de BI

Essa separação mantém o projeto modular e facilita evolução futura.

---

## Observações Técnicas

O desenvolvimento da API priorizou:
- clareza estrutural
- simplicidade de manutenção
- compatibilidade com o pipeline de dados
- organização das rotas
- padronização das respostas
- facilidade de expansão futura

A integração entre Python, SQL e FastAPI permitiu construir uma camada de acesso aos dados consistente e reutilizável.