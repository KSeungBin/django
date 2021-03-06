from django.shortcuts import render
import pandas as pd
import numpy as np
# Create your views here.

df3=pd.read_json('https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json')

#def indexPage(request):
def index(request):
    confirmedGlobal=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',encoding='utf-8',na_values=None)
    totalCount=confirmedGlobal[confirmedGlobal.columns[-1]].sum()
    barPlotData=confirmedGlobal[['Country/Region',confirmedGlobal.columns[-1]]].groupby('Country/Region').sum()
    barPlotData=barPlotData.reset_index()
    barPlotData.columns=['Country/Region','values']
    barPlotData=barPlotData.sort_values(by='values', ascending=False)
    barplotVals=barPlotData['values'].values.tolist()
    countryNames=barPlotData['Country/Region'].values.tolist()
    dataForMap=mapDataCal(barPlotData, countryNames)
    showMap='True'
    context={'totalCount':totalCount, 'countryNames':countryNames, 'barplotVals':barplotVals, 'dataForMap':dataForMap, 'showMap':showMap}
    return render(request,'index.html',context)


def mapDataCal(barPlotData, countryNames):
    dataForMap=[]
    for i in countryNames:
        try:
            tempdf=df3[df3['name']==i]
            temp={}
            temp["code3"]=list(tempdf['code3'].values)[0]
            temp["name"]=i
            temp["value"]=barPlotData[barPlotData['Country/Region']==i]['values'].sum()
            temp["code"]=list(tempdf['code'].values)[0]
            dataForMap.append(temp)
        except:
            pass
    print (len(dataForMap))
    return dataForMap

def getHeatMapData(confirmedGlobal,contryNames):
    df3=confirmedGlobal[list(confirmedGlobal.columns[1:2])+list(list(confirmedGlobal.columns.values)[-6:-1])]
    dataForheatMap=[]
    for i in contryNames:
        try:
            tempdf=df3[df3['Country/Region']==i]
            temp={}
            temp["name"]=i
            temp["data"]=[{'x':j,'y':k} for j,k in zip(tempdf[tempdf.columns[1:]].sum().index,tempdf[tempdf.columns[1:]].sum().values)]
            dataForheatMap.append(temp)
        except:
            pass
    dateCat=list(list(confirmedGlobal.columns.values)[-6:-1])
    return dataForheatMap,dateCat


def getDataforMap(uniqueCOuntryName,df2):
    dataForMap=[]
    for i in uniqueCOuntryName:
        try:
            tempdf=df3[df3['name']==i]
            temp={}
            temp["code3"]=list(tempdf['code3'].values)[0]
            temp["name"]=i
            temp["value"]=df2[df2['Country/Region']==i]['values'].sum()
            temp["code"]=list(tempdf['code'].values)[0]
            dataForMap.append(temp)
        except:
            pass
    print (len(dataForMap))
    return dataForMap


def getBarData(confirmedGlobal,uniqueCountryNames):
    df2=confirmedGlobal[list(confirmedGlobal.columns[1:2])+list([confirmedGlobal.columns[-2]])]
    df2.columns=['Country/Region','values']
    df2=df2.sort_values(by='values',ascending=False)
    contryNames=list(df2['Country/Region'].values)
    countsVal=list(df2['values'].values)
    maxVal=max(countsVal)
    overallCount=sum(countsVal)
    logVals=list(np.log(ind) if ind != 0 else 0 for ind in countsVal )
    dataForMapGraph=getDataforMap(uniqueCountryNames,df2)
    # dictVal=[]
    # for i in range(df2.shape[0]):
    #     dictVal.append(dict(df2.ix[i]))
    return (contryNames,countsVal,logVals,overallCount,dataForMapGraph,maxVal)


def indiAirConditionData(request):
    countryNameSe=request.POST.get('countryName')
    confirmedGlobal=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',encoding='utf-8',na_values=None)
    totalCount=confirmedGlobal[confirmedGlobal.columns[-1]].sum()
    barPlotData=confirmedGlobal[['Country/Region',confirmedGlobal.columns[-1]]].groupby('Country/Region').sum()
    barPlotData=barPlotData.reset_index()
    barPlotData.columns=['Country/Region','values']
    barPlotData=barPlotData.sort_values(by='values', ascending=False)
    barplotVals=barPlotData['values'].values.tolist()
    countryNames=barPlotData['Country/Region'].values.tolist()
    showMap='False'
    countryDataSpe=pd.DataFrame(confirmedGlobal[confirmedGlobal['Country/Region']==countryNameSe][confirmedGlobal.columns[4:-1]].sum()).reset_index()
    countryDataSpe.columns=['country','values']
    countryDataSpe['lagVal']=countryDataSpe['values'].shift(1).fillna(0)
    countryDataSpe['incrementVal']=countryDataSpe['values']-countryDataSpe['lagVal']
    countryDataSpe['rollingMean']=countryDataSpe['incrementVal'].rolling(window=4).mean()
    countryDataSpe=countryDataSpe.fillna(0)
    datasetsForLine=[{'label':'Daily Cumulated Data','data':countryDataSpe['values'].values.tolist()},
                    {'label':'Rolling Mean 4 days','data':countryDataSpe['rollingMean'].values.tolist()}]
    axisvalues=countryDataSpe.index.tolist()
    context={'axisvalues':axisvalues, 'countryName':countryNameSe, 'totalCount':totalCount, 'countryNames':countryNames, 'barplotVals':barplotVals, 'showMap':showMap, 'datasetsForLine':datasetsForLine}
    return render(request,'index2.html',context)


    #print (request.POST.dict())
    #countryName=request.POST.get('countryName')
    #confirmedGlobal=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',encoding='utf-8',na_values=None)
    #countryDataSpe=pd.DataFrame(confirmedGlobal[confirmedGlobal['Country/Region']==countryName][confirmedGlobal.columns[4:-1]].sum()).reset_index()
    #countryDataSpe.columns=['country','values']
    #countryDataSpe['lagVal']=countryDataSpe['values'].shift(1).fillna(0)
    #countryDataSpe['incrementVal']=countryDataSpe['values']-countryDataSpe['lagVal']
    #countryDataSpe['rollingMean']=countryDataSpe['incrementVal'].rolling(window=4).mean()
    #countryDataSpe=countryDataSpe.fillna(0)
    #datasetsForLine=[{'yAxisID': 'y-axis-1','label':'Daily Cumulated Data','data':countryDataSpe['values'].values.tolist(),'borderColor':'#03a9fc','backgroundColor':'#03a9fc','fill':'false'},
    #                {'yAxisID': 'y-axis-2','label':'Rolling Mean 4 days','data':countryDataSpe['rollingMean'].values.tolist(),'borderColor':'#fc5203','backgroundColor':'#fc5203','fill':'false'}]
    #axisvalues=countryDataSpe.index.tolist()
    #uniqueCountryNames=pd.unique(confirmedGlobal['Country/Region'])
    #contryNames,countsVal,logVals,overallCount,dataForMapGraph,maxVal=getBarData(confirmedGlobal,uniqueCountryNames)
    #dataForheatMap,dateCat=getHeatMapData(confirmedGlobal,contryNames)
    #context=context={"countryName":countryName,'axisvalues':axisvalues,'datasetsForLine':datasetsForLine,'dateCat':dateCat,'dataForheatMap':dataForheatMap,'maxVal':maxVal,'dataForMapGraph':dataForMapGraph,'uniqueCountryNames':uniqueCountryNames,'contryNames':contryNames,'countsVal':countsVal,'logVals':logVals,'overallCount':overallCount}
    #
    #return render(request,'index2.html',context)

