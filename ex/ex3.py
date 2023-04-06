import netCDF4 as nc
import numpy as np
import pandas as pd
import xlsxwriter
import xlrd
import os
import matplotlib.pyplot as plt
import pyKriging
from pykrige.ok import OrdinaryKriging
#os.path.exists('D:\\wxd\\ex\\GL_PR_PF_1900184.nc')
#path ='D:\\wxd\\afc\\GL_PR_PF_1900184.nc'

path='D:/wxd/afc/13/'
files=os.listdir(path)
#print(files)
i=0 #文件数量
r=0 #剖面数量
p= {}
a= []
lat_list=[]
lon_list=[]

workbook=xlsxwriter.Workbook('data1.xlsx')
worksheet=workbook.add_worksheet('sheet1')

for file in files:
    k=0 #一个文件中的剖面数量
    f=nc.Dataset(path+file,'r')
    vkeys=f.variables
    #print(i)
    if ('TEMP' not in vkeys.keys()) or ('PRES' not in vkeys.keys()) or ('LONGITUDE' not in vkeys.keys()) or ('LATITUDE' not in vkeys.keys()):
        continue
    lat = (f.variables['LATITUDE'][:])
    lon = (f.variables['LONGITUDE'][:])
    temp = (f.variables['TEMP'][:])
    pres = (f.variables['PRES'][:])

    lat_data=lat.flatten()
    lon_data=lon.flatten()
    temp_data = temp.flatten()
    pres_data = pres.flatten()

    n=len(lon_data)
    if n>1:
        for j in range(n):
            temp_list=[]
            pres_list=[]
            for b in range(int((len(pres_data)/n)*j),int((len(pres_data)/n)*(j+1))):
                temp_list.append(temp_data[b])
                pres_list.append(pres_data[b])
            #print(temp_list)
            temp_list2=np.array(temp_list)
            pres_list2 = np.array(pres_list)
            #print(temp_list2)
            temp_list3=np.nan_to_num(temp_list2)
            pres_list3=np.nan_to_num(pres_list2)
            #print(temp_list3)
            #print(pres_list3)
            #print(len(temp_list3))
            temp_list4=[]
            pres_list4=[]
            x=0
            for c in range(len(temp_list3)-1,-1,-1):
                if temp_list3[c]==0:
                    x=x+1
                if temp_list3[c]!=0:
                    break
            #print(x)
            if x!=0:
                de = range(len(temp_list3) - x , len(temp_list3))
                temp_list4 = np.delete(temp_list3, de)
                pres_list4=np.delete(pres_list3,de)
            #print(temp_list4)
            #print(pres_list4)
            if np.all((temp_list3==0)|(pres_list3==0)):
                break
            else:
                lat_list.append(lat_data[j])
                lon_list.append(lon_data[j])
                if x != 0:
                    for i in range(len(temp_list4)):
                        worksheet.write(i,r,temp_list4[i])
                    an = np.polyfit(pres_list4, temp_list4, 3)
                else:
                    for i in range(len(temp_list3)):
                        worksheet.write(i,r,temp_list3[i])
                    an = np.polyfit(pres_list3, temp_list3, 3)

                a.append(an)
                #p[r] = np.poly1d(an)
                # x[k] = np.polyval(an, pres_list)
                #print(p[k])
                k = k + 1
                r = r + 1
    else:
        lat_list.append(lat_data[k])
        lon_list.append(lon_data[k])
        an = np.polyfit(pres_data, temp_data, 3)
        a.append(an)
        #p[r] = np.poly1d(an)
        #x[k] = np.polyval(an, pres_data)
        #print(p[k])
        k = k + 1
        r = r + 1

    i = i + 1

#print(k)
#print(lat_list)
#print(lon_list)
#print(p)
#print(a)
#print(len(lat_list))
#print(len(lon_list))
#print(len(p))
#print(a)

worksheet2=workbook.add_worksheet('sheet2')
for i in range(len(lon_list)):
    worksheet2.write(i, 0, lon_list[i])
    worksheet2.write(i, 1, lat_list[i])
tempnew = {}
for i in range(len(a)):
    tempnew[i] = np.polyval(a[i], 50)
    worksheet2.write(i, 2, tempnew[i])
tempnew2=list(tempnew.values())
#print(tempnew2)

workbook.close()
wk=xlrd.open_workbook('D:/wxd/ex/data1.xlsx')
wks=wk.sheet_by_name('sheet2')
#print(wks.cell(1,1).value)

index=np.random.choice(len(lon_list),50,replace=False)
#print(index)
'''
x_dict = {}
y_dict = {}
z_dict = {}
for i in range(len(index)):
    x_dict[i] = wks.cell(index[i], 0).value
    y_dict[i] = wks.cell(index[i], 1).value
    z_dict[i] = wks.cell(index[i], 2).value
x=list(x_dict.values())
y=list(y_dict.values())
z=list(z_dict.values())
'''
n_row={}
for i in range(len(index)):
    n_row[i] = wks.row_values(rowx=i)
n_row2=list(n_row.values())
#print(n_row2)
n_row3=sorted(n_row2,key=lambda x:(x[0],x[1]))
#print(n_row3)

x_dict= {}
y_dict= {}
z_dict= {}
for i in range(len(n_row3)):
    x_dict[i]=n_row3[i][0]
    y_dict[i] = n_row3[i][1]
    z_dict[i] = n_row3[i][2]
x=list(x_dict.values())
y=list(y_dict.values())
z=list(z_dict.values())
print(z)

OK=OrdinaryKriging(x,y,z,variogram_model='gaussian')
x_grid,y_grid=np.meshgrid(x,y)
#print(x_grid)
zk,ss=OK.execute('grid',x,y)
print(zk)
#znew,ss=OK.execute('points',lon_list,lat_list)
#znew,ss=OK.execute('points',x_grid.flatten(),y_grid.flatten())
#plt.scatter(x,y,color='r',marker='+')

plt.contourf(x_grid,y_grid,zk,levels=np.arange(0,35,0.001),cmap="jet")
plt.colorbar()
plt.title("Kriging")
plt.show()


'''
dst=nc.Dataset(path)
#print(dst)
all_vars=dst.variables.keys()
#print(all_vars)
lat=(dst.variables['LATITUDE'][:])
lon=(dst.variables['LONGITUDE'][:])
time=(dst.variables['TIME'][:])
temp=(dst.variables['TEMP'][:])
pres=(dst.variables['PRES'][:])
temp_data=temp.flatten()
pres_data=pres.flatten()
print(time)
print(temp)
print(pres)
print(len(temp_data))
#print(dst.variables['PRES'])

fig, ax = plt.subplots()
plt.gca().invert_yaxis()
an = np.polyfit(pres_data, temp_data, 3)
p = np.poly1d(an)
x = np.polyval(an,pres_data)

ax.plot(temp_data, pres_data, '*')
ax.plot(x, pres_data, 'r')
ax.set_ylabel('pressure(db)') # y轴命名
ax.set_xlabel('temperature(degree)') # x轴命名
plt.show()
'''