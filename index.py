import BaseHTTPServer
import urlparse
import sys
import subprocess
import time
import os
import xml.etree.ElementTree as etree
import json

HOST = '127.0.0.1'
PORT = 8080
NIKTO_PATH = './nikto-master/program/'

class Utility(object):

	@classmethod
	def get_queries(cls, path):
		if path[1] == '?':
			pairs = urlparse.parse_qs(path[2:])
			if pairs and 'host' in pairs and 'cgidirs' in pairs:
				return [pairs['host'][0],pairs['cgidirs'][0]]

	@classmethod
	def run_nikto(cls, args):
		cwd = os.getcwd()
		file_path = '{0}/{1}.xml'.format(cwd, hex(int(time.time())))
		cmd = "cd {0} && perl nikto.pl -h {1} -C {2} -o {3} -config {4}/nikto.conf"
		format_cmd = cmd.format(NIKTO_PATH, args[0], args[1], file_path, cwd)
		subprocess.call(format_cmd, shell=True)
		response_xml = open(file_path).read()
		response_json = cls._parse_nikto(response_xml)
		os.remove(file_path)
		return response_json

	@classmethod
	def _parse_nikto(cls, xml):
		root = etree.fromstring(xml)
		parsed = { 'results': [] }
		for item in root.findall('./niktoscan/scandetails/item'):
			parsed_item = { "id": item.attrib['id'] }
			for child in item:
				parsed_item[child.tag] = child.text
			parsed['results'].append(parsed_item)
		return json.dumps(parsed)


class Handler(BaseHTTPServer.BaseHTTPRequestHandler):

	def do_GET(self):
		args = Utility.get_queries(self.path)
		if args:
			response_json = Utility.run_nikto(args)
			self.send_response(200)
			self.send_header('Content-type', 'text/json')
			self.end_headers()
			self.wfile.write(response_json)
		else:
			self.send_response(400)
			self.send_header('Content-type', 'text/plain')
			self.end_headers()
			self.wfile.write('Error 400: Bad Request')


def main():
	RequestHandlerClass = Handler
	server = BaseHTTPServer.HTTPServer((HOST, PORT), Handler)
	try:
		server.serve_forever()
	except KeyboardInterrupt:
	    pass
	server.server_close()

if __name__ == '__main__':
    main()
