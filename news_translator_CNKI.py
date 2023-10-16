from google_trans_new_main.google_trans_new import google_translator  
from tqdm import tqdm
import pandas as pd
import time

######### Customized parameters #########
name = "环球时报"                                            # dataset name to be translated
short_columns = ['Title', 'Keywords']                       # columns that containing short content that can be translated at once
long_column = 'Contents'                                    # column that containing long content that should be translated separately
dictionary = {'新冠肺炎': ' COVID-19 ', '新冠': 'COVID-19' ,'清零': 'Zero-COVID'}   # dictionary for replacing some words
######### translate the dataset #########
# read the dataset
src_file = './Datasets/' + name + '.csv'
dst_file = './Datasets_en/' + name + '_en.csv'
news = pd.read_csv(src_file, encoding='utf-8-sig')
try:
    news_en = pd.read_csv(dst_file, encoding='utf-8-sig')
except:
    # if xinmin_en.csv does not exist, create it
    news_en = news.copy()
    news_en['translated'] = False   # add a column to indicate whether the news has been translated
    news_en.to_csv(dst_file, index=False, encoding='utf-8-sig')

translator = google_translator(url_suffix="com")    # initialize the translator

def has_chinese_characters(input_string):
    for char in input_string:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False

while True:
    try:
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
            if news_en.at[index, 'translated'] == True:
                continue
            short_content = ""
            for short_column in short_columns:
                if (type(row[short_column]) != str):
                    row[short_column] = "Space"
                title = "Space"
                # note that for xinmin, ban is very special that should be dealt with separately
                if short_column == 'ban':
                    slash_index = row[short_column].find('/')
                    if row[short_column][slash_index+1].isdigit():
                        row[short_column] = row[short_column][:slash_index] + '和' + row[short_column][slash_index+1:]
                short_content += row[short_column] + " || "
            short_content = short_content[:-4]
            for key in dictionary:
                short_content = short_content.replace(key, dictionary[key])
            try:
                short_content_en = translator.translate(short_content,lang_src='zh', lang_tgt='en')
                short_elements = short_content_en.split("||")
                if (len(short_elements) != len(short_columns)) or (has_chinese_characters(short_content_en)):
                    # print("Error: The number of elements in short_content_en is not 4. Try to translate them one by one.")
                    short_elements = short_content.split("||")
                    for i in range(len(short_elements)):
                        short_elements[i] = short_elements[i].strip()
                        for key in dictionary:
                            short_elements[i] = short_elements[i].replace(key, dictionary[key])
                        news_en.at[index, short_columns[i]] = translator.translate(short_elements[i],lang_src='zh', lang_tgt='en')
                else:
                    for i in range(len(short_elements)):
                        news_en.at[index, short_columns[i]] = short_elements[i].strip()
            except:
                print("The short_content that causes error: ", short_content)
                raise Exception("Error: Maybe Connection error. Try again.")
            
            ###### sleep for 1 second to prevent the connection error ######
            time.sleep(1)
            
            ###### translate the content ######
            content = row[long_column]
            if (type(content) != str):
                content = "Space"
            for key in dictionary:
                content = content.replace(key, dictionary[key])
            translate_text = ""
            while len(content) > 3000:
                translate_text += translator.translate(content[:3000],lang_src='zh', lang_tgt='en')
                content = content[3000:]
            translate_text = translator.translate(content,lang_src='zh', lang_tgt='en')
            # print(content)
            # print(translate_text)
            news_en.at[index, long_column] = translate_text.strip()
            # print()
            news_en.at[index, 'translated'] = True
            news_en.to_csv(dst_file, index=False, encoding='utf-8-sig')
        break
    except:
        print("Error: Connection error. Try again.")
        time.sleep(1)
        continue

# remove the 'translated' mark column
news_en = news_en.drop(columns=['translated'])
news_en.to_csv(dst_file, index=False, encoding='utf-8-sig')