import sys
import urllib, re
print sys.argv[1]
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
regex5 = "Size:(.+?)<"
f = open("out.html", "w")
images = re.findall(regex2, data)
links = re.findall(regex, data)
links = ["http://global.rakuten.com" + link for link in links]
prices = re.findall(regex3, data)
sizes = []
for link in links:
	data = urllib.urlopen(link).read()
	possibility1 = re.findall(regex4, data, re.DOTALL)
	possibility2 = re.findall(regex5, data, re.DOTALL)
	if len(possibility1) != 0:
		sizes.append(possibility1[0].strip())
		continue
	if len(possibility2) != 0:
		sizes.append(possibility2[0].strip())
		continue
	sizes.append("UNKNOWN")
print prices
print "# links = " + str(len(links))
print "# images = " + str(len(images))
print "# prices = " + str(len(prices))
f.write("<link rel='stylesheet' href='stylesheet.css' type='text/css' media='screen' />")
f.write("<div align=\"center\">")
f.write("<div class='title'><h1>THE REAL RAKUTEN SITE SUCKS</h1></div><div>")
for i in range(len(images)):
	f.write("<div class=\"field-content\"><a href=\"%s\"><img src=\"%s\" /></a></div>" % (links[i], images[i]))
	f.write("<div class=\"text-data\">$%s FOR SIZE %s</div>" % (prices[i], sizes[i]))
f.write("</div>")
f.close()