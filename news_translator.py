from google_trans_new_main.google_trans_new import google_translator  
from tqdm import tqdm
import pandas as pd
import time

translator = google_translator(url_suffix="com")
news = pd.read_csv('./Sample_Datasets/XinMin.csv')
news_en = news.copy()

for index, row in tqdm(news.iterrows(), total=len(news)):
    '''
    We firstly put columns(except the content column) that containing short contenttogether and translate them at once.
    This is because we have to reduce the frequency of translation requests to accelerate the translation process.
    Please modify the code according to your own dataset.
    
    The logic is actually very simple. 
    However, due to some strange translation pricision error of the Google Translator package, we make the code look a little bit complicated :( 
    Please note that the translation may still not very accurate.
    Also, don't forget to connect to the VPN if you are in China. If you come across connection errors, just try again.
    '''
    ###### translate the short content ######
    special_title = row['special_title']
    if (type(special_title) != str):
        special_title = "Space"
    title = row['title']
    if (type(title) != str):
        title = "Space"
    subtitle = row['subtitle']
    if (type(subtitle) != str):
        subtitle = "Space"
    ban = row['ban']
    if (type(ban) != str):
        ban = "Space"
    slash_index = ban.find('/')
    if ban[slash_index+1].isdigit():
        ban = ban[:slash_index] + '和' + ban[slash_index+1:]
    short_content = special_title + " || " + title + " || " + subtitle + " || " + ban
    short_content = short_content.replace("新冠肺炎", " COVID-19 ")
    short_content = short_content.replace("新冠", " COVID-19 ")
    try:
        short_content_en = translator.translate(short_content,lang_src='zh', lang_tgt='en')
        # print(short_content)
        # print(short_content_en)
        short_elements = short_content_en.split("||")
        if len(short_elements) != 4:
            # print("Error: The number of elements in short_content_en is not 4. Try to translate them one by one.")
            special_title = special_title.replace("新冠肺炎", " COVID-19 ").replace("新冠", " COVID-19 ")
            title = title.replace("新冠肺炎", " COVID-19 ").replace("新冠", " COVID-19 ")
            subtitle = subtitle.replace("新冠肺炎", " COVID-19 ").replace("新冠", " COVID-19 ")
            news_en.at[index, 'special_title'] = translator.translate(special_title,lang_src='zh', lang_tgt='en')
            news_en.at[index, 'title'] = translator.translate(title,lang_src='zh', lang_tgt='en')
            news_en.at[index, 'subtitle'] = translator.translate(subtitle,lang_src='zh', lang_tgt='en')
            news_en.at[index, 'ban'] = translator.translate(ban,lang_src='zh', lang_tgt='en')
        else:     
            news_en.at[index, 'special_title'] = short_elements[0].strip()
            news_en.at[index, 'title'] = short_elements[1].strip()
            news_en.at[index, 'subtitle'] = short_elements[2].strip()
            news_en.at[index, 'ban'] = short_elements[3].strip()
    except:
        # print('There is an error. Try to translate them one by one.'')
        special_title = special_title.replace("新冠肺炎", " COVID-19 ").replace("新冠", " COVID-19 ")
        title = title.replace("新冠肺炎", " COVID-19 ").replace("新冠", " COVID-19 ")
        subtitle = subtitle.replace("新冠肺炎", " COVID-19 ").replace("新冠", " COVID-19 ")
        news_en.at[index, 'special_title'] = translator.translate(special_title,lang_src='zh', lang_tgt='en')
        news_en.at[index, 'title'] = translator.translate(title,lang_src='zh', lang_tgt='en')
        news_en.at[index, 'subtitle'] = translator.translate(subtitle,lang_src='zh', lang_tgt='en')
        news_en.at[index, 'ban'] = translator.translate(ban,lang_src='zh', lang_tgt='en')
        
    
    ###### sleep for 1 second to prevent the connection error ######
    time.sleep(1)
    
    ###### translate the content ######
    content = row['content']
    if (type(content) != str):
        content = "Space"
    content = content.replace("新冠肺炎", " COVID-19 ")
    content = content.replace("新冠", " COVID-19 ")
    while len(content) > 3000:
        translate_text += translator.translate(content[:3000],lang_src='zh', lang_tgt='en')
        content = content[3000:]
    translate_text = translator.translate(content,lang_src='zh', lang_tgt='en')
    # print(content)
    # print(translate_text)
    news_en.at[index, 'content'] = translate_text.strip()
    # print()
    
    news_en.to_csv('./Sample_Datasets/XinMin_en.csv', index=False)