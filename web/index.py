#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys    
sys.path.insert(0, '/usr/lib/python2.7/bridge/') 
from bridgeclient import BridgeClient as bridgeclient
                                                    
value = bridgeclient()                                                                                                          

print "Content-type:text/html\r\n\r\n"
print '<!doctype html>'
print '<html>'
print '  <head>'
print '    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
print '    <title>Fousáčův Arduino server</title>'
print '    <link rel="stylesheet" href="styles.css" type="text/css" />'
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
print '         		<li class="start selected"><a href="index.py">Home</a></li>'
print '         	  <li class=""><a href="log.py">Log</a></li>'
print '         	</ul>'
print '       	</div>'
print '      </nav>'
print '      <div id="body" class="width">'
print '    		<section id="content">'
print '    	    <article>'	
print '            <h3>' + value.get('datum') + '&nbsp; - &nbsp;' +value.get('cas') + '</h3><br/>'
print '            <b>Teplota: </b>' +value.get('teplota') + ' C<br/>'			            
print '    		  </article>'
print '        </section>'     
print '      </div>'
print '    </div>'
print '  </body>'
print '</html>'