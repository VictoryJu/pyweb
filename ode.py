from pyoembed import oEmbed, PyOembedException

data = oEmbed('https://www.instagram.com/p/BUawPlPF_Rx/',maxwidth=640, maxheight=480)
print(data)