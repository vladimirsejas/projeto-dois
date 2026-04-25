# Projeto LGPD com Python, SQLAlchemy e Pandas

Este projeto implementa um fluxo completo de acesso, tratamento e exportação de dados pessoais com base nos princípios da LGPD. O sistema realiza leitura de dados em banco PostgreSQL, anonimização de informações sensíveis, geração de arquivos CSV e medição de tempo de execução.
O código está dividido em módulos para separar responsabilidades e garantir organização, reutilização e manutenção. Sendo a forma que aprendi e acho mais seguro e lógico para estrurar  o código tangto para correções futuras quando para compreensão e segurança.

## Bibliotecas utilizadas

SQLAlchemy é responsável pela conexão com o banco de dados e execução de consultas SQL. Ele abstrai o acesso ao banco permitindo trabalhar com Python ao invés de SQL puro, embora neste projeto também seja utilizado SQL direto via text.
Pandas é utilizado para estruturar os dados em formato de DataFrame e facilitar a manipulação, filtragem por ano e exportação para arquivos CSV.functools.
wraps é utilizado dentro do decorador para preservar os metadados da função original, como nome e documentação. Sem isso, a função decorada perderia sua identidade.Uso de functools.wraps no decorador
O projeto utiliza um decorador para medir o tempo de execução das funções principais. Dentro desse decorador é utilizado o recurso functools.wraps.
O wraps tem a função de preservar as informações originais da função que está sendo decorada. Quando um decorador é aplicado, a função original é substituída internamente por uma nova função chamada wrapper. Sem o uso de wraps, essa substituição faz com que a função perca sua identidade original.
Isso significa que atributos importantes como o nome da função, documentação e assinatura seriam alterados. Por exemplo, a função exportar_todos passaria a ser identificada como wrapper, o que dificulta depuração, leitura de logs e entendimento do fluxo do programa.
O uso de @wraps(func) resolve esse problema ao copiar os metadados da função original para a função wrapper. Dessa forma, mesmo após a aplicação do decorador, a função mantém seu nome, documentação e outras características importantes.
No contexto deste projeto, isso é relevante porque o sistema registra logs de execução e utiliza funções separadas para diferentes responsabilidades. Manter a identidade correta das funções garante que os registros de log sejam claros, facilita a manutenção do código e preserva a rastreabilidade do comportamento do sistema.
Além disso, o uso de wraps segue boas práticas de desenvolvimento em Python, especialmente em projetos modulares onde decoradores são utilizados para adicionar comportamento sem alterar a lógica principal das funções.
logging é utilizado para registrar o tempo de execução das funções em arquivo de log.

## Estrutura do projeto e separação de responsabilidades

O código foi separado em arquivos diferentes para evitar acoplamento excessivo e facilitar manutenção.
lgpd.py é responsável pela conexão com o banco e pela lógica de anonimização dos dados. Ele centraliza as regras de proteção de dados.
atividade4.py contém o decorador medir_tempo. Sua função é interceptar chamadas de funções e medir quanto tempo elas levam para executar.

atividade2.py implementa a exportação dos dados anonimizados por ano de nascimento.

atividade3.py implementa a exportação de todos os registros sem anonimização, contendo apenas nome e CPF.

Essa separação garante que cada módulo tenha uma única responsabilidade, evitando código duplicado e permitindo reutilização.

## Interligação entre os módulos

O sistema funciona de forma integrada.
atividade2 e atividade3 utilizam a conexão com o banco definida em lgpd.py através do objeto engine.

atividade2.py utiliza também a função LGPD para anonimizar os dados antes de exportar.

atividade4.py fornece o decorador medir_tempo, que é aplicado nas funções principais de atividade2 e atividade3 para registrar o tempo de execução.

Dessa forma, existe uma dependência clara:
lgpd.py fornece dados e regras de anonimização
atividade4.py fornece controle de execução e logging
atividade2.py  e atividade3.py  executam a lógica principal de exportação

## Correlação entre as atividades

A atividade2.py gera múltiplos arquivos separados por ano de nascimento, com dados anonimizados. 

A atividade3py gera um único arquivo contendo todos os registros, sem anonimização e apenas com nome e CPF. 

A atividade 4.py adiciona a medição de tempo de execução às atividades 2 e 3 utilizando um decorador. 

Ou seja, a atividade4.py não executa lógica de negócio diretamente, mas envolve as outras duas atividades para monitorar desempenho.

## Funcionamento do decorador

O decorador medir_tempo envolve a função original e executa três etapas

captura o tempo antes da execução
executa a função original
captura o tempo após execução

A diferença entre os tempos é registrada em log e exibida no console. 

## Processo de anonimização

A anonimização é realizada na função LGPD. 

Nome é dividido em partes e apenas a primeira letra do primeiro nome é mantida, o restante é substituído por asteriscos.
CPF mantém os três primeiros dígitos e substitui o restante por máscara.
Email mantém apenas o primeiro caractere do usuário antes do @ e preserva o domínio.
Telefone mantém apenas os últimos quatro dígitos.
Essas transformações garantem que os dados não possam ser facilmente identificados, mantendo apenas parte da informação útil.

## Fluxo geral do sistema

Conecta ao banco de dados
Consulta os dados da tabela usuarios
Aplica anonimização quando necessário
Organiza os dados em DataFrame
Filtra ou transforma conforme a atividade
Exporta para CSV
Registra tempo de execução em log

## Logs

O tempo de execução das funções é registrado automaticamente no arquivo tempo_execucao.log. 

Isso permite análise de desempenho e comparação entre execuções.

## Conclusão

O projeto demonstra a aplicação prática de conceitos de proteção de dados, modularização de código, uso de decoradores e manipulação de dados em Python, mantendo separação clara de responsabilidades e integração entre os módulos.
