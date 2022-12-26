import requests
import re

def check_iframe_allowed(url):
  # Fetch the URL
  response = requests.get(url)
  html = response.text

  # Check the X-Frame-Options header
  x_frame_options_regex = r'<meta[^>]+http-equiv="X-Frame-Options"[^>]+content="(.+?)"'
  x_frame_options_match = re.search(x_frame_options_regex, html, re.IGNORECASE)
  if x_frame_options_match:
    # If the X-Frame-Options header is set to 'DENY' or 'SAMEORIGIN',
    # the URL is not allowed to be loaded in an iframe
    x_frame_options = x_frame_options_match.group(1).lower()
    if x_frame_options in ('deny', 'sameorigin'):
      return False
  
  # Check the frame-ancestors directive in the Content-Security-Policy header
  content_security_policy_regex = r'<meta[^>]+http-equiv="Content-Security-Policy"[^>]+content="[^;]*frame-ancestors[^;]*none"'
  content_security_policy_match = re.search(content_security_policy_regex, html, re.IGNORECASE)
  if content_security_policy_match:
    # If the frame-ancestors directive is set to 'none', the URL is not allowed to be loaded in an iframe
    return False
  
  # If no restrictions were found, the URL is allowed to be loaded in an iframe
  return True

# Prompt the user for a URL
url = input('Enter a URL: ')

# Check if the URL is allowed to be loaded in an iframe
result = check_iframe_allowed(url)

if result:
  print('The URL is allowed to be loaded in an iframe.')
else:
  print('The URL is not allowed to be loaded in an iframe.')
