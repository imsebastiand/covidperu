#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# **MAPA**

# In[2]:


import ipyleaflet
import json
import pandas as pd
from branca.colormap import linear
import branca.colormap as cm
import numpy as np


# In[3]:


with open('peru_departamental_simple.geojson') as f:
    geo_json_data = json.load(f)


# In[4]:


geo_json_data


# In[5]:


for i in geo_json_data['features']:
    i['id'] = i['properties']['NOMBDEP']


# **COVID PERU POR DEPARTAMENTO**

# In[6]:


covid = pd.read_csv("DATOSABIERTOS_SISCOVID.csv", encoding='ISO-8859-1')


# In[7]:


covid.head()


# In[8]:


covid.shape


# In[9]:


covid = covid.drop(columns=['UUID'])


# In[10]:


covid.head(3)


# In[11]:


#se ven los casos nulos


# In[12]:


covid.isnull().sum()


# In[13]:


xdepartamentos = covid.DEPARTAMENTO.value_counts()
xdepartamentos


# In[14]:


xdepartamentos = covid.DEPARTAMENTO.value_counts().rename_axis('unique_values').reset_index(name='counts')
xdepartamentos


# In[15]:


choro_map_data_covidxdep =  dict(zip(xdepartamentos['unique_values'].tolist(), xdepartamentos['counts'].tolist()))


# In[16]:


colormap = cm.StepColormap(colors=['#FFA07A','#F08080','#CD5C5C', '#FF7F50', '#FF6347','#DC143C','#B22222', '#A52A2A'],
                           index=[min(choro_map_data_covidxdep.values()),
                                  np.percentile(list(choro_map_data_covidxdep.values()), 12.5),
                                  np.percentile(list(choro_map_data_covidxdep.values()), 25),
                                  np.percentile(list(choro_map_data_covidxdep.values()), 37.5),
                                  np.median(list(choro_map_data_covidxdep.values())),
                                  np.percentile(list(choro_map_data_covidxdep.values()), 62.5),
                                  np.percentile(list(choro_map_data_covidxdep.values()), 75),
                                  np.percentile(list(choro_map_data_covidxdep.values()), 87.5),
                                  max(choro_map_data_covidxdep.values())],
                           vmin=250,
                           vmax=66000)


# In[17]:


layercoviddepa = ipyleaflet.Choropleth(
    geo_data=geo_json_data,
    choro_data=choro_map_data_covidxdep,
    colormap=colormap,
    border_color='black',
    style={'fillOpacity': 0.6, 'dashArray': '5, 5'})

mapacoviddep = ipyleaflet.Map(center = (-10, -70), zoom = 4.9)
mapacoviddep.add_layer(layercoviddepa)
display(mapacoviddep)


# **COVID PER CAPITA**

# In[18]:


xdepartamentos2 = xdepartamentos.sort_values(by='unique_values',ascending = True).drop([10])
xdepartamentos2 = xdepartamentos2.reset_index()
xdepartamentos2 = xdepartamentos2.drop(columns=['index'])
xdepartamentos2


# In[19]:


xdepartamentos2["poblacion"]=[379384,
1083519,
405759,
1382730,
616176,
1341012,
994494,
1205527,
347639,
721047,
850765,
1246038,
1778080,
1197260,
9485405,
883510,
141070,
174863,
254065,
1856809,
1172697,
813381,
329332,
224863,
496459]


# In[20]:


#información de población según INEI 2017


# In[21]:


xdepartamentos2["percapita"]= xdepartamentos2["counts"]/xdepartamentos2["poblacion"]
xdepartamentos2


# In[22]:


choro_map_data_covidxdepper =  dict(zip(xdepartamentos2['unique_values'].tolist(), xdepartamentos2['percapita'].tolist()))


# In[23]:


layercoviddepaper = ipyleaflet.Choropleth(
    geo_data=geo_json_data,
    choro_data=choro_map_data_covidxdepper,
    colormap=linear.YlOrRd_04,
    border_color='black',
    style={'fillOpacity': 0.7
           , 'dashArray': '4, 4'})

mapacoviddepper = ipyleaflet.Map(center = (-10, -70), zoom = 4.9)
mapacoviddepper.add_layer(layercoviddepaper)
display(mapacoviddepper)


# In[ ]:





# **COVID POR PROVINCIA**

# In[24]:


with open('peru_provincial_simple.geojson') as f:
    geo_json_data_prov = json.load(f)


# In[25]:


geo_json_data_prov


# In[26]:


for i in geo_json_data_prov['features']:
    i['id'] = i['properties']['NOMBPROV']


# In[27]:


covid['PROVINCIA']= covid['PROVINCIA'].astype(str)


# In[28]:


covid.PROVINCIA.value_counts()


# In[29]:


#esta contando doble algunos nombres porque tienen espacio al final por eso se hace lo siguiente:


# In[30]:


for x in covid['PROVINCIA']:
    x = x.rstrip()


# In[31]:


covid.PROVINCIA.value_counts()


# In[32]:


covid['PROVINCIA'] = covid['PROVINCIA'].apply(lambda x: x.rstrip())


# In[33]:


covid.PROVINCIA.unique()


# In[34]:


covid.PROVINCIA.value_counts()


# In[35]:


#hay nombres con tildes lo cuál hace que exista duplicidad en algunos casos , adicionalmente pueden existir problemas 
#al integrar esto con el archivo geo_json para hacer el mapa por lo que se arreglará esto


# In[36]:


#se usará esta función
def normalize(s):
    replacements = (
        ("á", "a"),
        ("à", "a"),
        ("è", "è"),
        ("é", "e"),
        ("ì", "ì"),
        ("í", "i"),
        ("ò", "o"),
        ("ó", "o"),
        ("ù", "ù"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

print(normalize("¡Hólá, múndó!"))
print(normalize("¡HÓLÁ, MÚNDÓ!"))


# In[37]:


covid['PROVINCIA'] = covid['PROVINCIA'].apply(lambda x: normalize(x))


# In[38]:


covid['PROVINCIA'].unique()


# In[39]:


#ahora si pasamos a hacer el mapa 


# In[40]:


xprovincias = covid.PROVINCIA.value_counts().rename_axis('unique_values').reset_index(name='counts')
xprovincias


# In[41]:


choro_map_data_covidxprov =  dict(zip(xprovincias['unique_values'].tolist(), xprovincias['counts'].tolist()))


# In[42]:


layercovidprov = ipyleaflet.Choropleth(
    geo_data=geo_json_data_prov,
    choro_data=choro_map_data_covidxprov,
    colormap=linear.YlOrRd_04,
    border_color='black',
    style={'fillOpacity': 0.7
           , 'dashArray': '4, 4'})

mapacovidprov = ipyleaflet.Map(center = (-10, -70), zoom = 4.9)
mapacovidprov.add_layer(layercovidprov)
display(mapacovidprov)


# In[43]:


#al parecer faltan datos de la provincia Antonio Raymondi 


# In[44]:


import pandas as pd
pd.set_option('display.max_rows', 200)


# In[45]:


xprovincias


# In[46]:


xprovincias = xprovincias.append(pd.Series(['ANTONIO RAYMONDI', 0], index=xprovincias.columns ), ignore_index=True)


# In[47]:


xprovincias


# In[48]:


choro_map_data_covidxprov =  dict(zip(xprovincias['unique_values'].tolist(), xprovincias['counts'].tolist()))


# In[49]:


layercovidprov = ipyleaflet.Choropleth(
    geo_data=geo_json_data_prov,
    choro_data=choro_map_data_covidxprov,
    colormap=linear.YlOrRd_04,
    border_color='black',
    style={'fillOpacity': 0.7
           , 'dashArray': '4, 4'})

mapacovidprov = ipyleaflet.Map(center = (-10, -70), zoom = 4.9)
mapacovidprov.add_layer(layercovidprov)
display(mapacovidprov)


# In[50]:


#lo mismo pero con Bolivar y con el resto de provincias que aparecieron después faltando (los pasos donde aparecen los errores
#se eliminaron ya que son lo mismo de arriba), se agregaron las provincias faltantes y se fue actualizando
#el mapa choro_map


# In[51]:


xprovincias = xprovincias.append(pd.Series(['BOLIVAR', 0], index=xprovincias.columns ), ignore_index=True)


# In[52]:


choro_map_data_covidxprov =  dict(zip(xprovincias['unique_values'].tolist(), xprovincias['counts'].tolist()))


# In[53]:


xprovincias = xprovincias.append(pd.Series(['CANDARAVE', 0], index=xprovincias.columns ), ignore_index=True)


# In[54]:


choro_map_data_covidxprov =  dict(zip(xprovincias['unique_values'].tolist(), xprovincias['counts'].tolist()))


# In[55]:


xprovincias = xprovincias.append(pd.Series(['GENERAL SANCHEZ CERRO', 0], index=xprovincias.columns ), ignore_index=True)


# In[56]:


choro_map_data_covidxprov =  dict(zip(xprovincias['unique_values'].tolist(), xprovincias['counts'].tolist()))


# In[57]:


xprovincias = xprovincias.append(pd.Series(['HUACAYBAMBA', 0], index=xprovincias.columns ), ignore_index=True)


# In[58]:


choro_map_data_covidxprov =  dict(zip(xprovincias['unique_values'].tolist(), xprovincias['counts'].tolist()))


# In[59]:


xprovincias = xprovincias.append(pd.Series(['MOHO', 0], index=xprovincias.columns ), ignore_index=True)


# In[60]:


choro_map_data_covidxprov =  dict(zip(xprovincias['unique_values'].tolist(), xprovincias['counts'].tolist()))


# In[61]:


xprovincias = xprovincias.append(pd.Series(['OCROS', 0], index=xprovincias.columns ), ignore_index=True)


# In[62]:


choro_map_data_covidxprov =  dict(zip(xprovincias['unique_values'].tolist(), xprovincias['counts'].tolist()))


# In[63]:


layercovidprov = ipyleaflet.Choropleth(
    geo_data=geo_json_data_prov,
    choro_data=choro_map_data_covidxprov,
    colormap=linear.YlOrRd_04,
    border_color='black',
    style={'fillOpacity': 0.7
           , 'dashArray': '4, 4'})

mapacovidprov = ipyleaflet.Map(center = (-10, -70), zoom = 4.9)
mapacovidprov.add_layer(layercovidprov)
display(mapacovidprov)


# In[64]:


#esto se hace para ver los nombres y si hay un error , hay una forma de iterar pero por el momento no lo he hecho
pd.set_option('display.max_rows', 230)


# In[65]:


xprovincias


# In[66]:


#provincias = xprovincias


# In[67]:


#xprovincias.drop([1])y también ([149])


# In[68]:


#FALTA CORREGIR LO DE ARRIBA EL COLLAO Y PROV.CONST EN CALLAO y ver que otros errores ortográficos hay


# In[ ]:





# In[69]:


#en el archivo geo_json se corrigieron nombres de PIURA y MANUEL FAJARDO ya que aparecieron esos errores 
#al querer hacer el mapa


# In[70]:


#lo corro para ver cómo va quedando , se agrega la provincia de Sucre finalmente


# In[71]:


xprovincias = xprovincias.append(pd.Series(['SUCRE', 0], index=xprovincias.columns ), ignore_index=True)


# In[72]:


choro_map_data_covidxprov =  dict(zip(xprovincias['unique_values'].tolist(), xprovincias['counts'].tolist()))


# In[73]:


layercovidprov = ipyleaflet.Choropleth(
    geo_data=geo_json_data_prov,
    choro_data=choro_map_data_covidxprov,
    colormap=linear.YlOrRd_04,
    border_color='black',
    style={'fillOpacity': 0.7
           , 'dashArray': '4, 4'})

mapacovidprov = ipyleaflet.Map(center = (-10, -70), zoom = 4.9)
mapacovidprov.add_layer(layercovidprov)
display(mapacovidprov)


# In[74]:


#uso la paleta de colores hecha a mano anterior porque la básica no ilustra mucho


# In[75]:


colormap2 = cm.StepColormap(colors=['#FFA07A','#F08080','#CD5C5C', '#FF7F50', '#FF6347','#DC143C','#B22222', '#A52A2A'],
                           index=[min(choro_map_data_covidxprov.values()),
                                  np.percentile(list(choro_map_data_covidxdep.values()), 12.5),
                                  np.percentile(list(choro_map_data_covidxdep.values()), 25),
                                  np.percentile(list(choro_map_data_covidxdep.values()), 37.5),
                                  np.median(list(choro_map_data_covidxdep.values())),
                                  np.percentile(list(choro_map_data_covidxdep.values()), 62.5),
                                  np.percentile(list(choro_map_data_covidxdep.values()), 75),
                                  np.percentile(list(choro_map_data_covidxdep.values()), 87.5),
                                  max(choro_map_data_covidxdep.values())],
                           vmin=0,
                           vmax=64000)


# In[76]:


layercovidprov = ipyleaflet.Choropleth(
    geo_data=geo_json_data_prov,
    choro_data=choro_map_data_covidxprov,
    colormap=colormap2,
    border_color='black',
    style={'fillOpacity': 0.7
           , 'dashArray': '4, 4'})

mapacovidprov = ipyleaflet.Map(center = (-10, -70), zoom = 4.9)
mapacovidprov.add_layer(layercovidprov)
display(mapacovidprov)


# In[ ]:





# In[ ]:





# In[ ]:




