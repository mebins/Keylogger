import sys, math
import pandas as pd
from os.path import exists
import time
from pynput.keyboard import Key, Listener
import atexit


#event driven word token key logging for your own analysis

#DATABASE FOUNDATION
seconds = time.time()
creation_time = 0;
count = 0
keys = []
key_word = []
word_count = 0

#WPM CLOCK CYCLE 
wpm = 0
average_wpm = 0
wpm_cycled = 0
wpm_time = 0

#DICTIONARY FILTERS
word = {"om":0}

#DATABASE LOADER
existing = exists("WORD_DICTIONARY.xlsx")
if existing:
    sf = pd.read_excel("WORD_DICTIONARY.xlsx")
    bank = sf.to_dict()
    #print(bank)
    #print(bank[0])

    sf.columns = sf.columns.str.replace('Unnamed: 0', "Word")
    bank = sf.to_dict()
    for key in bank["Word"]:
        word[bank["Word"][key]] = bank["Count"][key]
    print("WORD COUNT TABLE FOR MAGICC STUDY: ")
    print(word)
else:
    print("WELCOME TO A FRESH DATABASE ON WORD MAGC STUDY")



allowed_letters = ['a','b','c','d','e','f','g','h','i','j','k','l',
                   'm','n','o','p','q','r','s','t','u','v','w','x','y','z',
                   "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O",
                   "P","Q","R","S","T","U","V","W","X","Y","Z"]

def on_press(key):
    global keys, count, key_word
    count+= 1
    tokenize(key)
    keys = []
    pass

def tokenize(key):
    global key_word, word_count, seconds, wpm_time, wpm, df
    k = str(key).replace("'","")
    if k in allowed_letters:
        key_word.append(k)
        print(key_word)
    if key == Key.backspace:
        if(len(key_word) > 0):
            key_word.pop(-1)
        print(key_word)
    if (key == Key.enter or key == Key.space) and len(key_word)>0:
        token = ("".join(key_word))
        key_word = []
        word_count += 1
        creation_time = time.time()
        delta_time = creation_time - seconds
        seconds = creation_time
        wpm_time += delta_time

        wpm_cycled = math.floor(wpm_time)/60
        token = token.lower()
        if wpm_cycled >= 1:
            if word_count > 120 :
                print(" WPM STATS: " + str(word_count/wpm_cycled))
        
        if word.get(token):
            print("Words Enterted: " + str(word[token]))
            word[token] = word.get(token)+1  
        else:
            word[token] = 1
            
        #write_file(token)
        print(token + " : " + str(word[token]))

        print("WORD COUNT: "+ str( word_count) + " TIME: " + str(wpm_time) +
              " WPM CYCLES: " + str(wpm_cycled))
        
def write_file(key):
    with open("Christ Word.txt","a") as f:
        f.write(key)
        f.write("\n")
        
def on_release(key):
    if key == Key.esc:
        save()
    pass

def save():
    df = pd.DataFrame( data=word, index=["Count"])    
    df =(df.T)
    df.to_excel("word_dictionary.xlsx")
    print("SAVED LOG: ")
    print(df)
    return False

def on_each_key_press(key):
    keystrokes.append(key)
    
def main():
    print("MEBIN'S KEY STROKE HASHTABLER STARTED")
    atexit.register(save)
main()

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
    

    

    

