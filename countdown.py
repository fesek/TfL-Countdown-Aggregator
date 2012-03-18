#! /usr/bin/env python

import cgi
import httplib
from xml.dom.minidom import parse, parseString

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def parseEntry(entry):
  info = entry.getElementsByTagName("td")
  if len(info) != 3:
    return ()
  route = getText(info[0].childNodes).strip()
  dest = getText(info[1].childNodes).strip()
  eta = getText(info[2].childNodes).strip()
  return (route, dest, eta)

def processData(data):
  entries_out = []

  content = data.getElementsByTagName("tbody")
  if len(content) == 0:
    return entries_out
  entries = content[0].getElementsByTagName("tr")
  for entry in entries:
    entry_out = parseEntry(entry)
    entries_out.append(entry_out)

  return entries_out


site = "m.countdown.tfl.gov.uk"
page = "/arrivals"

stops = [ ("58872", "Trafalgar Square (S) "),
          ("48595", "Piccadilly Circus (D)"),
        ]




print 'Content-type: text/html\n\n'

print '<html><head>'
print '<title>My Page</title>'
print '</head><body>'

print '<b>Departures</b>'
print '<br/><br/>'

print '<table>'
for stop in stops:

  print '<tr><td colspan = "3">'
  print '<b>' + stop[1] + '</b>'
  print '(#' + stop [0] + ')'
  print '</td></tr>'

  if (1):
    conn = httplib.HTTPConnection(site)
    conn.request("GET", page+"/"+stop[0])
    rl = conn.getresponse()
    if rl.status != 200:
      print rl.status, rl.reason
      continue

    datal = rl.read()
    dom = parseString(datal)
  else:
    dom = parse("./data")

  entries = processData(dom)

  print len(entries)

  if len(entries):
    for entry in entries:
      print '<tr>'
      if len(entry) == 0:
  	print '<td colspan = "3"> Invalid entry </td>'
      print '<td>' + entry[0] + '</td>'
      print '<td>' + entry[1] + '</td>'
      print '<td>' + entry[2] + '</td>'
      print '</tr>'
  else:
    print '<tr><td>No data found</td></tr>'

  print '<tr></tr>'


print '</body></html>'
