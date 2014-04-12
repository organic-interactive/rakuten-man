import sys
import urllib, re

if (len(sys.argv) < 2):
	print "Usage: rak_man.py SEARCH+TERM [PAGENUM]"
	exit(0)
print "Search term: " + sys.argv[1]
site = None
try:
	site = "http://global.rakuten.com/en/search/?k=%s&p=%d&tl=551177" % (sys.argv[1], int(sys.argv[2]))
except:
	site = "http://global.rakuten.com/en/search/?k=%s&p=1&tl=551177" % sys.argv[1]
data = urllib.urlopen(site).read()
regex = "<div class=\"b\-content b\-fix\-2lines\"><a href=\"(.+?)\">"
regex2 = "<a href=\"/en/store/.+?/\"><img alt=\".+?\" src=\"(.+?)\" /></a>"
regex3 = "USD<span class=\"b-text-prime\">(.+?)[<\.]"
regex4 = "> Size </td>.+?</td>.+?<td valign=\"top\"> ?(.+?)<"
regex5 = "Size:(.+?)[<\"]"
regex6 = "> Size (\d+) <"
regex7 = "variant-label-\d-\d\"> Size (\d+) <"
regex8 = "Size</td>[\s\n]+<td style=\".+?\">(\d+)<"
regex9 = "size: (\d+)"
regex10 = "variant-label-\d-\d\"> (.+?) "
regex11 = "name=\"shop_url\" type=\"hidden\" value=\"(.+?)\""
regex12 = " size: size (\d+) "
regex13 = "sizes: (\d+) size"
regex14 = "size </td>[\s\n]+<td .+?>(\d+)</td>"
regex15 = "Size:\s*(\d+) "
f = open("out.html", "w")
images = re.findall(regex2, data)
if len(images) == 0:
	print "Nothing found, trying main site."
	try:
		site = "http://global.rakuten.com/en/search/?k=%s&p=%d" % (sys.argv[1], int(sys.argv[2]))
	except:
		site = "http://global.rakuten.com/en/search/?k=%s&p=1" % sys.argv[1]
data = urllib.urlopen(site).read()
images = re.findall(regex2, data)
links = re.findall(regex, data)
shops = []
links = ["http://global.rakuten.com" + link for link in links]
prices = re.findall(regex3, data)
sizes = []
for link in links:
	print "%d/%d loaded." % (links.index(link), len(links))
	data = urllib.urlopen(link).read()
	shops.append(re.findall(regex11, data)[0])
	possibility1 = re.findall(regex4, data, re.DOTALL)
	possibility2 = re.findall(regex5, data, re.DOTALL)
	possibility3 = re.findall(regex6, data)
	possibility4 = re.findall(regex7, data)
	possibility5 = re.findall(regex8, data)
	possibility6 = re.findall(regex9, data)
	possibility7 = re.findall(regex10, data)
	possibility8 = re.findall(regex12, data)
	possibility9 = re.findall(regex13, data)
	possibility10 = re.findall(regex14, data)
	possibility11 = re.findall(regex15, data)
	if len(possibility1) != 0:
		sizes.append(possibility1[0].strip().upper())
		continue
	if len(possibility11) != 0:
		sizes.append(possibility11[0])
		continue
	if len(possibility2) != 0:
		possibility2[0] = possibility2[0].upper()
		possibility2[0] = possibility2[0].replace("SIZE", "")
		sizes.append(possibility2[0].strip())
		continue
	if len(possibility3) != 0:
		sizes.append(possibility3[0].strip())
		continue
	if len(possibility4) != 0:
		new_size = ""
		for size in possibility4:
			new_size += size + " / "
		new_size = new_size[:-2]
		sizes.append(new_size.strip())
		continue
	if len(possibility5) != 0:
		sizes.append(possibility5[0])
		continue
	if len(possibility6) != 0:
		sizes.append(possibility6[0])
		continue
	if len(possibility7) != 0:
		new_size = ""
		for size in possibility7:
			new_size += size + " / "
		new_size = new_size[:-2]
		sizes.append(new_size.strip().upper())
		continue
	if len(possibility8) != 0:
		sizes.append(possibility8[0])
		continue
	if len(possibility9) != 0:
		sizes.append(possibility9[0])
		continue
	if len(possibility10) != 0:
		sizes.append(possibility10[0])
		continue
	sizes.append("UNKNOWN")
print "%d/%d loaded." % (len(links), len(links))
f.write("<link rel='stylesheet' href='stylesheet.css' type='text/css' media='screen' />")
f.write("<div align=\"center\">")
f.write("<div class='title'><h1>THE REAL RAKUTEN SITE SUCKS</h1></div><div>")
for i in range(len(images)):
	if "COLOR:" in sizes[i]:
		sizes[i] = sizes[i][:sizes[i].index("COLOR:")].strip()
	f.write("<div class=\"field-content\"><a href=\"%s\"><img src=\"%s\" /></a></div>" % (links[i], images[i]))
	f.write("<div class=\"text-data\">$%s FOR SIZE %s BY %s</div>" % (prices[i], sizes[i], shops[i]))
f.write("</div>")
f.close()
print "out.html written."