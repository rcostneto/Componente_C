# Minha API COMPONENTE_C

Este projeto foi pensado em atender a demanda de uma *Oficina_de_Peças* **VS Veiculos**, onde se realiza concerto e manutenção de veículos,
Componente_A(API principal) recebe dados de veículo do Componente_B(API externa) e peças do Componente_C(API externa).

```
    Essa API COMPONENTE_C é usada para fazer o cadastro, exclusão e edição de peças usadas na Componente_A(API principal) Oficina de Peças.
```
Logo abaixo informa como executar a API.

---
## Como executar 


Após efetuar o download do repositório e com o VSCode aberto, abra a pasta Gerenciamento peças oficina, clicando em Arquivo/Abrir Pasta.
Em seguida clique com o botao direio do mouse em backend e com o esquerdo Abrir no Terminal Integrado.

> Não é obrigatório mas será recomendado usar o virtualenv, uma vez que o projeto foi elaborado com essa ferramenta.
 [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

Digite o comando abaixo no terminal para instalar o virtualenv
```
python3 -m venv env
```

Com o env instalado agora iremos ativá-lo.
```
./env/Scripts/activate
```

agora iremos instalar todas as libs/bibliotecas python listadas no `requirements.txt` instaladas.
```
(env)$ pip install -r requirements.txt
```
>*Após instalar as libs é recomendado que faça uma atualização do comando* `pip`
>>python.exe -m pip install --upgrade pip

Antes de iniciar o Docker é recomendável que execute o flask para criar o arquivo sqlite com as tabelas.
```
    flask run --host 0.0.0.0 --port 8000
```
Com o arquivo do banco criado, saia do flask com o comando abaixo.
```
    CTRL + C
```

---
## Como executar através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

>*Você pode instalar o docker para VSCode via terminal com o seguinte comando*
>>pip3 install docker

Vá até o diretório que contém o Dockerfile e o requirements.txt no terminal.
    Antes de criar a imagem é necessário criar uma rede para que haja comunicação entre conteiners;
        >>criar rede com o nome "oficina"
            ```
            >>>$ docker network create --driver=bridge oficina
            ```

>**Componente_A**;
>>Execute **como administrador** o seguinte comando para construir a imagem Docker da Componente_A(API principal):

```
$ docker build -t rest-c .
```

Para executar o container basta executar, **como administrador**, expecificando o nome e a rede.

```
$ docker run -d -p 8000:8000 --name peca --network oficina -v /c/Users/RCNeto/Desktop/mvp_desenvolvimento_backend_avancado/rest_api_suprimentos_c/database:/app/database rest-c
>>>>>>obs: o comando anterior se refere ao mapeamento com o docker da pasta database que esta na maquina local(area de trabalho), para que a imagem que esta no docker com o banco db.sqlite3 consiga atualizar o mesmo banco na maquina local.
```
---
### Alguns comandos úteis do Docker

>**Para verificar se a imagem foi criada** você pode executar o seguinte comando:
>
>```
>$ docker images
>```
>**Traz uma lista incluindo a imagem e o conteiner** você pode executar o seguinte comando:
>
>```
>$ docker ps
>```
>**Para verificar se o conteiner foi criado** você pode executar o seguinte comando:
>
>```
>$ docker exec -ti <NOME_IMAGE>
>```
>**Para verificar o conteudo do arquivo que consta na pasta** você pode executar o seguinte comando:
>
>```
>$ tail -f <NOME_ARQUIVO>
>>>Obs: Antes de acessar o conteudo do arquivo, é necessário entrar na pasta que se encontra o arquivo com o comando(cd nome_da_pasta).
>```

>
> Caso queira **remover uma imagem**, basta executar o comando:
>```
>$ docker rmi <IMAGE ID>
>```
>Subistituindo o `IMAGE ID` pelo código da imagem
>
>**Para verificar se o container está em exceução** você pode executar o seguinte comando:
>
>```
>$ docker container ls --all
>```
>
> Caso queira **parar um conatiner**, basta executar o comando:
>```
>$ docker stop <CONTAINER ID>
>```
>Subistituindo o `CONTAINER ID` pelo ID do conatiner
>
>
> Caso queira **destruir um conatiner**, basta executar o comando:
>```
>$ docker rm <CONTAINER ID>
>```
>Para mais comandos, veja a [documentação do docker](https://docs.docker.com/engine/reference/run/).

---

#### **GET/busca_peca**

Com o Swagger aberto iremos a procura da rota GET/busca_peca para procurar por peças cadastradas no banco.
```
Clique em "Try it out", em seguida, clique em execute para buscar dados das peças como(nome_peca, modelo_peca e cod_peca).
```

>Obs: *Os dados serão exibidos no banco* tanto via terminal quanto swagger.

>Cod:200 - Não há peças cadastradas, retornará uma [].
>Cod:200 - peças encontradas.

---

#### **DELETE/peca**

Deleta uma peça a partir do id informado

```
Clique em "Try it out", em seguida escolha o id, depois clique em execute para deletar os dados das peças como(nome_peca, modelo_peca e cod_peca).
```

>Obs: *Os dados serão deletados do banco* e será exibida a confirmação tanto via terminal quanto swagger.

>Cod:200 - Peça deletada.
>Cod:404 - Peça não encontrada na base.

---

#### **POST/peca**

Adiciona uma nova peça a base de dados.

```
Clique em "Try it out", em seguida preencha os campos, depois clique em execute para adicionar os dados das peças como(nome_peca, modelo_peca e cod_peca).
```

>Obs: *Os dados serão adicionados ao banco* e será exibida a confirmação tanto via terminal quanto swagger.

>Cod:200 - Adicionado peça.
>Cod:409 - Peça de mesmo nome e marca já salvo na base.
>Cod:400 - Não foi possível salvar nova peça.

---

#### **GET/pecas**

Faz uma busca por uma peça a partir de seu nome.

```
Clique em "Try it out", em seguida digite o nome da peça, depois clique em execute para buscar os dados das peças como(nome_peca, modelo_peca e cod_peca).
```

>Obs: *Os dados serão encontrados no banco* e será exibida a confirmação tanto via terminal quanto swagger.

>Cod:200 - Peça encontrada.
>Cod:404 - Peca não localizado no banco.

---

#### **GET/pecasapi**

Faz uma busca por todas as peças cadastradas no banco.

```
Clique em "Try it out", em seguida, clique em execute para buscar os dados das peças como(nome_peca, modelo_peca e cod_peca).
```

>Obs: *Os dados serão encontrados no banco* e será exibida a confirmação tanto via terminal quanto swagger.

>Cod:200 - Peças, retorna uma [].
>Cod:404 - Pecas encontradas.

---


#### **PUT/updatePeca**

Edita uma peça já salva no banco.

```
Clique em "Try it out", em seguida preencha os campos com o id da peça que deseja editar, clique em execute para alterar os dados das peças como(nome_peca, modelo_peca e cod_peca).
```

>Obs: *Os dados serão editados no banco* e será exibida a confirmação tanto via terminal quanto swagger.

>Cod:200 - Editada peça de id.
>Cod:400 - Não foi possível salvar novo item.

---




