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
    Title = row['Title']
    if (type(Title) != str):
        Title = "Space"
    Keywords = row['Keywords']
    if (type(Keywords) != str):
        Keywords = "Space"
    Author = row['Author']
    if (type(Author) != str):
        Author = "Space"
    short_content = Title + " || " + Keywords + " || " + Author
    short_content = short_content.replace("新冠肺炎", " COVID-19 ")
    short_content = short_content.replace("新冠", " COVID-19 ")
    try:
        short_content_en = translator.translate(short_content,lang_src='zh', lang_tgt='en')
        # print(short_content)
        # print(short_content_en)
        short_elements = short_content_en.split("||")
        if len(short_elements) != 4:
            # print("Error: The number of elements in short_content_en is not 4. Try to translate them one by one.")
            Title = Title.replace("新冠肺炎", " COVID-19 ").replace("新冠", " COVID-19 ")
            Keywords = Keywords.replace("新冠肺炎", " COVID-19 ").replace("新冠", " COVID-19 ")
            Author = Author.replace("新冠肺炎", " COVID-19 ").replace("新冠", " COVID-19 ")
            news_en.at[index, 'Title'] = translator.translate(Title,lang_src='zh', lang_tgt='en')
            news_en.at[index, 'Keywords'] = translator.translate(Keywords,lang_src='zh', lang_tgt='en')
            news_en.at[index, 'Author'] = translator.translate(Author,lang_src='zh', lang_tgt='en')
        else:     
            news_en.at[index, 'Title'] = short_elements[0].strip()
            news_en.at[index, 'Keywords'] = short_elements[1].strip()
            news_en.at[index, 'Author'] = short_elements[2].strip()
    except:
        # print('There is an error. Try to translate them one by one.'')
        Title = Title.replace("新冠肺炎", " COVID-19 ").replace("新冠", " COVID-19 ")
        Keywords = Keywords.replace("新冠肺炎", " COVID-19 ").replace("新冠", " COVID-19 ")
        Author = Author.replace("新冠肺炎", " COVID-19 ").replace("新冠", " COVID-19 ")
        news_en.at[index, 'Title'] = translator.translate(Title,lang_src='zh', lang_tgt='en')
        news_en.at[index, 'Keywords'] = translator.translate(Keywords,lang_src='zh', lang_tgt='en')
        news_en.at[index, 'Author'] = translator.translate(Author,lang_src='zh', lang_tgt='en')
        
    
    ###### sleep for 1 second to prevent the connection error ######
    time.sleep(1)
    
    ###### translate the content ######
    content = row['Contents']
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
    news_en.at[index, 'Contents'] = translate_text.strip()
    # print()
    
    news_en.to_csv('./Users/karan/Documents/GitHub/local_central-level-propaganda/Datasets_en/JFdaily_en.csv', index=False, encoding='utf-8-sig')