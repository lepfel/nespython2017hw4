
# coding: utf-8

# ## Задача 1

# In[6]:

import requests
import zipfile
import os

import numpy as np
import pandas as pd

pd.set_option('float_format', '{:6.2f}'.format)


# In[7]:

get_ipython().system(u'pwd')


# In[8]:

url = 'https://drive.google.com/uc?export= download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM'
dirname = '/Users/mihail/Desktop/HW4/'
path = dirname + 'stack_overflow.zip'


response = requests.get(url)
with open(path, "wb") as file:
    file.write(response.content)


# In[9]:

path


# In[10]:

zf = zipfile.ZipFile(path)
files = zf.namelist()

print(files)


# In[11]:

files[6]


# In[12]:

survey = pd.read_csv(zf.open(files[5]), header=0)


# In[13]:

survey.head()


# In[14]:

results = pd.read_csv(zf.open(files[6]))


# In[15]:

results.head()


# In[16]:

results.shape


# 154 вопроса было в опросе

# In[17]:

survey.shape


# 51392 разработчиков приняло участие

# ## Задача 2

# In[18]:

survey.Country.value_counts()[0:10]


# In[19]:

survey.Country.value_counts()[0:10]/len(survey)


# ## Задача 3

# In[20]:

import re
import urllib
from bs4 import BeautifulSoup


# In[21]:

url = 'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population'
html = urllib.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')
print( soup)


# In[23]:

tables = soup.find("table", { "class" : "wikitable sortable" })
table = []
line = []
for row in tables.findAll("tr"):
    cells = row.findAll("td")
    line = []
    for i in range(len(cells)):
        line.append(cells[i].text)
    table.append(line)
    
table = pd.DataFrame(table)
table.head()


# In[24]:

table = table.loc[1:]


# In[25]:

table = table[ [1,2] ]


# In[26]:

table.columns = ['Country', 'People']


# In[27]:

table.head()


# In[28]:

s = 'China[Note 2]'


# In[29]:

k = s.find('[')


# In[30]:

s[0:k]


# In[31]:

for s in table.index:
    k = table.loc[s]['Country'].find('[')
    if k >0:
        table.loc[s]['Country'] = table.loc[s]['Country'] [0:k]


# In[32]:

for s in table.index:
    k = table.loc[s]['Country']
    if k[0] == ' ':
        table.loc[s]['Country'] = table.loc[s]['Country'] [1:]


# In[33]:

for s in table.index:
    k = table.loc[s]['People']
    k_new = re.sub( ',', '', k )
    table.loc[s]['People'] = k_new


# In[34]:

table.People = table.People.astype(float)


# In[35]:

survey_country_count = survey.groupby('Country').count()


# In[36]:

survey_country_count = survey_country_count.reset_index()


# In[37]:

a = pd.merge( left = table, right =  survey_country_count, on = 'Country') [['Country','People','Respondent']]


# In[38]:

a[a.Country =='Slovenia']


# In[39]:

a['ratio'] = a.Respondent/ a.People


# In[40]:

a[a.Respondent>100].sort_values( by = 'ratio', ascending = False)[0:10]


# ## Задача 4

# In[41]:

survey.VersionControl.value_counts()


# ## Задача 5

# In[42]:

Language = set()


# In[43]:

for i in survey.HaveWorkedLanguage:
    if pd.isnull(i) == False:
        Language = Language.union(set(re.split(';',   i.replace('; ', ';')) ))


# In[44]:

print(list(Language))


# ## Задача 6

# In[45]:

counts = []

for i in list(Language):
    summa = 0
    for j in survey.HaveWorkedLanguage: 
        if pd.isnull(j) == False:
            if (i) in (set(re.split(';',   j.replace('; ', ';')) )):
                summa +=1
    counts.append(summa) 


# In[46]:

answer6 = pd.DataFrame( data = [Language , counts]).T


# In[47]:

answer6.columns = ['Language' , 'counts']


# In[48]:

answer6.sort_values(by = 'counts' , ascending= False).iloc[0:10]


# ## Задача 7

# In[49]:

data = survey.copy()


# In[50]:

for i in Language:
    data[i] = 0


# In[51]:

data.head()


# In[53]:

for i in list(Language):
    print(i)
    summa = []
    for j in data.HaveWorkedLanguage: 
        if ((pd.isnull(j) == False) and ((i) in (set(re.split(';',   j.replace('; ', ';')) )))):
            summa.append(1)
        else:
            summa.append(0)
    data[i] = summa


# In[54]:

data[ list(Language) ].head()


# In[55]:

top10 = data.groupby( 'Country' ).sum()[ ['Respondent']+ list(Language) ].sort_values(by = 'Respondent', ascending =False).iloc[0:10]


# In[56]:

top10[list(Language)].idxmax(axis=1)  #самый популярный язык в топ 10 стран


# In[57]:

top = data.groupby( 'Country' ).sum()[ ['Respondent']+ list(Language) ].sort_values(by = 'Respondent', ascending =False)


# In[58]:

top_l = top[list(Language)].idxmax(axis=1)


# In[59]:

top_l [top_l !='JavaScript' ] [0:5]


# In[60]:

#ответ South Korea     Java


# ## Задача 8

# In[61]:

#Как образование влияет на среднюю зарплату


# In[62]:

survey.groupby ('FormalEducation').mean( ).Salary


# Наибольшую зарплату получают программисты с Doctoral degree 
# наименьшую с Professional degree  ( среди тех кто ответил)
# 
# Master's degree   получают чуть больше Bachelor's degree 
# Primary/elementary school  получают больше  Master's degree  и Bachelor's degree , как бы это не было странным
# возможно это связано с малым объемом выборки

# In[63]:

survey.groupby ('FormalEducation').count( ).Salary

