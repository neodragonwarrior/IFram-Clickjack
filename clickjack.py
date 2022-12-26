import requests
import re
import webbrowser
import sys

from urllib.parse import urlparse

def check_iframe_allowed(url):
  # Add the 'http://' prefix to the URL if it is not present
  parsed_url = urlparse(url)
  if not parsed_url.scheme:
    url = 'http://' + url

  # Fetch the URL
  response = requests.get(url)
  headers = response.headers

   # Set the text color to blue
  blue_color_code = '\033[94m'
  reset_color_code = '\033[0m'

  # Print the headers in a neat tabular form
  print(blue_color_code + 'Response headers:' + reset_color_code)
  print('-' * 80)
  print('{:<40s} {:<40s}'.format('Header name', 'Header value'))
  print('-' * 80)
  for name, value in headers.items():
    print('{:<40s} {:<40s}'.format(name, value))
  print('-' * 80)
  
  # Check the X-Frame-Options header
  x_frame_options = headers.get('X-Frame-Options', '').lower()
  if x_frame_options in ('deny', 'sameorigin'):
    return False
  
   # Check the frame-ancestors directive in the Content-Security-Policy header
  content_security_policy = headers.get('Content-Security-Policy', '').lower()
  if 'frame-ancestors none' in content_security_policy:
    print('The page cannot be displayed in a frame, regardless of the site attempting to do so.')
    return False
  elif 'frame-ancestors self' in content_security_policy:
    print('The page can only be displayed in a frame on the same origin as the page itself.')
    return False
  elif 'frame-ancestors' in content_security_policy:
    print('The page can only be displayed in a frame on the specified origins.')
    return False
  
  # If no restrictions were found, the URL is allowed to be loaded in an iframe
  # Create an HTML string with the URL in an iframe tag
  f = open('clickjacktest.html','w')
  message = """<html>
  <body>
  <h1>Clickjack Test Page</h1>
  <iframe src="{testurl}" width="800" height="500"></iframe>
  <!--Clickjack Test Page @github.com/neodragonwarrior -->
  </body>
  </html>
  """.format(testurl=url)
  f.write(message)
  f.close()
  webbrowser.open_new_tab('clickjacktest.html')
  return True

# Prompt the user for a URL
url = input('Enter a URL: ')

# Check if the URL is allowed to be loaded in an iframe
result = check_iframe_allowed(url)

# Set the text color to red if the URL is allowed to be loaded in an iframe, or to green if the URL is not allowed to be loaded in an iframe
red_color_code = '\033[91m'
green_color_code = '\033[92m'
reset_color_code = '\033[0m'

if result:
  print(red_color_code + 'VULNERABLE:The URL is allowed to be loaded in an iframe.Potential Clickjacking' + reset_color_code)
else:
  print(green_color_code + 'SAFE:The URL is not allowed to be loaded in an iframe.' + reset_color_code)
