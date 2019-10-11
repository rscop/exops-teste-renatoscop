
# GIT Autodeploy for EZOps
#### Python3

# Como usar?

### Requisitos
 - Repositório GitHub e conta com acesso ao mesmo
 - Conta previamente configurada ja no servidor e na pasta
 - Servidor linux (Feito em ubuntu 18.04)

### Como funciona?
Após a configuração da máquina de forma que atenda sua aplicação é necessário configurar alguns fatores, tanto no GH quanto no projeto para que o autoDeploy funcione de melhor forma.
É necessário que a aplicação rode na pasta Master de seu projeto.
O Webservice, por padrão, está configurado na porta 3005, então é necessário que a mesma seja liberada no servidor para não ocorrer quaisquer problemas.
Após isso é necessário a configuração no ambiente do próprio GitHub.
Acesse as configurações do seu projeto, vá em Webhooks e crie um novo:
![enter image description here](https://image.prntscr.com/image/x1RhSuRcS4S4ESW5ye-LNQ.png)
É necessário configurar alguns campos como:

 - Payload URL: Link do seu WebService 
 - Content type: json para esse caso
 - Secret: (Deixaremos em branco, mas pode ser implementado algum tipo
   de segurança)

Na parte de eventos, vamos usar apenas alguns:

 - Commit comments 
 - Branch or tag creation 
 - Pushes.

Após a configuração, o GH irá começar os dados para a URL concedia acima, e tudo pode ser acompanhando no log ao fim da página.

# Comandos:
 - -cB [branche_name] : Muda de Branch
 - -iL : Faz com que não ignore as alterações locals (Por padrão será ignorado)
 - -nD : Faz com que não dê deploy automático (Por padrão fará)

# Usabilidade:
Após realizar as alterações necessárias e enviar o commit para a base é possível um dos 3 parâmetros acima citados, caso nenhum seja passado ele irá assumir as instruções padrões.

Exemplo: 

'commit name -nD': Irá apenas enviar as modificações para nuvem, sem fazer alterações na base de produção.

# OBS:
Ao criar um branch novo, antés de fazer qualquer alteração ou commit é preciso salvar o mesmo para enviar ao github.

### Bônus:
Para melhor análise de logs, foi usando um pacote para exibição do mesmo na web:

##### Instalar a biblioteca:
sudo npm i frontail -g

##### Rodar o serviço na pasta onde está salva o log:
sudo frontail -p 3010 autodeploy.log

Vale lembrar que a porta 3010 foi aberta previamente.
O arquivo "autodeploy.log" é o nome padrão, podendo ser alterado casa haja necessidade.
