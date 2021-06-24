#!/usr/bin/env python
# coding: utf-8

# In[130]:


import smtplib
from email.message import EmailMessage
from pygooglenews import GoogleNews
import pandas as pd
from bs4 import BeautifulSoup


EMAIL_ADDRESS = '@gmail.com'
EMAIL_PASSWORD = ''


# In[131]:


gn = GoogleNews(lang = 'en')


# In[132]:


def get_titles(search):
    stories = []
    search = gn.search(search, when = '7d')
    newsitem = search['entries']
    for item in newsitem:
        story = {
            'title': item.title,
            'published': item.published,
            'link': item.link,
            'source': item.source,
        
        }
        stories.append(story)
    return(stories)


# In[133]:


ds_list = get_titles('Data Science')
ds_news = pd.DataFrame(ds_list)
ds_news['date'] = pd.to_datetime(ds_news['published']).dt.date
ds_news.sort_values(by=['date'], ascending=False, inplace = True)
ds_news.to_csv('news.csv')


# In[134]:


template = open('email.html')
soup = BeautifulSoup(template.read(), "html.parser")

article_template = soup.find('div', attrs={'class':'columns'})
html_start = str(soup)[:str(soup).find(str(article_template))]
html_end = str(soup)[str(soup).find(str(article_template))+len(str(article_template)):]
html_start = html_start.replace('\n','')
html_end = html_end.replace('\n','')


# In[135]:


urls = ds_news["link"]
urls


# In[136]:


newsletter_content = ""
for i,article in enumerate(ds_list):
    
    try:
        img = article_template.img
        img['src'] = article['image']
        article_template.img.replace_with(img)
    except:
        pass
    
    title = article_template.h1
    title.string = article['title'][:100]
    
    link = article_template.a
    link['href'] = urls[i]
    link.string = urls[i]
    article_template.a.replace_with(link)
    
    
    newsletter_content += str(article_template).replace('\n','')

email_content = html_start + newsletter_content + html_end


# In[137]:


newsletter_html = BeautifulSoup(email_content).prettify()


# In[138]:


msg = EmailMessage()
msg['Subject'] = 'Here is my newsletter'
msg['From'] = EMAIL_ADDRESS 
msg['To'] = EMAIL_ADDRESS
msg.set_content(newsletter_html, subtype='html')


# In[139]:


with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD) 
    smtp.send_message(msg)


# In[ ]:




