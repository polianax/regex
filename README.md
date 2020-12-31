# regex
Utilização de regex para classificação de despachos judicias

### Dependências:
elasticsearch~=7.9.1

### Variáveis de ambiente
ELASTICSEARCH_URL: url do servidor, Ex: ELASTICSEARCH_URL=http://localhost:9200

### Como importar os dados:
Colocar o arquivo dump (ele deve ter esse nome exato) na mesma pasta dos scripts, em seguida executar
`python upload.py`, ele criará um index com o nome data que será utilizado no processamento.

### Como processar os dados:
Após feita a importação, executar `python main.py`, os documentos serão atualizados com a propriedade tags, que contém as informações identificadas.
