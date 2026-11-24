# Builds available/index.html from index.html: same look and data, but only "Available now" / "Available from <date>" cards.
import re, os
s = open('index.html').read()
s = s.replace('<!--PAGE-CONFIG-->', '<script>window.COHOST_BASE="../";window.COHOST_ONLY_AVAILABLE=true;</script>')
s = s.replace('<script src="site-config.js"></script>', '<script src="../site-config.js"></script>')
s = s.replace('<title>Properties | Clifford The Co Host</title>', '<title>Available Now | Clifford The Co Host</title>')
s = s.replace('<h1>Our Properties. <em>Ready When You Are.</em></h1>', '<h1>Available Now. <em>Ready When You Are.</em></h1>')
s = re.sub(r'(<section class="hero">.*?<p>).*?(</p>)',
           r"\1Furnished homes that are free now or coming free soon, in Dubai and South Africa. This list updates automatically. Message me on WhatsApp about any home.\2", s, count=1, flags=re.S)
s = s.replace('<button data-f="available">Available now</button>', '<button data-f="available">Free today</button>')
s = s.replace('<a class="on hide" href="#">Properties</a>', '<a class="hide" href="../">All properties</a><a class="on hide" href="#">Available</a>')
s = s.replace('<a href="https://co-host.pro/home">co-host.pro</a></footer>',
              '<a href="../">All properties</a><a href="https://co-host.pro/home">co-host.pro</a><br><br>Powered by LaunchRiot</footer>')
os.makedirs('available', exist_ok=True)
open('available/index.html', 'w').write(s)
print('available/index.html written')
