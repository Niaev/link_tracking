# link_traking

**Link Tracking** é um script escrito em **Python** que utiliza métodos de ***Web Scrapping***, com as bibliotecas **urllib** e **BeautifulSoup**. Possui este nome pois busca e armazena todos os links possíveis - e o título das suas respectvas páginas - dentro de uma página Web.

## Como funciona

O script, ao ser executado, solicita uma URL, que será a URL da página que o usuário deseja retirar os links. O dado URL deverá ser válido e será utilizado para que o **BeautifulSoup** leia a página a que ele se refere, recebendo os elementos do HTML5. Depois o script irá buscar somente pelas tag de link ```<a></a>``` e então será extrído somente o link. Veja o exemplo:

Tag retornada pelo **BeautifulSoup**:
```
<a href="https://www.github.com/" id="link-github" class="link" target="_blank">Github</a>
```

Link extraído da tag:
```
www.github.com
```

O links são então tratados e armazenados em uma lista. Eles são tratados pois eles serão acessados pelo próprio script mais a frente e o usuário, depois que os links forem armazenados em um documento de texto, pode acessar. Agora, como eles são tratados: alguns links podem ter referencial relativo ou absoluto, o que pode dificultar o acesso pelo script e pelo usuário.

Dentro da página do [GitHub](https://www.github.com/) existe um link para o [Sobre o GitHub](https://www.github.com/about/). Se o link dentro da página estiver se referindo de maneira absoluta, não é um problema, então não precisa ser tratado, se estiver se referindo de maneira relativa, deve ser tratado. Eis aqui um exemplo do caso de referancial relativo:
```
<a href="/about/">Sobre</a>
```

O links extraído será:
```
/about/
```

O script não sabe que esse ```/about/``` é da página do GitHub e o usuário pode não saber, caso queira acessar. Sendo assim, esse link é tratado pelo script para que fique assim:
```
https://www.github.com/about/
```

Existem outros tipos de link que são tratados, como links para âncoras ou para outras páginas, mas sem usar o ```http(s)://```, que pode fazer o **BeautifulSoup** não compreender como URL, assim impossibilitando o acesso à página.

O script acessa os links que extraiu para captar informações, como título da página a que o link se refere.

Feito isso, o script armazena tudo em um arquivo de texto, ```links.txt```.

## Como usar

Para utilizar o **Link Tracking**, é necessário que você instale os [requisitos](#requisitos) e baixe o conteúdo desse repositório clicando em ```Clone or Download``` e em seguida em ```Download ZIP```, ou você pode cloná-lo, executando o seguinte comando em seu terminal:
```
$ git clone git://github.com/Niaev/link_tracking
```

### Requisitos
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - ```pip install beautifulsoup4``` ou ```python -m pip install beautifulsoup4```

### Executando o script

No terminal de seu sistema operacional, navegue até o diretório em que o script se encontra e o execute:
```
$ python __init__.py
```

Ou abra o ```__init__.py``` utilizando o [**IDLE Python**](https://www.python.org/downloads/).

Ao executar, a seguinte mensagem deve aparecer:
```
Digite a URL da página que deseja raspar: 
```

Então você digita ou cola a URL que deseja raspar e basta aguardar um tempo para verificar os links no arquivo ```links.txt```

## Faça bom uso :)