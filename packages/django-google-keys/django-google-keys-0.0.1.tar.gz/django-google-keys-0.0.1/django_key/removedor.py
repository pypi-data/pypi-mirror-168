from bs4 import BeautifulSoup as bs
def removedor(t):
    t = str(t)
    x = bs(t, 'html.parser').text
    return x