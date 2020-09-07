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
    if request.method == 'GET':
        chk = request.GET.getlist('sort')
        if len(chk) > 0:
            if chk[0]=='sortaz':
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

            elif chk[0]=='sortpublications':
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
            
            elif chk[0]=='sortcitations':
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

            elif chk[0]=='sortauthors':
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

    elif request.method == 'POST':

        catch = request.POST['affiliation']

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
    chk = request.GET.getlist('id_topik')
    if len(chk) > 0:
        id_univ = kwargs['id_univ']
        univ = Affiliations.objects.get(id_univ=id_univ)
        nidn = Authors.objects.filter(univ=id_univ).values('nidn').distinct()
        topic = Topics.objects.all().order_by('topic_name')
        nidn_fix = []
        for i in nidn:
            nidn_fix.append(i['nidn'])
        paper = Papers.objects.filter(author__in=nidn_fix, topic=chk[0])[:25]
        # topik_affi = Papers.objects.filter(author__in=nidn_fix).value('topic').distinct()
        # topik = []
        # for i in topik_affi:
        #     topik.append(i['topic'])

        # topik_affiliation = Topics.objects.filter(id_topic__in=topik).order_by('-total_publication')[:6]

        # print(topik)

        # models.Shop.objects.order_by().values('city').distinct()
        page = request.GET.get('page', 1)
        paginator = Paginator(paper, 5)

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        df_countsum,list_count,list_sum=vis_affil(id_univ)
        ##data sum count, udah urut dari topik dominan sampai ke topik yang ga dominan, data yang ditampilkan data pertahun yang ada nilainya aja
        topik_sumcount=[univ.topik_dominan1_id,univ.topik_dominan2_id,univ.topik_dominan3_id]  
        data_sumcount=sortData_sumcount_univ(df_countsum,id_univ)
        data_sumcount=data_sumcount.to_dict('records')
        print(data_sumcount)
        return render(request, 'affiliation/detail_affiliation_filter.html', {'univs': univ, 'users': users,'data_count':list_count,
        'data_sum':list_sum, 'nama_topik': topic, 'chk':chk[0],'data_sumcount':data_sumcount})
    
    else:
        id_univ = kwargs['id_univ']
        univ = Affiliations.objects.get(id_univ=id_univ)
        nidn = Authors.objects.filter(univ=id_univ).values('nidn').distinct()
        topic = Topics.objects.all().order_by('topic_name')
        nidn_fix = []
        for i in nidn:
            nidn_fix.append(i['nidn'])
        paper = Papers.objects.filter(author__in=nidn_fix)[:25]
        # models.Shop.objects.order_by().values('city').distinct()
        page = request.GET.get('page', 1)
        paginator = Paginator(paper, 5)

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        df_countsum,list_count,list_sum=vis_affil(id_univ)
        topik_sumcount=[univ.topik_dominan1_id,univ.topik_dominan2_id,univ.topik_dominan3_id]  

        ##data sum count, udah urut dari topik dominan sampai ke topik yang ga dominan, data yang ditampilkan data pertahun yang ada nilainya aja
        data_sumcount=sortData_sumcount_univ(df_countsum,id_univ)
        data_sumcount=data_sumcount.to_dict('records')

        topik1_data = Data_sumcount_univ.objects.filter(univ=id_univ,topic=univ.topik_dominan1_id).order_by('-year')[:3]
        topik2_data = Data_sumcount_univ.objects.filter(univ=id_univ,topic=univ.topik_dominan2_id).order_by('-year')[:3]
        topik3_data = Data_sumcount_univ.objects.filter(univ=id_univ,topic=univ.topik_dominan3_id).order_by('-year')[:3]

        # print(data_sumcount)

        author_rekomen1 = Authors.objects.filter(univ=id_univ, topik_dominan1=univ.topik_dominan1_id).order_by('-nilai_dominan1')[:3]
        # print(author_rekomen1)
        author_rekomen2 = Authors.objects.filter(univ=id_univ, topik_dominan1=univ.topik_dominan2_id).order_by('-nilai_dominan1')[:3]
        author_rekomen3 = Authors.objects.filter(univ=id_univ, topik_dominan1=univ.topik_dominan3_id).order_by('-nilai_dominan1')[:3]

        return render(request, 'affiliation/detail_affiliation.html', {'univs': univ, 'users': users,'data_count':list_count,
        'data_sum':list_sum, 'nama_topik': topic,'data_sumcount':data_sumcount, 'author_rekomen1':author_rekomen1, 'author_rekomen2':author_rekomen2, 'author_rekomen3':author_rekomen3, 'topik1_data':topik1_data, 'topik2_data':topik2_data, 'topik3_data':topik3_data})
    

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