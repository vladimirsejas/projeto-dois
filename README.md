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

## Testes
Isso permite análise de desempenho e comparação entre execuções.
Os testes automatizados foram implementados utilizando o framework pytest com foco no módulo lgpd.py, responsável pela anonimização de dados sensíveis, sendo testadas as funcionalidades de anonimização de nomes, CPF, e-mail e telefone, além do funcionamento da classe LGPD e do decorador, garantindo que as funções produzam resultados corretos e consistentes para diferentes entradas; a execução dos testes pode ser realizada com o comando `python -m pytest`. A cobertura de testes foi concentrada nesse módulo porque ele contém lógica pura, ou seja, funções determinísticas que recebem dados de entrada e retornam resultados previsíveis, o que o torna adequado para testes unitários; por outro lado, os demais módulos do projeto envolvem dependência de banco de dados por meio do SQLAlchemy, operações de entrada e saída como geração de arquivos CSV e execução de efeitos colaterais como escrita em log e impressão em console, características que dificultam a aplicação de testes unitários diretos e exigem técnicas mais avançadas como mocking e testes de integração, razão pela qual foi adotada a estratégia de priorizar os testes no núcleo lógico do sistema, onde há maior previsibilidade e controle.

Os módulos atividade2.py, atividade3.py e atividade4.py não possuem testes unitários porque não apresentam as características necessárias para esse tipo de teste. Diferente do módulo lgpd.py, que contém lógica pura e determinística (recebe dados, processa e retorna sempre o mesmo resultado para a mesma entrada), esses arquivos dependem de elementos externos ao código. Nos casos de atividade2.py e atividade3.py, as funções acessam banco de dados por meio do SQLAlchemy, executam consultas reais e geram arquivos CSV, o que torna o resultado dependente do ambiente, dos dados existentes e do sistema de arquivos. Já em atividade4.py, o decorador mede tempo de execução, escreve em log e imprime no console, ou seja, produz efeitos colaterais e utiliza valores variáveis como o tempo, que não são previsíveis. Essas características impedem o isolamento necessário para testes unitários, que exigem controle total das entradas e saídas. Para testar esses módulos corretamente, seria necessário utilizar técnicas mais avançadas como mocking ou testes de integração, que não eram o foco do projeto. Por isso, os testes foram concentrados no módulo lgpd.py, onde há previsibilidade, controle e validação direta da lógica implementada.





## Conclusão

O projeto demonstra a aplicação prática de conceitos de proteção de dados, modularização de código, uso de decoradores e manipulação de dados em Python, mantendo separação clara de responsabilidades e integração entre os módulos.
