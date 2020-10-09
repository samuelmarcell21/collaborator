from django.shortcuts import render
from affiliation.models import Affiliations,Data_sumcount_univ
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from author.models import Authors, Papers
from topic.models import Topics
import pandas as pd
import numpy as np
from django.db.models import Sum

# Create your views here.
def index(request):
    # Untuk Request Get
    if request.method == 'GET':
        # Mengambil data sort dari Request User
        chk = request.GET.getlist('sort')
        # Jika ada request get dengan mempassing data maka akan masuk kesini
        if len(chk) > 0:
            # Sort A-Z
            if chk[0]=='sortaz':
                # Mengambil 11 univ saja dengan publikasi tertinggi
                univ_list = ['Institut Pertanian Bogor', 'Institut Teknologi Bandung', 'Institut Teknologi Sepuluh Nopember', 'Universitas Airlangga', 'Universitas Diponegoro', 'Unviersitas Gadjah Mada', 'Universitas Hasanuddin', 'Universitas Indonesia', 'Universitas Padjajaran', 'Universitas Pendidikan Indonesia', 'Universitas Sumatera Utara']
                result = Affiliations.objects.filter(name__in=univ_list).order_by('name')
                page = request.GET.get('page', 1)
                paginator = Paginator(result, 6)

                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    users = paginator.page(1)
                except EmptyPage:
                    users = paginator.page(paginator.num_pages)

                return render(request, 'affiliation/affiliation_filter.html', {'users':users, 'chk':chk[0]})
            # Sort Publications
            elif chk[0]=='sortpublications':
                # Mengambil 11 univ saja dengan publikasi tertinggi
                univ_list = ['Institut Pertanian Bogor', 'Institut Teknologi Bandung', 'Institut Teknologi Sepuluh Nopember', 'Universitas Airlangga', 'Universitas Diponegoro', 'Unviersitas Gadjah Mada', 'Universitas Hasanuddin', 'Universitas Indonesia', 'Universitas Padjajaran', 'Universitas Pendidikan Indonesia', 'Universitas Sumatera Utara']
                result = Affiliations.objects.filter(name__in=univ_list).order_by('-total_publication')
                page = request.GET.get('page', 1)
                paginator = Paginator(result, 6)

                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    users = paginator.page(1)
                except EmptyPage:
                    users = paginator.page(paginator.num_pages)

                return render(request, 'affiliation/affiliation_filter.html', {'users':users, 'chk':chk[0]})
            # Sort Citations
            elif chk[0]=='sortcitations':
                # Mengambil 11 univ saja dengan publikasi tertinggi
                univ_list = ['Institut Pertanian Bogor', 'Institut Teknologi Bandung', 'Institut Teknologi Sepuluh Nopember', 'Universitas Airlangga', 'Universitas Diponegoro', 'Unviersitas Gadjah Mada', 'Universitas Hasanuddin', 'Universitas Indonesia', 'Universitas Padjajaran', 'Universitas Pendidikan Indonesia', 'Universitas Sumatera Utara']
                result = Affiliations.objects.filter(name__in=univ_list).order_by('-total_cite')
                page = request.GET.get('page', 1)
                paginator = Paginator(result, 6)

                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    users = paginator.page(1)
                except EmptyPage:
                    users = paginator.page(paginator.num_pages)

                return render(request, 'affiliation/affiliation_filter.html', {'users':users, 'chk':chk[0]})

            # Sort Authors
            elif chk[0]=='sortauthors':
                # Mengambil 11 univ saja dengan publikasi tertinggi
                univ_list = ['Institut Pertanian Bogor', 'Institut Teknologi Bandung', 'Institut Teknologi Sepuluh Nopember', 'Universitas Airlangga', 'Universitas Diponegoro', 'Unviersitas Gadjah Mada', 'Universitas Hasanuddin', 'Universitas Indonesia', 'Universitas Padjajaran', 'Universitas Pendidikan Indonesia', 'Universitas Sumatera Utara']
                result = Affiliations.objects.filter(name__in=univ_list).order_by('-total_author')
                page = request.GET.get('page', 1)
                paginator = Paginator(result, 6)

                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    users = paginator.page(1)
                except EmptyPage:
                    users = paginator.page(paginator.num_pages)

                return render(request, 'affiliation/affiliation_filter.html', {'users':users, 'chk':chk[0]})

        else:
            # Mengambil 11 univ saja dengan publikasi tertinggi
            univ_list = ['Institut Pertanian Bogor', 'Institut Teknologi Bandung', 'Institut Teknologi Sepuluh Nopember', 'Universitas Airlangga', 'Universitas Diponegoro', 'Unviersitas Gadjah Mada', 'Universitas Hasanuddin', 'Universitas Indonesia', 'Universitas Padjajaran', 'Universitas Pendidikan Indonesia', 'Universitas Sumatera Utara']
            result = Affiliations.objects.filter(name__in=univ_list).order_by('-total_publication')
            page = request.GET.get('page', 1)
            paginator = Paginator(result, 6)

            try:
                users = paginator.page(page)
            except PageNotAnInteger:
                users = paginator.page(1)
            except EmptyPage:
                users = paginator.page(paginator.num_pages)
            print(result)

            return render(request, 'affiliation/affiliation.html', {'users':users})

    # Ini untuk fitur search
    elif request.method == 'POST':
        # Mengambil data yang dipassing dalam metode POST
        catch = request.POST['affiliation']
        # Mengambil 11 univ saja dengan publikasi tertinggi
        univ_list = ['Institut Pertanian Bogor', 'Institut Teknologi Bandung', 'Institut Teknologi Sepuluh Nopember', 'Universitas Airlangga', 'Universitas Diponegoro', 'Unviersitas Gadjah Mada', 'Universitas Hasanuddin', 'Universitas Indonesia', 'Universitas Padjajaran', 'Universitas Pendidikan Indonesia', 'Universitas Sumatera Utara']
        result = Affiliations.objects.filter(name__in=univ_list).filter(name__icontains=catch)
        page = request.GET.get('page', 1)
        paginator = Paginator(result, 6)

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        print(result)

        return render(request, 'affiliation/affiliation.html', {'users':users})

def show_detailaffiliation(request, *args, **kwargs):
    # Mengambil id topik yang dipassing dari halaman afiliasi
    chk = request.GET.getlist('id_topik')
    if len(chk) > 0:
        id_univ = kwargs['id_univ']
        # Mengambil data univ dengan topik tersebut
        univ = Affiliations.objects.get(id_univ=id_univ)
        # Mengambil data author yang bekerja pada afiliasi terkait
        nidn = Authors.objects.filter(univ=id_univ).values('nidn').distinct()
        # Mengambil seluruh data topik agar dapat digunakan untuk filter
        topic = Topics.objects.all().order_by('topic_name')
        # Memasukkan hasil nidn ke array baru
        nidn_fix = []
        for i in nidn:
            nidn_fix.append(i['nidn'])
        # Mengambil data paper dari nidn yang didapatkan dan dibataskan hanya 25 paper
        paper = Papers.objects.filter(author__in=nidn_fix, topic=chk[0])[:25]
        page = request.GET.get('page', 1)
        paginator = Paginator(paper, 5)

        # Pagination
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        df_countsum,list_count,list_sum=vis_affil(id_univ)

        return render(request, 'affiliation/detail_affiliation_filter.html', {'univs': univ, 'users': users,'data_count':list_count,
        'data_sum':list_sum, 'nama_topik': topic, 'chk':chk[0]})
    
    else:
        id_univ = kwargs['id_univ']
        # Mengambil data univ dengan topik tersebut
        univ = Affiliations.objects.get(id_univ=id_univ)
        # Mengambil data author yang bekerja pada afiliasi terkait
        nidn = Authors.objects.filter(univ=id_univ).values('nidn').distinct()
        # Mengambil seluruh data topik agar dapat digunakan untuk filter
        topic = Topics.objects.all().order_by('topic_name')
        # Memasukkan hasil nidn ke array baru
        nidn_fix = []
        for i in nidn:
            nidn_fix.append(i['nidn'])
        # Mengambil data paper dari nidn yang didapatkan dan dibataskan hanya 25 paper
        paper = Papers.objects.filter(author__in=nidn_fix)[:25]
        page = request.GET.get('page', 1)
        paginator = Paginator(paper, 5)

        # Pagination
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        df_countsum,list_count,list_sum=vis_affil(id_univ)

        # Mengambil data topik dari 3 topik dominan afiliasi
        topik1_data = getData_sumcount_univ(id_univ,univ.topik_dominan1_id)
        topik2_data = getData_sumcount_univ(id_univ,univ.topik_dominan2_id)
        topik3_data = getData_sumcount_univ(id_univ,univ.topik_dominan3_id)

        # Mengambil data rekomendasi author dari 3 topik dominan afiliasi
        author_rekomen1 = Authors.objects.filter(univ=id_univ, topik_dominan1=univ.topik_dominan1_id).order_by('-nilai_dominan1')[:2]
        author_rekomen2 = Authors.objects.filter(univ=id_univ, topik_dominan1=univ.topik_dominan2_id).order_by('-nilai_dominan1')[:2]
        author_rekomen3 = Authors.objects.filter(univ=id_univ, topik_dominan1=univ.topik_dominan3_id).order_by('-nilai_dominan1')[:2]

        return render(request, 'affiliation/detail_affiliation.html', {'univs': univ, 'users': users,'data_count':list_count,
        'data_sum':list_sum, 'nama_topik': topic, 'author_rekomen1':author_rekomen1, 'author_rekomen2':author_rekomen2, 'author_rekomen3':author_rekomen3, 'topik1_data':topik1_data, 'topik2_data':topik2_data, 'topik3_data':topik3_data})
    

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

def vis_affil(id_univ):
    data=Data_sumcount_univ.objects.filter(univ_id=id_univ).order_by('-topic_id')
    univ= Affiliations.objects.get(id_univ=id_univ)
    YEAR=['2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']
    TOPIK=[univ.topik_dominan1_id,univ.topik_dominan2_id,univ.topik_dominan3_id]
    TOPIK_NAMA=[univ.topik_dominan1.topic_name,univ.topik_dominan2.topic_name,univ.topik_dominan3.topic_name]
    df=pd.DataFrame(columns=['Topic','Year','Count','Sumcite'])
    YEAR=['2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']
    for top in data.values('topic_id').distinct():
        dataPerTopik=Data_sumcount_univ.objects.filter(univ_id=id_univ,topic_id=top['topic_id'])
        df_temp=pd.DataFrame(columns=['Topik','Year','Count','Sumcite'])
        count=[0]*11
        sumcite=[0]*11
        topic=[top['topic_id']]*11
        for dat in dataPerTopik:
            yea=int(dat.year)-2010
            count[yea]=int(dat.pubcount)
            sumcite[yea]=int(dat.sumcite)
            # print(dat)
        df_temp['Topik']=topic
        df_temp['Year']=YEAR
        df_temp['Count']=count
        df_temp['Sumcite']=sumcite
        # print(df_temp)
        df=pd.concat([df,df_temp])
    df=df.reset_index(drop=True)
    list_count=[]
    list_sum=[]
    df = df.astype({"Topik": int})
    df['Color']=df.apply(color,axis=1)
    flag=0
    # print(df.Topik.unique())
    for top in TOPIK:
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
    return(df,list_count,list_sum)

def sortData_sumcount_univ(df_countsum,id_univ):
    univ = Affiliations.objects.get(id_univ=id_univ)
    TOPIK=[univ.topik_dominan1_id,univ.topik_dominan2_id,univ.topik_dominan3_id]
    count_topik = df_countsum[['Topik', 'Count']].groupby(['Topik']).agg('sum')
    count_topik=count_topik.sort_values(by=['Count'],ascending=False)
    count_topik=count_topik.reset_index(level=['Topik'])
    count_topik['Urutan']=count_topik.index+1
    urutan_dict=count_topik[['Topik','Urutan']].to_dict('records')
    def urutan(row):
        for dat in urutan_dict:
            if(row['Topik']==dat['Topik']):
                val=dat['Urutan']
                break
        return val
    df_countsum['Urutan']=df_countsum.apply(urutan,axis=1)
    df_countsum=df_countsum.sort_values(by=['Urutan','Year'],ascending=[True,False])
    return(df_countsum)

def getData_sumcount_univ(id_univ,top):
    datasumcount=Data_sumcount_univ.objects.filter(univ=id_univ,topic=top).order_by('-year')
    # temp=datasumcount.values_list()
    df = pd.DataFrame.from_records(datasumcount.values_list(),columns=['id','idTopic','id_univ','Year','Count','Sumcite','id_pub'])
    id_univ = df['id_univ']
    Year=df['Year']
    Count=df['Count']
    Sumcite=df['Sumcite']
    id_pub=df['id_pub']
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
    new_df = pd.DataFrame({'year':Year, 'pubcount':Count, 'sumcite':Sumcite,'citestat':citestat,'pubstat':pubstat,'id_pub':id_pub,'pubcolor':pubcolor,'citecolor':citecolor})
    data=new_df.to_dict('records')
    # bisa di batasin jumlah row yang mau d passing di sini
    print(data[:3])
    return(data[:3])