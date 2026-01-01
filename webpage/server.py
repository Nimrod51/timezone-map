#!/usr/bin/env python3
"""
Simple HTTP server with Range request support for PMTiles.
"""
import http.server
import socketserver
from functools import partial
import os

class RangeHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler with Range request support."""
    
    def send_head(self):
        """Common code for GET and HEAD commands with Range support."""
        path = self.translate_path(self.path)
        
        if os.path.isdir(path):
            return super().send_head()
        
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(404, "File not found")
            return None
        
        try:
            fs = os.fstat(f.fileno())
            file_len = fs[6]
            
            # Check for Range header
            if "Range" in self.headers:
                self.send_response(206)
                
                # Parse range header
                ranges = self.headers["Range"]
                ranges = ranges.strip()
                ranges = ranges[6:]  # Remove 'bytes='
                
                # Handle simple byte range (e.g., "0-1023" or "0-")
                if '-' in ranges:
                    start, end = ranges.split('-', 1)
                    start = int(start) if start else 0
                    end = int(end) if end else file_len - 1
                    
                    if start >= file_len:
                        self.send_error(416, "Requested Range Not Satisfiable")
                        return None
                    
                    if end >= file_len:
                        end = file_len - 1
                    
                    self.send_header("Content-type", self.guess_type(path))
                    self.send_header("Content-Range", f"bytes {start}-{end}/{file_len}")
                    self.send_header("Content-Length", str(end - start + 1))
                    self.send_header("Accept-Ranges", "bytes")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    
                    f.seek(start)
                    return f
            else:
                # No range, send full file
                self.send_response(200)
                self.send_header("Content-type", self.guess_type(path))
                self.send_header("Content-Length", str(file_len))
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                return f
                
        except Exception as e:
            f.close()
            self.send_error(500, f"Internal error: {e}")
            return None
    
    def copyfile(self, source, outputfile):
        """Copy data with potential range limits."""
        # Check if we're doing a range request
        if "Range" in self.headers and hasattr(source, 'tell'):
            ranges = self.headers["Range"]
            ranges = ranges.strip()[6:]  # Remove 'bytes='
            
            if '-' in ranges:
                start, end = ranges.split('-', 1)
                start = int(start) if start else 0
                end = int(end) if end else None
                
                if end is not None:
                    # Read only the requested range
                    length = end - start + 1
                    while length > 0:
                        chunk_size = min(8192, length)
                        chunk = source.read(chunk_size)
                        if not chunk:
                            break
                        outputfile.write(chunk)
                        length -= len(chunk)
                    return
        
        # Default: copy entire file
        super().copyfile(source, outputfile)

    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Range')
        super().end_headers()

if __name__ == '__main__':
    PORT = 8000
    
    with socketserver.TCPServer(("", PORT), RangeHTTPRequestHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}/")
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
