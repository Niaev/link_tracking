# imports
import re

from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup

# track_links recebe a URL de uma página e retorna todos os links presentes na página, dentro de um documento de texto.
def track_links(url=None):

    # input
    if url == None:
        url = input('Digite a URL da página que deseja raspar: ')

    # tratamento de erro...
    try:
        # url open
        html = urlopen(url)

    # em caso de valor que não é URL
    except ValueError:
        print('URL inválido')

    # caso tenha ocorrido um erro HTTP
    except HTTPError as e:
        print(e)

    # em caso de valor que é URL, mas domínio incorreto ou servidor offline
    except URLError:
        print('Servidor indiponível ou domínio incorreto.')

    # caso nenhum erro tenha ocorrido...
    else:

        # lê toda a página e recebe todos os elementos do HTML5 nela presentes
        res = BeautifulSoup(html.read(), 'html5lib')

        # recebe todas as tags <a>
        a_links = res.findAll('a')

        # expressão regular que busca o link em um href="link"
        p = r'href="([\w\.\/#-:;?=~]*)"'

        a_links

        # busca pelos links dentro das tags e adiciona na lista links
        links = []
        for l in a_links:
            search = re.search(p, str(l)).group(1)
            match = re.match(r'[#/]', search)
            
            # trata dos tipos de url. Ex: #about, /files/index.php, //docs.python.org/, etc
            if re.match(r'[#]', search):
                links.append(url + search)
            elif re.match(r'//', search):
                links.append('https:' + search)
            elif re.match(r'/', search):
                links.append(url[0:-1] + search)
            elif re.match(r'http', search):
                links.append(search)

        # cria uma lista em que cada item da lista é uma lista que possui url e título da página correspondente ao url
        links_wtitle = []
        for l in links:
            try:
                html_title = urlopen(l)
            except Exception:
                print('Não foi possível acessar este link: ' + l)
            else:
                res_title = BeautifulSoup(html_title.read(), 'html5lib')
                
                if res_title.title == None:
                    print([l, l])
                    links_wtitle.append([l, l])
                else:
                    print([l, res_title.title.getText()])
                    links_wtitle.append([l, res_title.title.getText()])

        # adiciona os itens de links no arquivo links.txt
        f = open('links.txt', 'a', encoding='utf-8')
        i = 0
        for l in links_wtitle:
            f.write(str(i) + ';' + l[0] + ';' + l[1] + '\n')
            i += 1
        f.close()

if __name__ == '__main__':
    track_links()