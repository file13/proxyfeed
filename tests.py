#!/usr/bin/env python3

#######################################################################
# This program source is a part of a literate program and was produced
# by nuweb. Please see the accompanying literate program pdf for the
# full documentation.
#
# author: Michael J. Rossi
# contact: file13@hushmail.me
# literate pdf file: proxyfeed.pdf
#######################################################################

#######################################################################
# Copyright (c) 2015, Michael J. Rossi
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#######################################################################


import unittest
from xml.etree.ElementTree import parse
from proxyfeed import *

class ProxyFeedTest(unittest.TestCase):
    
    def test_extract_proxy_data(self):
        with open('testfeed.xml', 'rt') as f:
            doc = parse(f)
            spec = 'http://www.proxyrss.com/specification.html'
            results = extract_proxy_data(doc, spec)
            self.assertEqual(results[0]['ip'], '183.223.173.237')
            self.assertEqual(results[0]['port'], '8123')
            self.assertEqual(results[0]['country'], 'China')
            self.assertEqual(results[0]['timestamp'], '03/6 20:23:47')

            self.assertEqual(results[1]['ip'], '183.221.208.44')
            self.assertEqual(results[1]['port'], '8123')
            self.assertEqual(results[1]['country'], 'CN')
            self.assertEqual(results[1]['timestamp'], '03/6 20:21:37')

            self.assertEqual(results[2]['ip'], '183.221.160.12')
            self.assertEqual(results[2]['port'], '8123')
            self.assertEqual(results[2]['country'], 'Unknown')
            self.assertEqual(results[2]['timestamp'], 'Unknown')
    
    def test_get_proxy_feed(self):
        feed = 'http://www.proxz.com/proxylists.xml'
        results = get_proxy_feed(feed)
        self.assertTrue(results[0]['ip'])
        self.assertTrue(results[0]['port'])
        self.assertTrue(results[0]['country'])
        self.assertTrue(results[0]['timestamp'])
        self.assertTrue(results[0]['country'])
    
    def test_filter_by_country(self):
        with open('testfeed.xml', 'rt') as f:
            doc = parse(f)
            spec = 'http://www.proxyrss.com/specification.html'
            results = extract_proxy_data(doc, spec)
            results = filter_by_country(results, 'CN', 'China')
            self.assertEqual(len(results), 2)
            results = extract_proxy_data(doc, spec)
            results = filter_by_country(results, 'US', 'United States')
            self.assertEqual(len(results), 2)
    
    def test_get_whois_description(self):
        results = get_whois_description('104.41.162.113')
        self.assertEqual(results, 'Microsoft Corporation')
    
    def test_lookup_whois(self):
        results = [{'ip':'104.41.162.113', 'port':'80'}]
        proxies = lookup_whois(results)
        self.assertEqual(results[0]['whois'], 'Microsoft Corporation')
    
    def test_is_ip_in_dict(self):
        with open('testfeed.xml', 'rt') as f:
            doc = parse(f)
            spec = 'http://www.proxyrss.com/specification.html'
            results = extract_proxy_data(doc, spec)
            self.assertTrue(is_ip_in_dict('183.221.160.12', results))
    
    def test_remove_duplicates(self):
        with open('testfeed.xml', 'rt') as f:
            doc = parse(f)
            spec = 'http://www.proxyrss.com/specification.html'
            results = extract_proxy_data(doc, spec)
            self.assertEqual(len(results), 6)
            results = remove_duplicates(results)
            self.assertEqual(len(results), 5)
    
    def test_convert_time(self):
        self.assertTrue(convert_time("1439993032"), "08-19-2015 at 14:03:00 UTC")
        self.assertTrue(convert_time("08/19 13:54:28"), "08-19-2015 at 13:54:28 UTC")
        format = "%m-%d-%Y at %H:%M:00 UTC"
        now = datetime.datetime.now()
        self.assertTrue(convert_time("Unknown"),
                        "Unknown time, listing found at " + now.strftime(format))
     
    def test_print_results(self):
        with open('testfeed.xml', 'rt') as f:
            doc = parse(f)
            spec = 'http://www.proxyrss.com/specification.html'
            results = extract_proxy_data(doc, spec)
            print_results(results)
            print_results(results, human_readable=False)
            print_results(results, print_country=False, human_readable=False)
    
        
if __name__ == '__main__':
    unittest.main(warnings='ignore',failfast=True)
