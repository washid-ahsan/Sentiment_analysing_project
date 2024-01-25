#!/usr/bin/env python
# coding: utf-8

# In[18]:


#import required library
import customtkinter
from tkinter import messagebox
from tkinter import filedialog
import string
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

#cleaning text 
def clean_text(msg):
    sp_words=stopwords.words('english')
    sp_words.remove('not')
    sp_words.remove("don't")
    sp_words.remove("didn't")
    sp_words.remove("hasn't")
    sp_words.remove("haven't")
    sp_words.remove("wasn't")
    sp_words.remove("weren't")

    def remove_punct(msg):
        return re.sub(f'[{string.punctuation}]','',msg)

    def remove_stopwds(msg):
        words=word_tokenize(msg)
        new_words=[]
        for w in words:
            if(w not in sp_words):
                new_words.append(w)
        return " ".join(new_words)

    def stemming(msg):
        ps=PorterStemmer()
        words=word_tokenize(msg)
        new_words=[]
        for w in words:
            new_words.append(ps.stem(w))
        return " ".join(new_words) 
    
    X1=remove_punct(msg)
    X2=X1.lower()
    X3=remove_stopwds(X2)
    X4=stemming(X3)
    return X4
#-----------------------------------------------------------------------------------------------------------------
#load the testing data 
df=pd.read_csv('Restaurant_Reviews.txt',delimiter="\t")
df.Review=list(map(clean_text,df.Review))
cv=CountVectorizer(binary=False,ngram_range=(1,2))
X=cv.fit_transform(df.Review).toarray()
y=df.Liked
clf=MultinomialNB()
clf.fit(X,y)

#-------------------------------------------------------------------------------------------------------------------
#creating a window with one frame which is unchangble

app = customtkinter.CTk()
app.geometry("2000x900")
app.state("zoomed")
customtkinter.set_default_color_theme("blue")
customtkinter.set_appearance_mode("dark")
app.resizable(False, False)
app.title("Review Analysing System")
frame1=customtkinter.CTkFrame(master=app,height=100, width=600,fg_color="#556B2F",border_color="#FFCC70",border_width=2)
frame1.pack()
label = customtkinter.CTkLabel(master=app,text="Review Analysing System",font=("Footlight MT Light",50,"underline"),text_color="#FFCC70",bg_color="#556B2F",)
label.place(x=520,y=20)


#defining all function
def predict_single(entry_user,lbl_result):
    user_review=entry_user.get("1.0", "end-1c")
    ct=clean_text(user_review)
    X_test=cv.transform([ct]).toarray()
    pred=clf.predict(X_test)
    if(pred[0]==0):
        lbl_result.configure(text="Not Liked",fg_color="red")
    else:
        lbl_result.configure(text="Liked",fg_color="green")

def predict_save(entry_src,entry_dest):        
    srcpath=entry_src.get()
    destpath=entry_dest.get()
    df=pd.read_csv(srcpath,names=['Review'])
    X=df.Review.map(clean_text)
    X_test=cv.transform(X).toarray()  
    pred=clf.predict(X_test)
    result_df=pd.DataFrame()
    result_df['Review']=df.Review
    result_df['Sentiment']=pred
    result_df['Sentiment']=result_df['Sentiment'].map({0:"Not Liked",1:"Liked"})
    result_df.to_csv(destpath,index=False,sep="\t")
    messagebox.showinfo('Result',"Prediction Done...")



def logout():
    option=messagebox.askyesno('Confirmation','Do you want to logout?')
    if(option==True):
        home_screen()
    else:
        pass

def home_screen():
    
    frm=customtkinter.CTkFrame(master=app,height=350, width=700,fg_color="#8B4513",border_color="#FF7F24",border_width=4)
    frm.place(relx=0,rely=.15,relwidth=1,relheight=1)

    frame2=customtkinter.CTkFrame(master=app,height=350, width=700,fg_color="#8B3A62",border_color="#EE82EE",border_width=2)
    frame2.place(x=420,y=250)

    label_user = customtkinter.CTkLabel(master=frame2,text="USER",font=("Footlight MT Light",50,"bold",),text_color="#141414",)
    label_user.place(x=20,y=80)

    entry_user = customtkinter.CTkEntry(master=frame2,width=200,height=40,placeholder_text="enter user name...",placeholder_text_color="#CFCFCF",corner_radius=20)
    entry_user.place(x=320,y=80)
    entry_user.focus()


    label_passwrd = customtkinter.CTkLabel(master=frame2,text="PASSWORD",font=("Footlight MT Light",50,"bold",),text_color="#141414",)
    label_passwrd.place(x=20,y=200)

    entry_pass = customtkinter.CTkEntry(master=frame2,width=200,height=40,placeholder_text="enter password...",placeholder_text_color="#CFCFCF",show="*",corner_radius=20)
    entry_pass.place(x=320,y=200)

    btn_login=customtkinter.CTkButton(master=app,width=200,height=50,text="Login",command=lambda:welcome_screen(entry_user,entry_pass) ,corner_radius=30 ,fg_color="#030303",hover_color="#4158D0",bg_color="#8B4513", border_color="#FF7F24", border_width=2,)
    btn_login.place(x=700,y=650)

def welcome_screen(entry_user=None,entry_pass=None):
    if(entry_user!=None and entry_pass!=None):
        user=entry_user.get()
        pwd=entry_pass.get()
    else:
        user="admin"
        pwd="admin"
    if(len(user)==0 or len(pwd)==0):
        messagebox.showwarning("validation","Please fill both fields")
        return
    else:
        if(user=="admin" or pwd=="admin"):
            
            custom_font =("Times",30,'bold')
            
            frm=customtkinter.CTkFrame(master=app,height=350, width=700,fg_color="#8B4513",border_color="#FF7F24",border_width=4)
            frm.place(relx=0,rely=.15,relwidth=1,relheight=1)

            btn_single=customtkinter.CTkButton(master=frm,command=lambda:single_feedback_screen(),text="Single Feedback Prediction",font=("Footlight MT Light", 30,'bold'),fg_color="#030303",width=25,height=100,hover_color="#4158D0",border_color="#FF7F24",border_width=4,corner_radius=80)
            btn_single.place(relx=.33,rely=.2)

            btn_bulk=customtkinter.CTkButton(master=frm,command=lambda:bulk_feedback_screen(),text="Bulk Feedback Prediction",font=("Footlight MT Light", 30,'bold'),fg_color="#030303",width=25,height=100,hover_color="#4158D0",border_color="#FF7F24",border_width=4,corner_radius=80)
            btn_bulk.place(relx=.33,rely=.4)

            btn_logout=customtkinter.CTkButton(frm,command=lambda:logout(),text="logout",font=("Footlight MT Light", 30,'bold'),width=25,height=100,hover_color="#4158D0",fg_color="#030303",border_color="#FF7F24",border_width=4,corner_radius=80)
            btn_logout.place(relx=.9,rely=0)
        else:
            messagebox.showerror("Fail","Invalid Username/Password")


            
def single_feedback_screen():
    frm=customtkinter.CTkFrame(master=app,height=350, width=700,fg_color="#8B4513",border_color="#FF7F24",border_width=4)
    frm.place(relx=0,rely=.15,relwidth=1,relheight=1)
    
    lbl_user=customtkinter.CTkLabel(frm,text="Enter Feedback:",font=("Footlight MT Light", 30,'bold'),bg_color='green')
    lbl_user.place(relx=.26,rely=.3)

    entry_user=customtkinter.CTkTextbox(frm,font=('',20),border_width=10,width=500,height=200)
    entry_user.place(relx=.45,rely=.2)
    entry_user.focus()

    lbl_result=customtkinter.CTkLabel(frm,text="Prediction:",font=("Footlight MT Light", 30,'bold'),bg_color='black')
    lbl_result.place(relx=.26,rely=.55)

    btn_predict=customtkinter.CTkButton(frm,command=lambda:predict_single(entry_user,lbl_result),text="Predict",font=("Footlight MT Light", 30,'bold'),width=25,height=100,hover_color="#4158D0",fg_color="#030303",border_color="#FF7F24",border_width=4,corner_radius=80)
    btn_predict.place(relx=.47,rely=.48)

    btn_back=customtkinter.CTkButton(frm,command=lambda:welcome_screen(),text="Back",font=("Footlight MT Light", 30,'bold'),width=25,height=100,hover_color="#4158D0",fg_color="#030303",border_color="#FF7F24",border_width=4,corner_radius=80)
    btn_back.place(relx=.9,rely=0)

def bulk_feedback_screen():
    frm=customtkinter.CTkFrame(master=app,height=350, width=700,fg_color="#8B4513",border_color="#FF7F24",border_width=4)
    frm.place(relx=0,rely=.15,relwidth=1,relheight=1)
    
    lbl_src=customtkinter.CTkLabel(frm,text="Select Source file:",font=("Footlight MT Light", 30,'bold'),bg_color='green')
    lbl_src.place(relx=.16,rely=.2)
    
    lbl_dest=customtkinter.CTkLabel(frm,text="Select Dest Directory:",font=("Footlight MT Light", 30,'bold'),bg_color='green')
    lbl_dest.place(relx=.16,rely=.32)
    

    entry_src=customtkinter.CTkEntry(frm,font=('',20),border_width=10,width=350)
    entry_src.place(relx=.43,rely=.2)
    entry_src.focus()

    entry_dest=customtkinter.CTkEntry(frm,font=('',20),border_width=10,width=350)
    entry_dest.place(relx=.43,rely=.32)
    
    btn_browse=customtkinter.CTkButton(frm,command=lambda:browse(entry_src),text="Browse",font=("Footlight MT Light", 30,'bold'),width=25,height=80,hover_color="#4158D0",fg_color="#030303",border_color="#FF7F24",border_width=4,corner_radius=80)
    btn_browse.place(relx=.74,rely=.2)

    btn_browse2=customtkinter.CTkButton(frm,command=lambda:browse2(entry_dest),text="Browse",font=("Footlight MT Light", 30,'bold'),width=25,height=80,hover_color="#4158D0",fg_color="#030303",border_color="#FF7F24",border_width=4,corner_radius=80)
    btn_browse2.place(relx=.74,rely=.32)
    
    btn_login=customtkinter.CTkButton(frm,command=lambda:predict_save(entry_src,entry_dest),text="Predict and save",font=("Footlight MT Light", 30,'bold'),width=25,height=100,hover_color="#4158D0",fg_color="#030303",border_color="#FF7F24",border_width=4,corner_radius=80)
    btn_login.place(relx=.47,rely=.6)

    btn_back=customtkinter.CTkButton(frm,command=lambda:welcome_screen(),text="Back",font=("Footlight MT Light", 30,'bold'),width=25,height=100,hover_color="#4158D0",fg_color="#030303",border_color="#FF7F24",border_width=4,corner_radius=80)
    btn_back.place(relx=.9,rely=0)
    
def browse(entry_path):
    file_path=filedialog.askopenfilename()
    entry_path.delete(0,END)
    entry_path.insert(0,file_path)

def browse2(entry_path):
    file_path=filedialog.askdirectory()+"/result.txt"
    entry_path.delete(0,END)
    entry_path.insert(0,file_path)                


home_screen()
app.mainloop()


# In[ ]:





# In[ ]:




