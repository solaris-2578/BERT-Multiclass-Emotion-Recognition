

import pandas as pd
#from tkmacosx import Button

from bs4 import BeautifulSoup
from urllib.request import urlopen
from tkinter import *
import os
import re

####################

NYPOST_URL='https://nypost.com'

NEWS_TYPE = [
    "all",
    "general",
    "sports",
    "metro",
    "entertainment",
    "business",
    "opinion",
    "fashion",
    "shopping",
    "living",
    "real-estate",
    "tech",
    "media"
]


def get_NYPost_headlines(news_type = "all"):
    """
    :param news_type: New Type, must be one item in NEWS_TYPE
    :return: A list of string contains all headlines
    """
    if type(news_type) != str:
        raise TypeError("news_type must be a string, while {} found.".format(type(news_type)))

    if news_type not in NEWS_TYPE:
        raise ValueError("Unknown news type {}".format(news_type))

    ihtml = urlopen(NYPOST_URL)
    isoup = BeautifulSoup(ihtml, "html.parser")

    headlines = []
    target_news_type = []

    if news_type != "all":
        target_news_type.append(news_type)
    else:
        target_news_type.extend(NEWS_TYPE[1:])

    [headlines.extend(get_NYPost_special_news(isoup, t)) for t in target_news_type]

    return headlines

def clean_headline(headline):
    return re.sub("\t|\r|\n", "", headline)

def get_NYPost_general_news(isoup):
    a = isoup.find("div", {"id": "news-top-stories"})
    a1 = a.find("div", {"class": "featured-stories"})
    a2 = a1.findAll("article")
    news = []
    for i in a2:
        # print(i.find("h3").text)
        news.append(clean_headline(i.find("h3").text))

    a3 = a.find("div", {"class": "home-page-section-stories-wrapper"})
    a4 = a3.findAll("article")
    for i in a4:
        news.append(clean_headline(i.find("h3").text))

    return news


def get_NYPost_special_news(isoup, type):

    if type == "general":
        return get_NYPost_general_news(isoup)

    news = []
    b = isoup.find("div", {"id": "{}-top-stories".format(type)})
    b1 = b.findAll("article")
    for i in b1:
        news.append(clean_headline(i.find("h3").text))
    return news

#######################


click=0

root=Tk()

#root.attributes("-fullscreen", True) 
root.geometry("1750x1100")

root.title("Emotion Predictions")


bg_color='gray12'
root.configure(background=bg_color)


fg_color='white'

#root.wm_attributes("-transparentcolor", 'grey')



#C = Tkinter.Canvas(top, bg="cyan4", height=900, width=600)


labelfont0 = ('Helvetica', 19)

title = ('Helvetica', 45,'bold italic')
labelfont = ('times', 20, 'bold')
labelfont1 = ('times', 25, 'bold')





def onclick():
    labelfont1 = ('times', 25, 'bold')
    for i in range(200,1000,10):
        text=Label(root,text="                                                                                                                                                                                        ", bg=bg_color, fg='firebrick2')
        text.config(font=labelfont1)
        text.place(x=160,y=i)
        
    #pygame.init()
    #pygame.mixer.music.load('Ta_da.mp3')
    #pygame.mixer.music.play(0)
    #time.sleep(0.2)
    
   # type1_label=Label(text="                 ", bg=bg_color) 
   # type1_label.config(font=labelfont)
   # type1_label.place(x=950,y=250)
  
    t1=topic.get()
    t1=t1.lower()
    if t1=='technology':
        t1='tech'
    a=get_NYPost_headlines(t1)
    x=160
    y=350
    
    if t1=='all':
        y=200
        labelfont1 = ('times', 12, 'bold')
        for i in a:
    
            p_label=Label(root,text=i, bg=bg_color, fg='firebrick2')
            p_label.config(font=labelfont1)  
            p_label.place(x=x,y=y)
            y=y+17
    
    else:
        labelfont1 = ('times', 25, 'bold')
        for i in a:
            
            #emo=bert.predict_emotion(i)
            t_label=Label(text="                                                                                               ", bg=bg_color) 
            t_label.config(font=labelfont1)
            t_label.place(x=x,y=y)
            p_label=Label(root,text=i, bg=bg_color, fg='firebrick2')
            p_label.config(font=labelfont1)  
            p_label.place(x=x,y=y)
            y=y+40
        
    #os.execl(sys.executable, sys.executable, *sys.argv)



title_label=Label(root,text="NYPost Headlines Sentiment Analysis", font=title, bg=bg_color,fg='SpringGreen4')
title_label.place(x=440,y=10)  






stats_button=Button(root,text="Emotion Calculator", height=3,width=20, command=onclick)
stats_button.place(x=900,y=120)


topic=StringVar(root)
drop=OptionMenu(root,topic,"All","General", "Sports", "Metro", "Entertainment",
    "Business",
    "Opinion",
    "Fashion",
    "Shopping",
    "Living",
    "Real-Estate",
    "Technology",
    "Media" )
drop.place(x=750,y=135)
    

root.mainloop()


###


