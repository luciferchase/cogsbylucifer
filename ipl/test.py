from bs4 import BeautifulSoup 
import requests

r = requests.get("https://www.google.co.in/search?q=ipl&tbm=isch&hl=en-GB&tbs=qdr:d%2Cisz:l&sa=X&ved=0CAEQpwVqFwoTCMiE6reBkvACFQAAAAAdAAAAABAE&biw=1301&bih=695")
soup = BeautifulSoup(r.text, "lxml")
link = soup.find('img', 'irc_mi')['src']
print(link)