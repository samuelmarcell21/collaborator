from django.shortcuts import render
from django.http import HttpResponseRedirect

from author.models import Papers, Authors
from topic.models import Topics, Data_sumcount_topic
from affiliation.models import Affiliations


from django.shortcuts import render
from author.models import Papers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from topic.models import Subtopics

#SVG
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings("ignore")
import operator


# Untuk Search
import re
import numpy as np
import pandas as pd
from pprint import pprint

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Gensim

from gensim.corpora import Dictionary
from gensim.corpora.mmcorpus import MmCorpus
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from nltk.corpus import stopwords

# spacy for lemmatization
import spacy

# Plotting tools
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt

# Enable logging for gensim - optional
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

warnings.filterwarnings("ignore",category=DeprecationWarning)
import pandas as pd

from django.views.generic import ListView

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from gensim.similarities import MatrixSimilarity

from gensim.models import TfidfModel
from gensim.matutils import cossim as CS

import pickle
from gensim.similarities.docsim import Similarity
from gensim.test.utils import get_tmpfile
import gensim
from IPython.display import clear_output

global color

global warna 

warna=['#2d97ab', '#ed164f', '#72801b', '#755e5c', '#e9ce86', '#8851d2', '#ccbd73', '#7acdd3', '#7254da', '#655e2d', '#75377d', '#bea56b'
, '#e18a39', '#cef397', '#22875c', '#a3c6ae', '#d15ac9', '#7758fb', '#63b9c8', '#fa74b6']

def index(request):
    if request.method=='GET':
        topic = Topics.objects.all().order_by('-total_publication')[:3]
        topik = []
        for i in topic:
            topik.append(i.id_topic)
        
        print(topik)

        topik_1 = Topics.objects.filter(id_topic=topik[0]).first()

        topik_2 = Topics.objects.filter(id_topic=topik[1]).first()

        topik_3 = Topics.objects.filter(id_topic=topik[2]).first()

        affi_1 = Affiliations.objects.filter(topik_dominan1=topik[0]).order_by('-nilai_dominan1')[:1]

        affi_2 = Affiliations.objects.filter(topik_dominan1=topik[1]).order_by('-nilai_dominan1')[:1]

        affi_3 = Affiliations.objects.filter(topik_dominan1=topik[2]).order_by('-nilai_dominan1')[:1]

        author_1 = Authors.objects.filter(topik_dominan1=topik[0]).order_by('-nilai_dominan1')[:1]

        author_2 = Authors.objects.filter(topik_dominan1=topik[1]).order_by('-nilai_dominan1')[:1]

        author_3 = Authors.objects.filter(topik_dominan1=topik[2]).order_by('-nilai_dominan1')[:1]

        affiliation = Affiliations.objects.all().order_by('-total_publication')[:5]
        univ = []
        for i in affiliation:
            univ.append(i.initial_univ)
        topik=[1,16,11]

        data_akhir,listdict,listvis2,datatopics,data_warna=SVG(topik)
        topik1_data,topik1 = getData_sumcount_topik(topik[0])[:3]
        topik2_data,topik2 = getData_sumcount_topik(topik[1])[:3]
        topik3_data,topik3 = getData_sumcount_topik(topik[2])[:3]

        topik_filter = Topics.objects.all().order_by('topic_name')

        return render(request, 'find.html', {'affi_1':affi_1, 'affi_2':affi_2, 'affi_3':affi_3, 'author_1':author_1, 'author_2':author_2, 'author_3':author_3, 'topik_1':topik_1, 'topik_2':topik_2, 'topik_3':topik_3,
        'data':data_akhir,'nama_top':listdict,'datatopics':datatopics, 'topik_filter':topik_filter, 'topik1_data': topik1_data, 'topik2_data':topik2_data, 'topik3_data':topik3_data})

    else:
        chk = request.POST.getlist('id_topik')

        topic = Topics.objects.all().order_by('-total_publication')[:3]
        topikk = []
        for i in topic:
            topikk.append(i.id_topic)

        topik_1 = Topics.objects.filter(id_topic=topikk[0]).first()

        topik_2 = Topics.objects.filter(id_topic=topikk[1]).first()

        topik_3 = Topics.objects.filter(id_topic=topikk[2]).first()

        affi_1 = Affiliations.objects.filter(topik_dominan1=topikk[0]).order_by('-nilai_dominan1')[:1]

        affi_2 = Affiliations.objects.filter(topik_dominan1=topikk[1]).order_by('-nilai_dominan1')[:1]

        affi_3 = Affiliations.objects.filter(topik_dominan1=topikk[2]).order_by('-nilai_dominan1')[:1]

        author_1 = Authors.objects.filter(topik_dominan1=topikk[0]).order_by('-nilai_dominan1')[:1]

        author_2 = Authors.objects.filter(topik_dominan1=topikk[1]).order_by('-nilai_dominan1')[:1]

        author_3 = Authors.objects.filter(topik_dominan1=topikk[2]).order_by('-nilai_dominan1')[:1]

        affiliation = Affiliations.objects.all().order_by('-total_publication')[:5]
        univ = []
        for i in affiliation:
            univ.append(i.initial_univ)

        df=pd.DataFrame()

        topik = []
        for i in chk:
            topik.append(int(i))

        
        data_akhir,listdict,listvis2,datatopics,data_warna=SVG(topik)
        # topik1_data = getData_sumcount_topik(topik[0])[:3]
        # topik2_data = getData_sumcount_topik(topik[1])[:3]
        # topik3_data = getData_sumcount_topik(topik[2])[:3]

        topik_filter = Topics.objects.all().order_by('topic_name')

        if len(chk) == 1:
            topik1_data, topik1 = getData_sumcount_topik(topik[0])
            return render(request, 'find.html', {'affi_1':affi_1, 'affi_2':affi_2, 'affi_3':affi_3, 'author_1':author_1, 'author_2':author_2, 'author_3':author_3, 'topik_1':topik_1, 'topik_2':topik_2, 'topik_3':topik_3,
            'data':data_akhir,'nama_top':listdict,'datatopics':datatopics, 'topik_filter':topik_filter, 'topik1_data': topik1_data, 'topik1':topik1})
        elif len(chk) == 2:
            topik1_data, topik1 = getData_sumcount_topik(topik[0])
            topik2_data, topik2 = getData_sumcount_topik(topik[1])
            return render(request, 'find.html', {'affi_1':affi_1, 'affi_2':affi_2, 'affi_3':affi_3, 'author_1':author_1, 'author_2':author_2, 'author_3':author_3, 'topik_1':topik_1, 'topik_2':topik_2, 'topik_3':topik_3,
            'data':data_akhir,'nama_top':listdict,'datatopics':datatopics, 'topik_filter':topik_filter, 'topik1_data': topik1_data, 'topik1':topik1, 'topik2_data':topik2_data, 'topik2':topik2})
        elif len(chk) == 3:
            topik1_data, topik1 = getData_sumcount_topik(topik[0])
            topik2_data, topik2 = getData_sumcount_topik(topik[1])
            topik3_data, topik3 = getData_sumcount_topik(topik[2])
            return render(request, 'find.html', {'affi_1':affi_1, 'affi_2':affi_2, 'affi_3':affi_3, 'author_1':author_1, 'author_2':author_2, 'author_3':author_3, 'topik_1':topik_1, 'topik_2':topik_2, 'topik_3':topik_3,
            'data':data_akhir,'nama_top':listdict,'datatopics':datatopics, 'topik_filter':topik_filter, 'topik1_data': topik1_data, 'topik1':topik1, 'topik2_data':topik2_data, 'topik2':topik2, 'topik3_data':topik3_data, 'topik3':topik3})



def search(request):
    if request.method == 'POST':
        global catch
        catch = request.POST['title']

        id_artikel,topic = rekomendasi(catch)

        # global user_list
        global user_list

        user_list = Papers.objects.filter(id_pub__in=id_artikel).order_by('id_pub')[:10]

        topic_obj = Topics.objects.get(id_topic=topic)

        print(topic_obj)

        page = request.GET.get('page', 1)
        paginator = Paginator(user_list, 10)

        global author_rekomen
        author_rekomen = Authors.objects.filter(topik_dominan1=topic).order_by('-nilai_dominan1')[:4]

        global users

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        
        context = {
            'title': 'Halaman Utama',
            'topik': topic_obj,
            'catch': catch,
            'users' : users,
            'author': author_rekomen,
            'user_list': user_list,
        }

        return render(request, 'search.html', context)
    
    else:
        page = request.GET.get('page', 1)
        paginator = Paginator(user_list, 10)

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        
        context = {
            'users' : users,
            'catch': catch,
            'author': author_rekomen,
            'topic_obj': topic_obj,
        }

        return render(request, 'search.html', context)

# fungsi svg
#fungsi scaling kolom batas atas
scaler = MinMaxScaler(feature_range=(-1.0, 1.0))
col = ["Topik","Year","xAwalAtas","yAwalAtas","xLengkung1","yLengkung1atas","xLengkung2","yLengkung2atas","xAkhirAtas","yAkhirAtas","xAkhirBawah","yAkhirBawah","yLengkung2bawah","yLengkung1bawah","xAwalBawah","yAwalBawah"]
def fatas(row):
    value = scaler.transform([[row['kumAtas']]])
    return round(float(value),4)

#fungsi scaling kolom batas bawah
def fbawah(row):
    value = scaler.transform([[row['kumBawah']]])
    return round(float(value),4)

def scale_data(data_awal):
    df_scaled=pd.DataFrame()
    
    atas = np.array(data_awal['kumAtas']) #mengambil nilai dari kolom batas atas
    bawah = np.array(data_awal['kumBawah']) #mengambil nilai dari kolom batas bawah
    gabungan = np.append(atas,bawah).reshape(len(bawah)+len(atas),1) # menggabung nilai batas atas dan batas bawah 
    
    #scaling dan proses fit data
    scaler.fit(gabungan)
    
    #transform nilai batas atas dan batas bawah
    data_awal['Scale Atas']=data_awal.apply(fatas,axis=1)
    data_awal['Scale Bawah']=data_awal.apply(fbawah,axis=1)
    
    df_scaled=pd.concat([df_scaled,data_awal])
    
    return df_scaled

class grafik:
    def __init__(self, Topik, Year, scale_atas, scale_bawah, kumAtas, kumBawah,HASIL):
        self.Topik = Topik
        self.Year = Year
        self.xAwalAtas=0
        self.yAwalAtas=0
        self.xLengkung1=0
        self.yLengkung1atas=0
        self.xLengkung2=0
        self.yLengkung2atas=0
        self.xAkhirAtas=0
        self.yAkhirAtas=0
        self.xAkhirBawah=0
        self.yAkhirBawah=0
        self.yLengkung2bawah=0
        self.yLengkung1bawah=0
        self.xAwalBawah=0
        self.yAwalBawah=0
        self.kumAtas=kumAtas
        self.kumBawah=kumBawah
        
        #menghitung titik y
        tahun = self.Year
        topik = self.Topik
        if(tahun==2010):
            self.yAwalAtas=350
            self.yAwalBawah=350
        else:
            self.yAwalAtas=HASIL[(HASIL['Year']==tahun-1) & (HASIL['Topik']==topik)]['yAkhirAtas'].values[0]
            self.yAwalBawah=HASIL[(HASIL['Year']==tahun-1) & (HASIL['Topik']==topik)]['yAkhirBawah'].values[0]
        self.yAkhirAtas = (350 - abs(scale_atas*325))
        if(scale_bawah) > 0:
            self.yAkhirBawah = (350 - abs(scale_bawah*325)) 
        else:
            self.yAkhirBawah = (350 + abs(scale_bawah*325))
            
        #menghitung titik x
        if(tahun==2010):
            self.xAwalAtas=0
            self.xAwalBawah=0
        else:
            self.xAwalAtas=HASIL[(HASIL['Year']==tahun-1) & (HASIL['Topik']==topik)]['xAkhirAtas'].values[0]
            self.xAwalBawah=HASIL[(HASIL['Year']==tahun-1) & (HASIL['Topik']==topik)]['xAkhirBawah'].values[0]
        self.xAkhirAtas = self.xAwalAtas + 150
        self.xAkhirBawah = self.xAwalBawah + 150
    
        #menghitung nilai lengkung
        # xLengkung
        self.xLengkung1 = self.xAwalAtas + 75
        self.xLengkung2 = self.xAkhirAtas - 75

        rangeLengkungAtas = abs(self.yAkhirAtas-self.yAwalAtas)/8
        #yLengkung1atas yang kiri, yLengkung2atas yang kanan  
        self.yLengkung1atas = self.yAwalAtas - rangeLengkungAtas
        self.yLengkung2atas = self.yAkhirAtas + rangeLengkungAtas
        #print(xLengkung1, xLengkung2, rangeLengkung, yLengkung1, yLengkung2)

        rangeLengkungBawah = abs(self.yAkhirBawah-self.yAwalBawah)/8
        # yLengkung1bawah yang kiri, yLengkung2bawah yang kanan
        self.yLengkung1bawah = self.yAwalBawah + rangeLengkungBawah
        self.yLengkung2bawah = self.yAkhirBawah - rangeLengkungBawah
    
    def ubahTitikY(self,yAkhirBawah,yAkhirAtas) :
        self.yAkhirBawah=yAkhirBawah
        self.yAkhirAtas=yAkhirAtas
        
        
        rangeLengkungAtas = abs(self.yAkhirAtas-self.yAwalAtas)/8
        #yLengkung1atas yang kiri, yLengkung2atas yang kanan  
        self.yLengkung1atas = self.yAwalAtas - rangeLengkungAtas
        self.yLengkung2atas = self.yAkhirAtas + rangeLengkungAtas
        #print(xLengkung1, xLengkung2, rangeLengkung, yLengkung1, yLengkung2)

        rangeLengkungBawah = abs(self.yAkhirBawah-self.yAwalBawah)/8
        # yLengkung1bawah yang kiri, yLengkung2bawah yang kanan
        self.yLengkung1bawah = self.yAwalBawah + rangeLengkungBawah
        self.yLengkung2bawah = self.yAkhirBawah - rangeLengkungBawah

    def hasil(self):
        data=[self.Topik,self.Year,self.xAwalAtas,self.yAwalAtas,self.xLengkung1,self.yLengkung1atas,self.xLengkung2,
        self.yLengkung2atas,self.xAkhirAtas,self.yAkhirAtas,self.xAkhirBawah,self.yAkhirBawah,
        self.yLengkung2bawah,self.yLengkung1bawah,self.xAwalBawah,self.yAwalBawah]
        dftmp=pd.DataFrame([data],columns= col)
        return(dftmp)


def Gambar(sorted_listGraf):
    for i in range (len(sorted_listGraf)-1):
#         print('hai')
        new_yAkhirBawah=(sorted_listGraf[i].yAkhirAtas+sorted_listGraf[i].yAkhirBawah) / 2 - 4 # untuk yang diatas
        sorted_listGraf[i].ubahTitikY(new_yAkhirBawah,sorted_listGraf[i].yAkhirAtas) #atas 
        new_yAkhirAtas = sorted_listGraf[i].yAkhirBawah + 4 #untuk yang di bawah 
        sorted_listGraf[i+1].ubahTitikY(sorted_listGraf[i+1].yAkhirBawah,new_yAkhirAtas) #bawah
    return (sorted_listGraf)

def BuatHasil(sorted_listGraf,HASIL):
    for i in sorted_listGraf:
        dftmp=i.hasil()
        HASIL=pd.concat([HASIL,dftmp],axis=0)
    return HASIL


def SVG(listtopik):
    df=pd.DataFrame()
    topik=listtopik
    listdict=[]
    for top in topik:
        obj = Topics.objects.get(id_topic=top)
        data=obj.svg.all().order_by('Year').values()
        temp=pd.DataFrame(data)
        temp2={'name':obj.topic_name}
        listdict.append(temp2)
        # namatopik.append()
        df=pd.concat([df,temp])
    datatopics=Topics.objects.all().values()
    tes=Topics.objects.filter(id_topic=top).values().first()
    data = scale_data(df)#scaling data
    data = data.rename(columns={"topic_id": "Topik"})
    # print(data.info())
    data = data.astype({"Topik": float, "Year": float, "kumAtas": float, "kumBawah": float, "batasAtas": float, "batasBawah": float})
    # print(data)
    years=data.Year.unique()
    HASIL = pd.DataFrame(columns=col)
    # print( data[data['Topik']==1])
    for year in years:
        listGraf=[]
        for top in topik:
            a = data[(data['Topik']==top) & (data['Year']==year)]
            # print(a)
            graf=grafik(a['Topik'].values[0],a['Year'].values[0],a['Scale Atas'].values[0],a['Scale Bawah'].values[0],a['kumAtas'].values[0],a['kumBawah'].values[0],HASIL)
            listGraf.append(graf)
        sorted_listGraf = sorted(listGraf, key=operator.attrgetter('kumAtas'), reverse=True)
        sorted_listGraf=Gambar(sorted_listGraf)
        HASIL=BuatHasil(sorted_listGraf,HASIL)
        HASIL=BuatHasil(listGraf,HASIL)
    HASIL['Color']=HASIL.apply(color,axis=1)
    HASIL=HASIL.reset_index(drop=True)
    # print(HASIL.info())
    # print(HASIL)
    data_akhir=HASIL.to_dict('records')

    #Visualisasi samping svg
    dfvis2=df[['topic_id','Year','batasAtas']]
    dfvis2 = dfvis2.rename(columns={"topic_id": "Topik"})
    dfvis2 = dfvis2.astype({"Topik": float, "Year": float, "batasAtas": float})
    dfvis2= dfvis2[dfvis2['Year']>2017]
    dfvis2['Color']=dfvis2.apply(color,axis=1)
    listvis2=[]
    flag=0
    for top in dfvis2.Topik.unique():
        datay=[]
        for index,row in dfvis2[dfvis2['Topik']==top].iterrows():
            datay.append(row['batasAtas'])
        data={'x':listdict[flag]['name'],'y':datay,'Color':row['Color']}
        flag+=1
        listvis2.append(data)
    # print(datatopics)
    warna = HASIL.drop_duplicates(subset=['Topik', 'Color'])
    warna = warna[['Topik', 'Color']]
    # print(warna)
    data_warna = warna.to_dict()
    return data_akhir,listdict,listvis2,datatopics,data_warna
    # return render(request, 'author/SVG.html',{'data':data_akhir,'nama_top':listdict,'data2':listvis2,'datatopics':datatopics})


def color(row):
    if(row['Topik']==0):
        val='#2d97ab'
    elif(row['Topik']==1):
        val='#ed164f'
    elif(row['Topik']==2):
        val='#72801b'
    elif(row['Topik']==3):
        val='#755e5c'
    elif(row['Topik']==4):
        val='#e9ce86'
    elif(row['Topik']==5):
        val='#8851d2'
    elif(row['Topik']==6):
        val='#ccbd73'
    elif(row['Topik']==7):
        val='#7acdd3'
    elif(row['Topik']==8):
        val='#7254da'
    elif(row['Topik']==9):
        val='#655e2d'
    elif(row['Topik']==10):
        val='#75377d'
    elif(row['Topik']==11):
        val='#bea56b'
    elif(row['Topik']==12):
        val='#e18a39'
    elif(row['Topik']==13):
        val='#cef397'
    elif(row['Topik']==14):
        val='#22875c'        
    elif(row['Topik']==15):
        val='#a3c6ae'       
    elif(row['Topik']==16):
        val='#d15ac9'       
    elif(row['Topik']==17):
        val='#7758fb'       
    elif(row['Topik']==18):
        val='#63b9c8'
    elif(row['Topik']==19):
        val='#fa74b6'               
    return val


def vis_author(nidn):
    nidn_author=nidn 
    author = Authors.objects.get(nidn=nidn_author)
    df=pd.DataFrame(columns=['Topic','Year','Count','Sumcite'])
    YEAR=['2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']
    TOPIK=[author.topik_dominan1_id,author.topik_dominan2_id,author.topik_dominan3_id]
    TOPIK_NAMA=[author.topik_dominan1.topic_name,author.topik_dominan2.topic_name,author.topik_dominan3.topic_name]
    print(TOPIK)
    for top in TOPIK:
        papers_top = author.paper.filter(topic_id=top)
        year_dis = papers_top.values('year').distinct()
        df_temp=pd.DataFrame(columns=['Topic','Year','Count','Sumcite'])
        count=[0]*11
        sumcite=[0]*11
        topic=[top]*11
        for year in year_dis:
            cou=papers_top.filter(year=year['year']).count()
            sumc=papers_top.filter(year=year['year']).aggregate(Sum('cite'))['cite__sum']
            if(sumc is None):
                sumc=0
            yea=int(year['year'])-2010
            count[yea]=cou
            sumcite[yea]=int(sumc)
        df_temp['Topic']=topic
        df_temp['Year']=YEAR
        df_temp['Count']=count
        df_temp['Sumcite']=sumcite
        # print(df_temp)
        df=pd.concat([df,df_temp])
    df=df.reset_index(drop=True)
    list_count=[]
    list_sum=[]
    df = df.rename(columns={"Topic": "Topik"})
    df = df.astype({"Topik": int})
    df['Color']=df.apply(color,axis=1)
    flag=0
    for top in df.Topik.unique():
        datacount=[]
        datasum=[]
        for index,row in df[df['Topik']==top].iterrows():
            datacount.append(row['Count'])
            datasum.append(row['Sumcite'])
        datac={'x':TOPIK_NAMA[flag],'y':datacount,'Color':row['Color']}
        datas={'x':TOPIK_NAMA[flag],'y':datasum,'Color':row['Color']}
        flag+=1
        list_count.append(datac)
        list_sum.append(datas)
    # print(list_count)
    # print(list_sum)

    return(list_count,list_sum)
    # return render(request, 'author/cobajax.html',{'data_count':list_count,'data_sum':list_sum,'author':author})


def getData_sumcount_topik(top):
    datasumcount=Data_sumcount_topic.objects.filter(topic_id=top).order_by('-year')
    topic=Topics.objects.filter(id_topic=top).first()
    df = pd.DataFrame.from_records(datasumcount.values_list(),columns=['id','idTopic','Year','Count','Sumcite','id_univ'])
    Year=df['Year']
    Count=df['Count']
    Sumcite=df['Sumcite']
    id_univ=df['id_univ']
    leng=len(Year)
    pubstat=['-']*leng
    pubcolor=['-']*leng
    citestat=['-']*leng
    citecolor=['-']*leng
    # print(df)
    for i in range(len(Year)-1):
        if(int(Count[i])==int(Count[i+1])):
            pubstat[i]='-'
        elif(int(Count[i])>int(Count[i+1])):
            pubstat[i]='up'
            pubcolor[i]='green'
        else:
            pubstat[i]='down'
            pubcolor[i]='red'
        if(int(Sumcite[i])==int(Sumcite[i+1])):
            citestat[i]='-'          
        elif(int(Sumcite[i])>int(Sumcite[i+1])):
            citestat[i]='up'
            citecolor[i]='green'
        else:
            citestat[i]='down'
            citecolor[i]='red'
    # print(pubstat,citestat)
    new_df = pd.DataFrame({'year':Year, 'pubcount':Count, 'sumcite':Sumcite,'citestat':citestat,'pubstat':pubstat,'id_univ':id_univ,'pubcolor':pubcolor,'citecolor':citecolor})
    data=new_df.to_dict('records')
    # bisa di batasin jumlah row yang mau d passing di sini
    return(data[:3], topic)

def rekomendasi(input):
    data = [input]
    id2word = Dictionary.load('pdupt_website/id2word_new.dict')
    corpus = MmCorpus('pdupt_website/corpus_new.mm')
    df = pd.read_csv('pdupt_website/reduksifix.csv')
    with open("pdupt_website/lemma_new.txt", "rb") as fp:   #Pickling
        data_lemmatized=pickle.load(fp)
    stop_words = stopwords.words('indonesian')
    stop_words2 = stopwords.words('english')
    stop_words.extend(stop_words2)
    stop_words.extend(['of','in','and','the','for','on','using','based','from','with','to','by','as','an','pengaruh'
                    ,'effect','analisis','at','pre','pro','analysis','berbasis','tahun','between','kualitas','method',
                    'metode','through','menggunakan','hasil'])
    # Remove Numbers
    data = [re.sub(" \d+",' ', sent) for sent in data]
    data = [re.sub('[^a-zA-Z]',' ', sent) for sent in data]
    # Remove new line characters
    data = [re.sub('\s+', ' ', sent) for sent in data]

    # Remove distracting single quotes
    data = [re.sub("\'", "", sent) for sent in data]

    def sent_to_words(sentences):
        for sentence in sentences:
            yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

    data = sent_to_words(data)
    data_words = list(data)
    # Build the bigram and trigram models
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100)  

    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)


    # Define functions for stopwords, bigrams, trigrams and lemmatization
    # from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
    def remove_stopwords(texts):
        return [[word for word in simple_preprocess(str(doc)) if word not in (stop_words or stop_words2)] for doc in texts]

    def make_bigrams(texts):
        return [bigram_mod[doc] for doc in texts]

    def make_trigrams(texts):
        return [trigram_mod[bigram_mod[doc]] for doc in texts]

    def lemmatization(texts):
        """https://spacy.io/api/annotation"""
        texts_out = []
        for sent in texts:
            doc = nlp(" ".join(sent)) 
            texts_out.append([token.lemma_ for token in doc])
        return texts_out

    # Remove Stop Words
    data_words_nostops = remove_stopwords(data_words)

    # # Form Bigrams
    data_words_bigrams = make_bigrams(data_words_nostops)

    nlp = spacy.load('en_core_web_sm')

    data_lemmatized_search = lemmatization(data_words_bigrams)

    #stem masing-masing kata yang ada
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    for x in range(len(data_lemmatized_search)-1):
        for y in range(len(data_lemmatized_search[x])-1):
            data_lemmatized_search[x][y] = stemmer.stem(data_lemmatized_search[x][y])

            # import gensim
    model = gensim.models.ldamodel.LdaModel.load('pdupt_website/mallet_18_lda.mdl', mmap='r') 
    new_doc_bow = id2word.doc2bow(data_lemmatized_search[0])
    hasil = model.get_document_topics(new_doc_bow)

    topic=0
    nilai =-99
    for i, row in (hasil):
        if(row>nilai):
            topic=i
            nilai=row

    df_topik=df.loc[df['Topic1'] == topic]
    df_topik = df_topik.astype({"id_judul": int})
    df_topik=df_topik.reset_index(drop=True)

    ##membuat data lemma, corpus dan dictionary berdasarkan data dalam 1 topik
    res_list = [data_lemmatized[int(i)-1] for i in df_topik.id_judul] 
    # Create Dictionary
    id2word_topik = corpora.Dictionary(res_list)

    # Create Corpus
    texts = res_list

    # Term Document Frequency
    corpus_topik = [id2word_topik.doc2bow(text) for text in res_list]

    #membuat indexing untuk perhitungan cossim
    index_tmpfile = get_tmpfile("index")
    index = Similarity(index_tmpfile,corpus_topik, num_features=len(id2word_topik))

    #query diambil dari term document berdasarkan corpus per topik dari data lemma hasil search
    query = id2word_topik.doc2bow(data_lemmatized_search[0])
    similarities = index[query]

    sort_index=np.argsort(similarities)
    sort_index

    reversed_arr = sort_index[::-1]
    reversed_arr

    list_idx=reversed_arr[:10]

    list_id_artikel=list(df_topik[df_topik.index.isin(list_idx)].id_judul)

    return(list_id_artikel,topic+1)