#!/usr/bin/env python
# encoding: utf-8
# __author__ = 'Demon'

from seedsim.layers import Base, Routing, Ebgp, Dnssec
from seedsim.services import DomainNameService, DomainNameCachingService, WebService
from seedsim.core import Simulator, Binding, Filter
from seedsim.compiler import Docker


sim = Simulator()

dns = DomainNameService()
ldns = DomainNameCachingService()


#Install root server
a_root_server = dns.install('a-root-server')
a_root_server.addZone('.')
#Set a-root-server to be primary(master) server
a_root_server.setMaster()

dns.install('b-root-server').addZone('.') # b-root-server will be slave.

#Install COM TLD server
dns.install('a-com-server').addZone('com.')
dns.install('b-com-server').addZone('com.')
dns.install('c-com-server').addZone('com.')

#Install NET TLD server
dns.install('a-net-server').addZone('net.')

#Install EDU TLD server
dns.install('a-edu-server').addZone('edu.')

#Install CN TLD server
dns.install('a-cn-server').addZone('cn.')

#Install GOV TLD server
dns.install('a-gov-server').addZone('gov.')

#Add some default record
twitter_com = dns.getZone('twitter.com.')
google_com = dns.getZone('google.com.')
facebook_com = dns.getZone('facebook.com.')
syr_edu = dns.getZone('syr.edu.')
weibo_cn = dns.getZone('weibo.cn.')
php_net = dns.getZone('php.net.')
us_gov = dns.getZone('us.gov.')

twitter_com.addRecord('@ A 1.1.1.1')
twitter_com.resolveToVnode("www", "www-twitter-com-web")
google_com.addRecord('@ A 2.2.2.2')
google_com.resolveToVnode('www','www-google-com-web')
facebook_com.addRecord('@ A 3.3.3.3')
facebook_com.resolveToVnode('www', 'www-facebook-com-web')
syr_edu.addRecord('@ A 128.230.18.63')
syr_edu.resolveToVnode('www', 'www-syr-edu-web')
weibo_cn.addRecord('@ A 4.4.4.4')
weibo_cn.addRecord('www A 4.4.4.4')
php_net.addRecord('@ A 5.5.5.5')
php_net.addRecord('www A 5.5.5.5')
us_gov.addRecord('@ A 6.6.6.6')
us_gov.addRecord('www A 6.6.6.6')


#Install DNSPOD servers
dns.install('ns1-dnspod.com').addZone('twitter.com.')
dns.install('ns1-dnspod.com').addZone('google.com.')
dns.install('ns1-dnspod.com').addZone('facebook.com.')

dns.install('ns2-dnspod.com').addZone('syr.edu.')
dns.install('ns2-dnspod.com').addZone('us.gov.')

dns.install('ns2-dnspod.com').addZone('weibo.cn.')
dns.install('ns3-dnspod.com').addZone('php.net.')

#Install local DNS
ldns.install('local-dns-1')

sim.addLayer(dns)
sim.addLayer(ldns)

sim.dump('dns-component.bin')