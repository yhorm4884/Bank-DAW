import requests

url = 'https://raw.githubusercontent.com/sdelquin/dsw/main/ut3/te1/files/banks.json'
response = requests.get(url)
banks = response.json()
print(banks)