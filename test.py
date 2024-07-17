import requests
import urllib3
urllib3.disable_warnings()

endpoint = 'https://billing.smartshell.gg/api/graphql'
query = '''mutation login {
  login(input:{
    login:"Вставить тел администратора"
    password:"Его пароль"
    company_id:айди шела
    
  })
  {
    access_token
    token_type
    refresh_token
      __typename
    expires_in
  }
}'''
request = requests.post(endpoint, json={'query': query}, verify=False)
print(request.text)

#копируем токен из консоли в main.py

