import requests
from bs4 import BeautifulSoup



url = 'https://www.nobroker.in/prophub/new-builder-projects/new-builder-projects-in-bangalore/'

res = requests.get(url=url)
html_content = res.content
soup = BeautifulSoup(html_content,'html.parser')
# print(soup.title.text)
property_details  = {"project_name":[], "price":[],"bhk":[]}
for inner_ul in soup.find_all('ul'):
    for inner_li in inner_ul:

        for innner_most_li in inner_li:
            if 'Project_Name' in innner_most_li:
                property_details['project_name'].append(innner_most_li.strip().split(':')[1])

            if 'Price' in innner_most_li:
                property_details['price'].append(innner_most_li.strip().split(':')[1])
            if 'BHK' in innner_most_li:
                property_details['bhk'].append(innner_most_li.strip().split(':')[1])


print(type(property_details))

for key, value in property_details.items():

    print(f'{key} : {value}','\n')