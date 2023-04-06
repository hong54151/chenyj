from argopy import DataFetcher as ArgoDataFetcher
import matplotlib.pyplot as plt
import numpy as np
import math
from math import sqrt
import openpyxl
argo_loader = ArgoDataFetcher()
# print(argo_loader.status())

ds = argo_loader.region([-75, -45, 20, 30, 0, 10, '2011-01-01', '2011-06']).to_xarray() # 读取区域包含的多个浮标多期的数据
#print(ds)
pr=ds['PLATFORM_NUMBER'].values
#n=len(pr)
n=10
n1=math.ceil(0.7*n)
print(n1)
# print(pr)

fig, ax = plt.subplots()
plt.gca().invert_yaxis()
xe=[]
ye=[]
for i in range(n1):
    dss = argo_loader.profile(pr[i], 2).to_xarray()
    dss_profiles = dss.argo.point2profile()
    temp = dss_profiles['TEMP'].values
    pres = dss_profiles['PRES'].values
    x = temp.flatten()
    y = pres.flatten()
    #print(i)
    #print(x)
    #print(y)
    if len(xe):
        # print('不为空')
        ye = y
        if len(x) < len(xe):
           for b in range(len(x)):
              count=(xe[b]+x[b])/2
              xe[b]=count
           for r in range(len(x),len(xe)):
              xe[r]=0

           #for r in range(len(xe)-1,len(x)-1,-1):
              #if xe[r]==0:
                  #del xe[r]
        else:
            for b in range(len(xe)):
             count=(xe[b]+x[b])/2
             xe[b]=count
    else:
        # print('为空')
        xe = x
        ye = y
#print(len(xe))
#print(len(ye))
#print(xe)
xee=[]
yee=[]
if len(xe)>len(ye):
    for i in range(len(ye)):
        if xe[i] != 0:
            xee.append(xe[i])
    yee=ye
else:
    for i in range(len(xe)):
        if ye[i] != 0:
            yee.append(ye[i])
    xee=xe
#print((len(xee)))

xe2=[]
ye2=[]
for i in range(n1,n):
    dss2 = argo_loader.profile(pr[i], 2).to_xarray()
    dss2_profiles = dss2.argo.point2profile()
    temp = dss2_profiles['TEMP'].values
    pres = dss2_profiles['PRES'].values
    x = temp.flatten()
    y = pres.flatten()
    if len(xe2):
        ye2 = y
        if len(x) < len(xe2):
            for b in range(len(x)):
                count = (xe2[b] + x[b]) / 2
                xe2[b] = count
            for r in range(len(x), len(xe2)):
                xe2[r] = 0
        else:
            for b in range(len(xe2)):
             count=(xe2[b]+x[b])/2
             xe2[b]=count
    else:
        xe2 = x
        ye2 = y
#print(len(xe2))
#print(len(ye2))
xee2=[]
yee2=[]
if len(xe2)>len(ye2):
    for i in range(len(ye2)):
        if xe2[i] != 0:
            xee2.append(xe2[i])
    yee2=ye2
else:
    for i in range(len(xe2)):
        if ye2[i] != 0:
            yee2.append(ye2[i])
    xee2=xe2
#print(len(xee2))
'''
degrees=np.arange(1,11)
for deg in degrees:
    an = np.polyfit(yee, xee, deg)
    p = np.poly1d(an)
    print("阶数=",deg)
    #print(p)
    x2 = np.polyval(an, yee)
    error=[]
    for i in range(len(y)):
        error.append(x2[i]-xee2[i])
    #print("error:",error)
    squarederror=[]
    for val in error:
        squarederror.append(val*val)
    #print("squarederrpor:",squarederror)
    rmse=sqrt(sum(squarederror)/len(squarederror))
    print("均方根误差",rmse)
'''
an = np.polyfit(yee, xee, 3)
p = np.poly1d(an)
xa = np.polyval(an,yee)
ax.plot(xee2, yee2, '*')
ax.plot(xa, yee, 'r')
ax.set_ylabel('pressure(db)') # y轴命名
ax.set_xlabel('temperature(degree)') # x轴命名
plt.show()

'''an = np.polyfit(y, x, 3)
    p = np.poly1d(an)
    x2 = np.polyval(an, y)
    ax.plot(temp.T, pres.T, '*')
    ax.plot(x2, pres.T, 'r')
ax.set_ylabel('pressure(db)') # y轴命名
ax.set_xlabel('temperature(degree)') # x轴命名
plt.show()
'''


'''  
dss = argo_loader.profile(pr[1], 2).to_xarray() # 读取一个浮标一期的数据，2为浮标周期数
dss_profiles = dss.argo.point2profile()
# print(dss_profiles)
temp = dss_profiles['TEMP'].values
pres = dss_profiles['PRES'].values
# print(temp.T)
# print(pres.T)
x=temp.flatten()
y=pres.flatten()
'''

'''
degrees=np.arange(1,12)
for deg in degrees:
    an = np.polyfit(y, x, deg)
    p = np.poly1d(an)
    print("阶数=",deg)
    #print(p)
    x2 = np.polyval(an, y)
    error=[]
    for i in range(len(y)):
        error.append(x2[i]-x[i])
    #print("error:",error)
    squarederror=[]
    for val in error:
        squarederror.append(val*val)
    #print("squarederrpor:",squarederror)
    rmse=sqrt(sum(squarederror)/len(squarederror))
    print("均方根误差",rmse)
'''

'''
print(x)
an=np.polyfit(y,x,9)
p=np.poly1d(an)
# print(p)
x2=np.polyval(an,y)
print(x2)
fig, ax = plt.subplots()
plt.gca().invert_yaxis()
ax.plot(temp.T,pres.T,'*')
ax.plot(x2,pres.T,'r')
ax.set_ylabel('pressure(db)') # y轴命名
ax.set_xlabel('temperature(degree)') # x轴命名
plt.show()
'''


#fig, ax = plt.subplots() # 在一个figure里画一张图ax
#plt.gca().invert_yaxis() #翻转y轴
#ax.plot(temp.T, pres.T)
#ax.scatter(temp.T, pres.T) # 在ax区域内做散点图
#ax.set_ylabel('pressure(db)') # y轴命名
#ax.set_xlabel('temperature(degree)') # x轴命名
#plt.show() # 显示作图结果