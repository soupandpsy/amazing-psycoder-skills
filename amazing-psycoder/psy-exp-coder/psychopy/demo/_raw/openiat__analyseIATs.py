# Source: openiat (demos/openiat)
# Project URL: https://gitlab.pavlovia.org/demos/openiat
# Original file: analysis/analyseIATs.py
## -----------IMPORT LIBRARIES
import pandas as pd #for dealing with csv import
import matplotlib.pyplot as plt  # Matplotlib's pyplot: MATLAB-like syntax
from scipy import stats

##check data summary files are up to date

reprocess=1 #a toggle, check for more data or not

if reprocess:
    execfile("calcIATs.py")
    
# GET THE DATA
iat_race=pd.read_csv('IATscores.csv')

dat={} #store for summary stats. We use a dict because can be dynamically allocated
basis=np.zeros(2) # IAT race, RAW race,order variable

# COLLATE THE DATA

#iterate through all IAT race data
for i in range(0,len(iat_race)):
           
           #get filename
           name=iat_race['file'].values[i]
           #from the filename we extract the ppt number
           end=name.find('_')
           ppt_number=int(name[:end])
           
           #creat a dict entry for that ppt
           ppt_dat=basis.copy()
           ppt_dat[0]=iat_race['IAT score'].values[i]
           ppt_dat[1]=iat_race['raw uncorrected'].values[i]
           
           dat[ppt_number]=ppt_dat
           

#now we can extract paired IAT scores
            
IATrace=[]  
RAWrace=[]
            
for key in dat:
    IATrace.append(dat[key][0])              
    RAWrace.append(dat[key][1])              


      
         
plt.clf()
plt.plot(RAWrace,IATrace,'.',markersize=20,color='g')
plt.xlim([-0.5,0.5])
plt.ylim([-2,2])
plt.xlabel('Race RAW scores')
plt.ylabel('Race IAT scores')
plt.title('RAW race mean {:+.3f}'.format(np.mean(RAWrace)) + '; IAT race mean {:+.3f}'.format(np.mean(IATrace)))
plt.savefig('IATscatterplot1.png', dpi=300, facecolor='w', edgecolor='w',
            orientation='portrait', papertype=None, format=None,
            transparent=False, bbox_inches=None, pad_inches=0.1)
         
print 'RACE t-statistic = %6.3f pvalue = %6.4f' %  stats.ttest_1samp(IATrace, 0)



