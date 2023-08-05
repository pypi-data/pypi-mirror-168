#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from fpdf import FPDF

class Insights:
    def __init__(self):
        self.data=pd.DataFrame()
        self.dat=pd.DataFrame()
        self.datin=pd.DataFrame()
        self.datout=pd.DataFrame()
    def open_file(self):
        file_name=input("Enter file name: ")
        file_path=input("Enter file path: ")
        file= file_path+file_name
        self.data= pd.read_excel(file)
    def cleaning(self):
        self.dat= self.data[['TRIPIDEN','TRUCKNUM','PLANT_NAME','NETWEIGH','CLUSTER_ZONE','YARDINTM','DICREATM','YARDOUTM','YARDTIME','GATEINTM','WGTFSTTM','LOADINTM','LOADOUTM','WGTSECTM','GATEOUTM','PLNTTIME','MOVETYPE','PRODUCT_TYPE']]
        #Dividing the dataset as Inbound or Outbound
        self.datin= self.dat[self.dat['MOVETYPE']=='Inbound']
        self.datout= self.dat[self.dat['MOVETYPE']=='Outbound']
        #Cleaning data: Removing dulicates and null values
        self.datin= self.datin.dropna(axis=1,how='all')
        self.datin= self.datin.dropna(axis=0)
        self.datin.drop_duplicates(subset ="TRIPIDEN",
                             keep = False, inplace = True)
        self.datout = self.datout.dropna()
        self.datout.drop_duplicates(subset ="TRIPIDEN",
                             keep = False, inplace = True)
    def inpreprocess(self):
        #Adding relevant columns to datin
        #Column which contains the time between Plant In time to Gross Weight  
        self.datin['DIFFGINWIN']= (self.datin['WGTFSTTM']-self.datin['GATEINTM'])
        #Column which contains the time between Gross Weight to Tare Weight 
        self.datin['DIFFTWGW']= self.datin['WGTSECTM']-self.datin['WGTFSTTM']
        #Column which contains the time between Tare Weight to Exit Gate
        self.datin['DIFFGOUTTW']= self.datin['GATEOUTM']-self.datin['WGTSECTM']

        self.datin['DIFFYARDTMCK'] = np.where(self.datin['YARDTIME']>self.datin.describe()['YARDTIME']['mean'], 1, 0)
        self.datin['DIFFGINWINCK'] = np.where(self.datin['DIFFGINWIN']>self.datin.describe()['DIFFGINWIN']['mean'], 1, 0)
        self.datin['DIFFTWGWCK'] = np.where(self.datin['DIFFTWGW']>self.datin.describe()['DIFFTWGW']['mean'], 1, 0)
        self.datin['DIFFGOUTTWCK'] = np.where(self.datin['DIFFGOUTTW']>self.datin.describe()['DIFFGOUTTW']['mean'], 1, 0)

        ca = self.datin['DIFFYARDTMCK']==1
        c1 = self.datin['DIFFGINWINCK']==1
        c2 = self.datin['DIFFTWGWCK']==1
        c3 = self.datin['DIFFGOUTTWCK']==1
        c4 = (self.datin['DIFFGINWINCK']==0) & (self.datin['DIFFTWGWCK']==0) & (self.datin['DIFFGOUTTWCK']==0)
        choices= ["The time taken for the truck in Yard is more than average so there might be congestion in the yard or the capacity for the product might be full in the plant inventory","The time taken for the truck to go from in gate to gross weight is more than average, as there might be traffic in the plant or some problems with the truck/truck driver."," The time taken for the truck to go from gross weight to tare weight is more than average, as there might be wrong amount of incoming raw material or problems with the weighing equipment(or technical issues)","The time taken for the truck to go from tare weight to gate-out is more than average, as there might be problems with packaging of the materials or problems with truck", "The truck is on time according to the average data." ]

        s = pd.concat((ca,c1,c2,c3,c4),keys=choices).swaplevel()
        self.datin = (self.datin.assign(Reason= pd.DataFrame.from_records(s[s].index).groupby(0)[1].agg(" ".join)))
        
    def outpreprocess(self):
        #Adding relevant columns to datin 
        #Column which contains the time between Yard In to DI Creation
        self.datout['DIFFYINDICTM']=self.datout['DICREATM']-self.datout['YARDINTM']
        #Column which contains the time between DI Creation to Yard Out
        self.datout['DIFFDICTMYOUT']=self.datout['YARDOUTM']-self.datout['DICREATM']
        #Column which contains the time between Plant In to Tare Weight  
        self.datout['DIFFGINWIN']= (self.datout['WGTFSTTM']-self.datout['GATEINTM'])
        #Column which contains the time between Tare Weight to Loading In  
        self.datout['DIFFTWLIN']= self.datout['LOADINTM']-self.datout['WGTFSTTM']
        #Column which contains the time between Loading In to Loading Out
        self.datout['DIFFLINLOUT']= self.datout['LOADOUTM']-self.datout['LOADINTM']
        #Column which contains the time between Loading Out to Gross Weight
        self.datout['DIFFLOUTGW']= self.datout['WGTSECTM']-self.datout['LOADOUTM']
        #Column which contains the time between Gross Weight to Exit Gate
        self.datout['DIFFGOUTTW']= self.datout['GATEOUTM']-self.datout['WGTSECTM']
        #creating checks for if the values of the differences 
        self.datout['DIFFYINDICTMCK']= np.where(self.datout['DIFFYINDICTM']>self.datout.describe()['DIFFYINDICTM']['mean'],1,0)
        self.datout['DIFFDICTMYOUTCK']=np.where(self.datout['DIFFDICTMYOUT']>self.datout.describe()['DIFFDICTMYOUT']['mean'],1,0)
        self.datout['DIFFGINWINCK']= np.where(self.datout['DIFFGINWIN']>self.datout.describe()['DIFFGINWIN']['mean'],1,0)
        self.datout['DIFFTWLINCK']= np.where( self.datout['DIFFTWLIN']>self.datout.describe()['DIFFTWLIN']['mean'],1,0)
        self.datout['DIFFLINLOUTCK']= np.where( self.datout['DIFFLINLOUT']>self.datout.describe()['DIFFLINLOUT']['mean'],1,0)
        self.datout['DIFFLOUTGWCK']= np.where( self.datout['DIFFLOUTGW']>self.datout.describe()['DIFFLOUTGW']['mean'],1,0)
        self.datout['DIFFGOUTTWCK']= np.where(self.datout['DIFFGOUTTW']>self.datout.describe()['DIFFGOUTTW']['mean'],1,0)

        ca = self.datout['DIFFYINDICTMCK']==1
        cb = self.datout['DIFFDICTMYOUTCK']==1
        c1 = self.datout['DIFFGINWINCK']==1
        c2 = self.datout['DIFFTWLINCK']==1
        c3 = self.datout['DIFFLINLOUTCK']==1
        c4 = self.datout['DIFFLOUTGWCK']==1
        c5 = self.datout['DIFFGOUTTWCK']==1

        #c6 = !(c1 & c2 & c3 & c4 & c5)

        c6 = (self.datout['DIFFGINWINCK']==0) & (self.datout['DIFFTWLINCK']==0) & (self.datout['DIFFLINLOUTCK']==0) & (self.datout['DIFFLOUTGWCK']==0) & (self.datout['DIFFGOUTTWCK']==0)
        choices= ["The time taken for the truck to go from Yard In gate until the time of creation of the delivery instruciton is more than average because of problems from transporter's end or there might be congestion in the yard.",'The time from the delivery instruction creation(DI) to the truck to get out the yard is more than average, which means there might be issues with the truck or the driver might be lethargic',"The time taken for the truck to go from gate-in to tare weight is more than average because there might be traffic in the plant or problems with truck or truck driver"," Time taken for the truck to go from tare weight and loading in time is more than average as, there might be traffic in the plant.","Time taken for the truck to go from load-in time to load-out time is more than average because of packaging problems.","The time taken for the truck to go from loading out time to gross weight time is more than average as, there might be congestion in the plant or equipment related problems ","The time taken for gross weight to gate-out time is more than average as there might be issues with the quantity loading or the wrong amount of material would have been loaded/unloaded ","The truck is on time." ]

        s = pd.concat((ca,cb,c1,c2,c3,c4,c5,c6),keys=choices).swaplevel()
        self.datout = (self.datout.assign(Reason= pd.DataFrame.from_records(s[s].index).groupby(0)[1].agg(" ".join)))
        
    def top3plantsI(self):
        a=''
        self.datin['HASISSUES']=np.where(self.datin['Reason']=="The truck is on time according to the average data.",0,1)
        a="The top 3 plants which have the most issues for Inbound trucks are:"
        for i in range(3):
            a+="\n"+str(i+1)+". "+str(self.datin.groupby(['PLANT_NAME']).sum()['HASISSUES'].index.tolist()[i])+":\n"
            d=self.datin[self.datin['PLANT_NAME']==self.datin.groupby(['PLANT_NAME']).sum()['HASISSUES'].index.tolist()[i]]
            a+="\tTotal number of vehicles: "+str(len(d['TRUCKNUM']))
            a+="\n\tNo. of vehicles with issues: "+str(d.sum()['HASISSUES'])+" / "+str(round((d.sum()['HASISSUES']/len(d['TRUCKNUM']))*100,2))+" %\n"
        return a
    
    def InsightsI(self,df,plantname='NULL',zonename='NULL',flag=1):
        if(plantname=='NULL' and zonename=='NULL'):
            finali=[]
            rfinali=[]
            title=[]
            counts = [df['DIFFYARDTMCK'].value_counts()[1],df['DIFFGINWINCK'].value_counts()[1],df['DIFFTWGWCK'].value_counts()[1],df['DIFFGOUTTWCK'].value_counts()[1]]
            per=[]
            for count in counts:
                per.append(round((count/len(df['TRUCKNUM'])*100),2))
            sentences=[" trucks were late from yard-in to yard-out because of congestion problems or truck related problems.\n"," trucks, had time taken to go from gate-in to gross weight more than average, as there might be some problems with the truck or truck driver.\n"," trucks, had time taken to go from gross weight to tare-weight more than average as there might be problems with the weighing equipment (or other technical issues).\n"," trucks had the time taken to go from tare-weight to gate-out more than average, as there might be problems with weighing equipment or the amount asked could be less than desired.\n"]
            title.append("Insights for Inbound (Total No. of vehicles: "+str(len(df['TRUCKNUM']))+") \n")
            for i in range(len(counts)):
                if(counts[i]==max(counts)):
                    rfinali.append("\n-> "+str(counts[i])+" / "+str(per[i])+" % of"+sentences[i])
                else:
                    finali.append("\n-> "+str(counts[i])+" / "+str(per[i])+" % of "+sentences[i])
            finali.append("\n-> Number of trucks that are on time according to the average data were "+str(df['Reason'].value_counts()['The truck is on time according to the average data.'])+" / "+str(round((df['Reason'].value_counts()["The truck is on time according to the average data."]/len(df['TRUCKNUM'])*100),2))+"%. "+df.groupby(['PRODUCT_TYPE']).sum()['NETWEIGH'].index.tolist()[0]+" was the most ordered by quantity.")
            if(flag==1):
                finali.append("\n"+self.top3plantsI())
            return title,finali,rfinali
        elif(zonename!="NULL"):
            df=df[df['CLUSTER_ZONE']==zonename]
            return self.InsightsI(df,zonename='NULL',flag=0)
        else:
            df=df[df['PLANT_NAME']==plantname]
            return self.InsightsI(df,plantname="NULL",flag=0)
    def top3plantsO(self):
        a=''
        self.datout['HASISSUES']=np.where(self.datout['Reason']=="The truck is on time.",0,1)
        a+="The top 3 plants which have the most issues for Outbound trucks are: \n"
        for i in range(3):
            a+="\n"+str(i+1)+". "+str(self.datout.groupby(['PLANT_NAME']).sum()['HASISSUES'].index.tolist()[i])+': \n'
            d=self.datout[self.datout['PLANT_NAME']==self.datout.groupby(['PLANT_NAME']).sum()['HASISSUES'].index.tolist()[i]]
            a+="\n\tTotal number of vehicles: "+str(len(d['TRUCKNUM']))
            a+="\n\tNo. of vehicles with issues: "+str(d.sum()['HASISSUES'])+" / "+str(round((d.sum()['HASISSUES']/len(d['TRUCKNUM']))*100,2))+" %\n"
        return a
    
    def InsightsO(self,df,plantname='NULL',zonename='NULL',flag=1):
        if(plantname=='NULL' and zonename=='NULL'):
            finali=[]
            rfinali=[]
            title=[]
            counts = [df['DIFFYINDICTMCK'].value_counts()[1], df['DIFFDICTMYOUTCK'].value_counts()[1],df['DIFFGINWINCK'].value_counts()[1], df['DIFFTWLINCK'].value_counts()[1], df['DIFFLINLOUTCK'].value_counts()[1], df['DIFFLOUTGWCK'].value_counts()[1], df['DIFFGOUTTWCK'].value_counts()[1]]
            per=[]
            for count in counts:
                per.append(round((count/len(df['TRUCKNUM'])*100),2))
            sentences=[" trucks were late from yard-in gate until the time of creation of delivery instruction(DI-creation time) was more than average as there might have beeen problems from the transporter's end or their might be congestion in the yard.\n"," trucks took more than average time from Delivery Instruction creation (DI) to the truck to get out of the yard as there might have been issues with the truck or the driver might have been lethargic.\n"," trucks, had the time taken for gate-in to tare-weight more than average as there might have been issues with the truck or truck driver.\n"," trucks, took longer than usual time to get from tare weight to loading-in as there could have been packaging-related issues.\n"," trucks, had the time between load-in and load-out longer than usual, suggesting that there might have been packaging or manpower related issues.\n"," trucks, had the time taken to go form Loading-out to gross-weight, more than average because there might have been issues with the vehicle or the weighing equipment.\n"," trucks, had the time taken for gross weight to gate-out more than average as there might have been a problem with quantity loading or truck related issues. \n"]
            title.append("Insights for Outbound (Total No. of Vehicles: "+str(len(df['TRUCKNUM']))+")")       
            for i in range(len(counts)):
                if(counts[i]==max(counts)):
                    rfinali.append("\n"+"-> "+str(counts[i])+" / "+str(per[i])+" % of "+sentences[i])
                else:
                    finali.append("\n-> "+str(counts[i])+" / "+str(per[i])+" % of "+sentences[i])
            finali.append("\n-> Based on the average data, "+str(df['Reason'].value_counts()["The truck is on time."])+" trucks were on time which is only " +str(round((df['Reason'].value_counts()["The truck is on time."]/len(df['TRUCKNUM'])*100),2)) +" % and "+str(df.groupby(['PRODUCT_TYPE']).sum()['NETWEIGH'].index.tolist()[0])+" was ordered the most by quantity.")
            if(flag==1):
                finali.append("\n\n"+self.top3plantsO())
            return title,finali,rfinali
        elif(zonename!='NULL'):
            df=df[df['CLUSTER_ZONE']==zonename]
            return self.InsightsO(df,zonename='NULL',flag=0)

        else:
            df=df[df['PLANT_NAME']==plantname]
            return self.InsightsO(df,plantname="NULL",flag=0)
    def AIReportsI(self):
        title,para,con_para=self.InsightsI(self.datin)
        pdf= FPDF()
        pdf.set_auto_page_break(auto= True)
        pdf.add_page()
        pdf.set_font("Times",style='BU', size=18)
        pdf.cell(200, 5, txt = "All India Report - Inbound", align = 'C',ln=1)
        pdf.set_font("Times",style='U', size=14)
        pdf.cell(200, 10, txt = title[0], align = 'C',ln=2)
        pdf.set_font('Times', size=12)
        pdf.set_text_color(r=255,g=0,b=0)
        pdf.multi_cell(200, 5, txt = con_para[0], align = 'L')
        pdf.set_text_color(r=0,g=0,b=0)
        for sent in para:
            pdf.set_font('Times', size=12)
            pdf.multi_cell(200, 5, txt = sent, align = 'L')
        pdf.output("All India Report (Inbound).pdf")
        
    def AIReportsO(self):
        title,para,con_para= self.InsightsO(self.datout)
        pdf= FPDF()
        pdf.set_auto_page_break(auto= True)
        pdf.add_page()
        pdf.set_font("Times",style='BU', size=18)
        pdf.cell(200, 5, txt = "All India Report - Outbound", align = 'C',ln=1)
        pdf.set_font("Times",style='U', size=14)
        pdf.cell(200, 10, txt = title[0], align = 'C',ln=2)
        pdf.set_font('Times', size=12)
        pdf.set_text_color(r=255,g=0,b=0)
        pdf.multi_cell(200, 5, txt = con_para[0], align = 'L')
        pdf.set_text_color(r=0,g=0,b=0)
        for sent in para:
            pdf.set_font('Times', size=12)
            pdf.multi_cell(200, 5, txt = sent, align = 'L')
        pdf.output("All India Report (Outbound).pdf")
    
    def PReportI(self):
        a=self.datin['PLANT_NAME'].unique()
        pdf= FPDF()
        pdf.set_auto_page_break(auto= True)
        pdf.add_page()
        pdf.set_font("Times",style='BU', size=18)
        pdf.cell(200, 10, txt = "Plant-wise Report - Inbound", align = 'C',ln=1)
        for plant in a:
            title,para,con_para=self.InsightsI(self.datin,plantname=plant)
            pdf.set_font("Times",style='U', size=16)
            pdf.multi_cell(200,10,txt=plant,align='C')
            pdf.set_font("Times",style='U', size=14)
            pdf.multi_cell(200, 10, txt = title[0], align = 'C')
            pdf.set_font('Times', size=12)
            pdf.set_text_color(r=255,g=0,b=0)
            pdf.multi_cell(200, 5, txt = con_para[0], align = 'L')
            pdf.set_text_color(r=0,g=0,b=0)
            for sent in para:
                pdf.set_font('Times', size=12)
                pdf.multi_cell(200, 5, txt = sent, align = 'L')
        pdf.output("Plant-wise Report (Inbound).pdf")
    
    def PReportO(self):
        a=self.datout['PLANT_NAME'].unique()
        pdf= FPDF()
        pdf.set_auto_page_break(auto= True)
        pdf.add_page()
        pdf.set_font("Times",style='BU', size=18)
        pdf.cell(200, 10, txt = "Plant-wise Report - Outbound", align = 'C',ln=1)
        for plant in a:
            title,para,con_para=self.InsightsO(self.datout,plantname=plant)
            pdf.set_font("Times",style='U', size=16)
            pdf.multi_cell(200,10,txt=plant,align='C')
            pdf.set_font("Times",style='U', size=14)
            pdf.multi_cell(200, 10, txt = title[0], align = 'C')
            pdf.set_font('Times', size=12)
            pdf.set_text_color(r=255,g=0,b=0)
            pdf.multi_cell(200, 5, txt = con_para[0], align = 'L')
            pdf.set_text_color(r=0,g=0,b=0)
            for sent in para:
                pdf.set_font('Times', size=12)
                pdf.multi_cell(200, 5, txt = sent, align = 'L')
        pdf.output("Plant-wise Report (Outbound).pdf")
        
    def ZReportI(self):
        a=self.datin['CLUSTER_ZONE'].unique()
        pdf= FPDF()
        pdf.set_auto_page_break(auto= True)
        pdf.add_page()
        pdf.set_font("Times",style='BU', size=18)
        pdf.cell(200, 10, txt = "Zone-wise Report - Inbound", align = 'C',ln=1)
        for zone in a:
            title,para,con_para=self.InsightsI(self.datin,zonename=zone)
            pdf.set_font("Times",style='U', size=16)
            pdf.multi_cell(200,10,txt=zone,align='C')
            pdf.set_font("Times",style='U', size=14)
            pdf.multi_cell(200, 10, txt = title[0], align = 'C')
            pdf.set_font('Times', size=12)
            pdf.set_text_color(r=255,g=0,b=0)
            pdf.multi_cell(200, 5, txt = con_para[0], align = 'L')
            pdf.set_text_color(r=0,g=0,b=0)
            for sent in para:
                pdf.set_font('Times', size=12)
                pdf.multi_cell(200, 5, txt = sent, align = 'L')
        pdf.output("Zone-wise Report (Inbound).pdf")
        
    def ZReportO(self):
        a=self.datout['CLUSTER_ZONE'].unique()
        pdf= FPDF()
        pdf.set_auto_page_break(auto= True)
        pdf.add_page()
        pdf.set_font("Times",style='BU', size=18)
        pdf.cell(200, 10, txt = "Zone-wise Report - Outbound", align = 'C',ln=1)
        for zone in a:
            title,para,con_para=self.InsightsO(self.datout,zonename=zone)
            pdf.set_font("Times",style='U', size=16)
            pdf.multi_cell(200,10,txt=zone,align='C')
            pdf.set_font("Times",style='U', size=14)
            pdf.multi_cell(200, 10, txt = title[0], align = 'C')
            pdf.set_font('Times', size=12)
            pdf.set_text_color(r=255,g=0,b=0)
            pdf.multi_cell(200, 5, txt = con_para[0], align = 'L')
            pdf.set_text_color(r=0,g=0,b=0)
            for sent in para:
                pdf.set_font('Times', size=12)
                pdf.multi_cell(200, 5, txt = sent, align = 'L')
        pdf.output("Zone-wise Report (Outbound).pdf")

