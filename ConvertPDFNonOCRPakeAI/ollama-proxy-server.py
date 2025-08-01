#!/usr/bin/env python3
"""
Simple CORS proxy server for Ollama API
This allows the local converter to access Ollama without CORS issues.

Usage:
    python ollama-proxy-server.py

Then open: http://localhost:8080/local-converter-oneliner.html
"""

import http.server
import socketserver
import urllib.request
import urllib.parse
import json
import os
from urllib.error import HTTPError, URLError

class OllamaProxyHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path.startswith('/api/'):
            self.proxy_to_ollama()
        else:
            # Serve static files from dist-local directory
            if self.path == '/' or self.path == '':
                file_path = 'local-converter-oneliner.html'
            else:
                file_path = self.path.lstrip('/')
            
            dist_local_path = os.path.join('dist-local', file_path)
            
            if os.path.exists(dist_local_path):
                # Serve the file directly
                try:
                    with open(dist_local_path, 'rb') as f:
                        content = f.read()
                    
                    # Determine content type
                    if file_path.endswith('.html'):
                        content_type = 'text/html'
                    elif file_path.endswith('.css'):
                        content_type = 'text/css'
                    elif file_path.endswith('.js'):
                        content_type = 'application/javascript'
                    else:
                        content_type = 'application/octet-stream'
                    
                    self.send_response(200)
                    self.send_header('Content-Type', content_type)
                    self.send_header('Content-Length', str(len(content)))
                    self.end_headers()
                    self.wfile.write(content)
                    return
                except Exception as e:
                    self.send_error(404, f"Error reading file: {e}")
                    return
            
            # File not found
            self.send_error(404, f"File not found: {file_path}")

    def do_POST(self):
        if self.path.startswith('/api/'):
            self.proxy_to_ollama()
        else:
            super().do_POST()

    def proxy_to_ollama(self):
        try:
            # Get the request body for POST requests
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else None
            
            # Construct Ollama URL
            ollama_url = f'http://localhost:11434{self.path}'
            
            # Create request
            req = urllib.request.Request(ollama_url, data=post_data)
            
            # Copy headers (except host)
            for header, value in self.headers.items():
                if header.lower() not in ['host', 'content-length']:
                    req.add_header(header, value)
            
            # Make request to Ollama
            with urllib.request.urlopen(req, timeout=30) as response:
                # Send response status
                self.send_response(response.getcode())
                
                # Copy response headers
                for header, value in response.headers.items():
                    if header.lower() not in ['server', 'date']:
                        self.send_header(header, value)
                
                self.end_headers()
                
                # Copy response body
                self.wfile.write(response.read())
                
        except HTTPError as e:
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = {
                'error': f'Ollama API Error: {e.code} {e.reason}',
                'details': 'Make sure Ollama is running on localhost:11434'
            }
            self.wfile.write(json.dumps(error_response).encode())
            
        except URLError as e:
            self.send_response(503)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = {
                'error': 'Cannot connect to Ollama',
                'details': 'Make sure Ollama is running on localhost:11434',
                'reason': str(e.reason)
            }
            self.wfile.write(json.dumps(error_response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = {
                'error': 'Proxy server error',
                'details': str(e)
            }
            self.wfile.write(json.dumps(error_response).encode())

def main():
    PORT = 8080
    
    print("🚀 Starting Ollama Proxy Server...")
    print(f"📡 Server running at: http://localhost:{PORT}")
    print(f"🔗 Open: http://localhost:{PORT}/local-converter-oneliner.html")
    print("📁 Serving files from dist-local/ directory")
    print("🔄 Proxying /api/* requests to Ollama at localhost:11434")
    print("\n💡 This server enables CORS for Ollama API access")
    print("⚠️  Make sure Ollama is running on localhost:11434")
    print("\n🛑 Press Ctrl+C to stop the server")
    
    try:
        with socketserver.TCPServer(("", PORT), OllamaProxyHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped gracefully")
    except OSError as e:
        if e.errno == 10048:  # Address already in use
            print(f"\n❌ Error: Port {PORT} is already in use")
            print(f"💡 Try using a different port or stop the process using port {PORT}")
        else:
            print(f"\n❌ Error starting server: {e}")

if __name__ == "__main__":
    main()