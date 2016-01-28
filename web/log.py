#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys    
import sqlite3 as sqlite  

con = sqlite.connect('/mnt/sd/arduino/db/reef.db')
cur = con.cursor()
cur.execute("SELECT cas, strftime('%d.%m.%Y %H:%M',cas) , teplota FROM teplota_log ORDER BY cas DESC LIMIT 216") 

cur2 = con.cursor()                                      
cur2.execute("select strftime('%H', cas) from teplota_log " +
  					 "where " +
	   				 "  strftime('%M', cas) = '00'  and " +
	           "  cas between  datetime((select max(cas)  from teplota_log "+
  					 "                         where " +
	   				 "                           strftime('%M', cas) = '00' ), '-72 hours') and " +
						 "                        (select max(cas) from teplota_log " +
  					 "                         where " +
	   				 "                           strftime('%M', cas) = '00' ) " + 																					 
             "order by cas")                                                                                                     

cur3 = con.cursor()                                      
cur3.execute("select teplota from teplota_log " +
  					 "where " +
	   				 "  strftime('%M', cas) = '00'  and " +
	           "  cas between  datetime((select max(cas)  from teplota_log "+
  					 "                         where " +
	   				 "                           strftime('%M', cas) = '00' ), '-72 hours') and " +
						 "                        (select max(cas) from teplota_log " +
  					 "                         where " +
	   				 "                           strftime('%M', cas) = '00' ) " + 																					 
             "order by cas")                                                                                                     

cur4 = con.cursor()                                      
cur4.execute("select min(teplota), max(teplota) from teplota_log " +
  					 "where " +
	   				 "  strftime('%M', cas) = '00'  and " +
	           "  cas between  datetime((select max(cas)  from teplota_log "+
  					 "                         where " +
	   				 "                           strftime('%M', cas) = '00' ), '-72 hours') and " +
						 "                        (select max(cas) from teplota_log " +
  					 "                         where " +
	   				 "                           strftime('%M', cas) = '00' ) " + 																					 
             "order by cas")  

for row in cur4:
  minTeplota = row[0]
  maxTeplota = row[1]

minTeplota = minTeplota - 0.2
maxTeplota = maxTeplota + 0.2
pocetKroku = (maxTeplota - minTeplota)/0.1

print 'Content-type:text/html\r\n\r\n'
print '<!doctype html>'
print '<html>'
print '  <head>'
print '    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
print '    <title>Fousáčův Arduino server</title>'
print '    <link rel="stylesheet" href="styles.css" type="text/css" />'
print '    <script src="Chart.min.js"></script>'
print '  </head>'
print '  <body>'
print '    <div id="container">'
print '      <header>'
print '    	  <div class="width">'
print '          <h1><a href="/">Fousáčův<span> arduino server</span></a></h1>'
print '    	  </div>'
print '      </header>'
print '      <nav>'
print '       	<div class="width">'
print '       		<ul>'
print '         		<li class=""><a href="index.py">Home</a></li>'
print '         	  <li class="start selected"><a href="log.py">Log</a></li>'
print '         	</ul>'
print '       	</div>'
print '      </nav>'
print '      <div id="body" class="width">'
print '    		<section id="content">'
print '    	    <article>'
print '           <canvas id="teplotaChart" width="1024" height="200"></canvas>  '	
print '           <table>'
print '             <tr>'
print '               <th>Čas</th>'
print '               <th>Teplota</th>'
print '             </tr>'

for row in cur:
  print '           <tr><td>' + row[1] + '</td>' + '<td>' + str(row[2]) + ' &deg;C</td></tr>'

print '           </table>'		            
print '    		  </article>'
print '        </section>'     
print '      </div>'
print '    </div>'

print '    <script>'
print '      var teplotaData = {'
print '        labels : ['

labels = ''       
for row in cur2:
  labels = labels + '"' + str(row[0]) + '", '       

print labels       
print '                 ],'
print '        datasets : ['
print '           {'
print '               fillColor : "rgba(172,194,132,0.4)",'
print '               strokeColor : "#ACC26D",'
print '               pointColor : "#fff",'          
print '               pointStrokeColor : "#9DB86D",'
print '               data : ['

data = ''
for row in cur3:
  data = data + str(row[0]) + ', '

print data  
print '                      ]'
print '           }'
print '        ]'
print '      }' 

print '      var teplotaOptions = {' 
print '        scaleOverride: true,'
print '        scaleBeginAtZero: false,'
print '        scaleSteps: ' + str(pocetKroku) + ','
print '        scaleStepWidth: 0.1,'
print '        scaleStartValue: ' + str(minTeplota) + ','
print '      }'            
print '      var teplota = document.getElementById("teplotaChart").getContext("2d");'          
print '      new Chart(teplota).Line(teplotaData, teplotaOptions);'
print '    </script>'

print '  </body>'
print '</html>'

con.close()
