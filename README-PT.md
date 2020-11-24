# **link_tracking**

Um simples *script* e pacote em Python que usa conceitos de *web crawling* para encontrar *links* e páginas pela internet e bancos de dados SQLite para armazenar os dados encontrados.

## **Utilizando**

Você pode clonar esse repositório Git e adicionar ao seu projeto para usar **link_tracking** [como um pacote](#como-um-pacote) or para usar o *script* [`tracker.py`](#script-tracker).

```sh
$ git clone https://github.com/Niaev/link_tracking.git
```
**O pacote não está disponível no Python Package Index ainda**

### **script `tracker`**

Esse *script* pode ser encontrado no diretório raíz do repositório. Siga o exemplo a seguir de como usá-lo:

```sh
$ python3 tracker.py SEEDS_FILE [depth]
```

* `SEEDS_FILE` - um caminho para um arquivo, que se refere a um arquivo de texto com uma lista de *links* para a internet. Exemplo:

```
http://link-one.com/
https://link.org/two
...
```

* `DEPTH` - é um parâmetro opcional, que representa um número inteiro (seu valor padrão é **2**), definindo a profundidade de busca de *links* - que é quantas vezes o algoritmo irá entrar em uma "página filho" a procurar por mais *links*, de forma recursiva

O *script* irá buscar *links* com base nas *seeds* - descritas em `SEEDS_FILE` - e irá raspar suas respectivas páginas, então irá armazenar em um banco de dados SQLite padrão: `data/pages.db`.  

### **como um pacote**

Existem dois módulos: `crawler` e `ìndexer`.

`crawler` possui funções e a classe princpal `Crawler`, responsável pelo *web crawling* de todo o algoritmo. A classe recebe uma URL e usa as bibliotecas **urllib** e **bs4** para conseguir informações da página a que a URL se refere e buscar os *links* dentro dela.

`indexer` possui apenas a classe `Indexer`, que é responsável por manipular, organizar e armazenar os dados coletador pelo `Crawler`.

O código está documentado com comentários e *docstrings*. A documentação mais completa dessa ferramenta pode ser encontrada na wiki deste repositório - **ainda não disponível**.