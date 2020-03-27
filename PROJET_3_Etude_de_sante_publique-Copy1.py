
# coding: utf-8

# # QUESTION 1

# # Créez un dataframe contenant les informations de population de chaque pays. Calculez le nombre total d’humains sur la planète. Donnez le résultat de votre calcul pour l'année 2013, ainsi que pour la dernière année disponible au jour où vous effectuez ce projet (2018).

# In[3]:


# Import des librairies
import numpy as np
import pandas as pd
import seaborn as sns


# In[4]:


# Import des données de la population mondiale 2013, 2017 (je vais en avoir besoin) et 2018
pop = pd.read_csv("C:/Users/Zang/Documents/APPRENDER/OPENCLASSROOMS/PARCOURS DA/P3_Etude_de_sante_publique/Pop_mond13-17-18.csv")


# In[5]:


# Je vérifie le type de données
pop.dtypes


# In[8]:


# Je regarde les données dans leur ensemble
pop.describe(include='all')


# In[9]:


# Vérification de l'import
pop.head()


# In[10]:


# Nettoyage du dataframe
pop.drop(["Code Domaine", "Domaine", "Code Élément", "Code Produit", "Produit", "Code année","Note"], axis=1).head()


# In[11]:


# Calcul des populations mondiales 2013, 2017 et 2018
pop_gb = pop.groupby("Année")


# In[12]:


pop_gb[['Valeur']].sum()*1000


# Mais sur Wikipedia, pop mondiale 2010 = env. 7 milliards; 2020 = env. 7,8 milliards => mes chiffres sont trop élevés. 

# In[57]:


pop.Zone.unique()


# Chine apparait plusieurs fois

# In[13]:


pop[pop["Zone"]=="Chine"]
# Seule occurrence à conserver


# In[30]:


pop[pop["Zone"]=="Chine - RAS de Hong-Kong"]


# In[31]:


pop[pop["Zone"]=="Chine - RAS de Macao"]


# In[32]:


pop[pop["Zone"]=="Chine, continentale"]


# In[33]:


pop[pop["Zone"]=="Chine, Taiwan Province de"]


# In[14]:


# Je garde seulement la ligne "Chine" et supprime les autres
pop = pop.drop([126,127,128,129,130,131,132,133,134,135,136,137])


# In[15]:


# Recalcul des pop 2013,2017,2018
pop_gb2 = (pop.groupby("Année").sum())*1000


# In[16]:


pop_gb2['Valeur']


# # QUESTION 3

# # Calculez (pour chaque pays et chaque produit) la disponibilité alimentaire en kcal puis en kg de protéines.

# ## Disponibilité alimentaire en kcal

# In[17]:


# Import des données des bilans alimentaires 2017 
veg = pd.read_csv("C:/Users/Zang/Documents/APPRENDER/OPENCLASSROOMS/PARCOURS DA/P3_Etude_de_sante_publique/vegetal2017.csv")
ani = pd.read_csv("C:/Users/Zang/Documents/APPRENDER/OPENCLASSROOMS/PARCOURS DA/P3_Etude_de_sante_publique/animal2017.csv")


# In[18]:


# Ajout de la variable origin
ani["origin"] = "animal"
veg["origin"] = "vegetal"


# In[19]:


# On regroupe veg et ani en un unique dataframe, via une union
temp = ani.append(veg)


# In[20]:


# Suppression de ani et veg
del ani, veg


# In[21]:


# On renomme les colonnes de temp
temp.columns = ["xx","xx2","country_code","country",'xx3','element','item_code','item','xx4',"year","unit","value"
                ,'origin']


# In[22]:


# Vérification
temp.head()


# In[23]:


# Transformation de temp en table pivot
data = temp.pivot_table(index=["country_code","country","item_code","item","year","origin"],columns = ["element"], 
values=["value"], aggfunc=sum)


# In[24]:


data.head()


# In[25]:


# On renomme les colonnes
data.columns = ['aliments pour touristes','aliments pour animaux','autres utilisations (non alimentaire)',
                'disponibilité alimentaire (Kcal/personne/jour)','disponibilité alimentaire en quantité (kg/personne/an)',
                'Disponibilité de matière grasse en quantité (g/personne/jour)',
                'Disponibilité de protéines en quantité (g/personne/jour)','disponibilité intérieure (en milliers de tonnes)', 'export-qté',
                'import-qté','nourriture','pertes', 'production','résidus','semences','traitement','variation de stock']


# In[26]:


data = data.reset_index()


# In[27]:


data.head()


# In[28]:


data.shape


# In[29]:


data.dtypes


# In[31]:


data.describe(include='all')


# In[164]:


data.isnull().sum()


# In[32]:


# Je vais chercher la population de l'année 2017 : 
pop2017 = pop[pop["Année"]==2017]


# In[33]:


pop2017.head()


# In[34]:


# J'enlève les colonnes inutiles
pop2017 = pop2017.drop(["Code Domaine", "Domaine", "Code Élément", "Code Produit", "Produit", "Code année","Note"], axis=1).head()


# In[35]:


pop2017.head()


# In[36]:


# Je créé la colonne population
pop2017['population'] = pop2017['Valeur'] * 1000


# In[37]:


pop2017.head()


# In[38]:


# Je modifie le type de population en entier
pop2017 = pop2017.astype({'population':'int'})


# In[39]:


pop2017['population'].dtypes


# In[40]:


pop2017.head()


# In[41]:


# Je garde les colonnes utiles pour la jointure
pop2017 = pop2017[['Code zone','population']]


# In[42]:


pop2017.head()


# In[43]:


# Jointure entre data et pop2017 sur Code zone 
datapop2017 = pd.merge(data, pop2017, left_on=['country_code'], right_on=['Code zone'])


# In[44]:


datapop2017.head()


# In[45]:


datapop2017.describe(include='all')


# In[46]:


# Vérification de l'absence d'occurrences muliples de la Chine
datapop2017[datapop2017["country"]=="Chine - RAS de Hong-Kong"]


# In[47]:


print(datapop2017.isnull().sum())


# In[48]:


datapop2017['disponibilité alimentaire (Kcal/personne/jour)'].describe()


# In[50]:


# Création de la colonne disponibilité alimentaire (Kcal/pays/jour)
datapop2017['disponibilité alimentaire (kcal/pays/jour)'] = datapop2017['disponibilité alimentaire (Kcal/personne/jour)'] * datapop2017['population']


# In[51]:


datapop2017.head()


# In[52]:


# Vérification du nb de données manquantes dans la colonne disponibilité alimentaire (Kcal/personne/jour)
data['disponibilité alimentaire (Kcal/personne/jour)'].isnull().sum()


# ## Disponibilité alimentaire en kg de protéines

# In[53]:


datapop2017['Disponibilité de protéines en quantité (g/personne/jour)'].describe()


# In[54]:


# Création de la colonne Disponibilité alimentaire (kg de protéines/pays/jour)
datapop2017['disponibilité alimentaire (Kg de protéines/pays/jour)'] = datapop2017['Disponibilité de protéines en quantité (g/personne/jour)'] * datapop2017['population'] * 1000


# In[55]:


datapop2017.head()


# In[56]:


datapop2017.shape


# # QUESTION 4

# # A partir de ces dernières informations, et à partir du poids de la disponibilité alimentaire pour chaque pays et chaque produit), calculez pour chaque produit le ratio "énergie/poids", que vous donnerez en kcal/kg.    
# # En suivant la même méthodologie, calculez également le pourcentage de protéines de chaque produit (pour chaque pays). Ce pourcentage est obtenu en calculant le ratio "poids de protéines/poids total" (attention aux unités utilisées). 

# ### Ratio "énergie/poids"

# Vu sur Wikipédia : moyenne valeur calorique d'un oeuf = 147 kcal/100g = 1470 kcal/kg  
# Calcul :  
# Ratio énergie/poids = Disponibilité alimentaire (Kcal/pays/jour)/Disponibilité alimentaire en quantité (kg/pays/jour)

# In[57]:


datapop2017['disponibilité alimentaire en quantité (kg/personne/an)'].describe()


# In[61]:


# Création de la colonne 'disponibilité alimentaire en quantité (kg/pays/jour)'
datapop2017['disponibilité alimentaire en quantité (kg/pays/jour)'] = datapop2017['disponibilité alimentaire en quantité (kg/personne/an)'] * datapop2017['population'] / 365


# In[62]:


datapop2017.head()


# In[63]:


datapop2017['disponibilité alimentaire en quantité (kg/pays/jour)'].dtypes


# In[65]:


# Création de la colonne 'ratio énergie/poids'
datapop2017['ratio énergie/poids (Kcal/kg)'] = datapop2017['disponibilité alimentaire (kcal/pays/jour)'] / datapop2017['disponibilité alimentaire en quantité (kg/pays/jour)']


# In[68]:


# Vérification pour les oeufs
datapop2017[datapop2017['item']=='Oeufs']


# #### La question 6 me fait reprendre cette question car j'obtiens des données incohérentes. 

# In[69]:


datapop2017['ratio énergie/poids (Kcal/kg)'].describe()


# ##### Nettoyage de 'ratio énergie/poids (Kcal/kg)' : 0, NaN, inf

# In[71]:


datapop2017REP = datapop2017[datapop2017['ratio énergie/poids (Kcal/kg)'] != 0]


# In[72]:


datapop2017REP[datapop2017REP['ratio énergie/poids (Kcal/kg)'] < 0]


# In[73]:


datapop2017REP[datapop2017REP['ratio énergie/poids (Kcal/kg)'] > 10000000]


# In[74]:


# Je supprime les lignes contenant 'inf'. 
datapop2017REP = datapop2017REP.drop([55,104,137,157,229,290,303,304,305,324,419])


# In[75]:


datapop2017REP['ratio énergie/poids (Kcal/kg)'].describe()


# In[76]:


datapop2017REP['ratio énergie/poids (Kcal/kg)'].max()


# In[79]:


# Je vérifie la donnée max pour voir si elle est cohérente
datapop2017REP[datapop2017REP['ratio énergie/poids (Kcal/kg)']==94652.54237288136]


# In[80]:


datapop2017REP.head()


# ### En suivant la même méthodologie, calculez également le pourcentage de protéines de chaque produit (pour chaque pays). Ce pourcentage est obtenu en calculant le ratio "poids de protéines/poids total" (attention aux unités utilisées).

# Teneur en protéines de l'avoine : 10.70g par 100g soit 10.7%

# In[81]:


# Création de la colonne disponibilité alimentaire en quantité (g/personne/jour) à partir de la colonne disponibilité 
# alimentaire en quantité (kg/personne/an)
datapop2017['disponibilité alimentaire en quantité (g/personne/jour)'] = datapop2017['disponibilité alimentaire en quantité (kg/personne/an)'] * 1000 / 365


# In[82]:


# Création de la colonne '% de protéines'
datapop2017['% de protéines'] =  datapop2017['Disponibilité de protéines en quantité (g/personne/jour)'] / datapop2017['disponibilité alimentaire en quantité (g/personne/jour)'] * 100


# In[83]:


datapop2017.head()


# In[84]:


# Vérification
datapop2017[datapop2017['item']=='Avoine']


# # QUESTION 5

# ## Citez 5 aliments parmi les 20 aliments les plus caloriques, en utilisant le ratio énergie/poids.
# Étonnamment, il arrive que ce ratio soit différent en fonction du pays. Il faudra donc réaliser pour chaque aliment une moyenne sur les différents pays. Vous créerez donc une nouvelle table grâce à une agrégation. Attention à bien retirer les valeurs égales à 0 afin de ne pas fausser le calcul de la moyenne.
# Citez 5 aliments parmi les 20 aliments les plus riches en protéines.

# In[85]:


# datapop2017REP[datapop2017REP['ratio énergie/poids (Kcal/kg)']==0].head()


# In[87]:


# Moyenne ratio énergie/poids par item
datapop2017REP.groupby('item').mean().filter(['ratio énergie/poids (Kcal/kg)']).sort_values(by = 'ratio énergie/poids (Kcal/kg)',ascending=False).head()


# In[88]:


# nb de valeurs nulles
datapop2017REP['ratio énergie/poids (Kcal/kg)'].isnull().sum()


# Les 5 aliments les plus caloriques d'après mon df :   
# Graisses Animales Crue  
# Huile de Sésame  
# Huile de Germe de Maïs  
# Huile de Tournesol  
# Huile de Palme  

# In[89]:


# Pour la question 6, je créé un df ratio énergie/poids afin d'ensuite faire une jointure :
dfREP = datapop2017REP.groupby('item').mean()


# In[90]:


dfREP.head()


# In[91]:


# Suppression de l'index
dfREP = dfREP.reset_index()


# In[92]:


# Je ne conserve que les colonnes utiles
dfREP = dfREP[['item','item_code','ratio énergie/poids (Kcal/kg)']]


# In[93]:


dfREP.head()


# ## Citez 5 aliments parmi les 20 aliments les plus riches en protéines.

# In[97]:


# Je vérifie si des valeurs sont = à 0
datapop2017[datapop2017['% de protéines']==0].head()


# In[95]:


# Je supprime les lignes contenant = 0 dans le % de protéines. 
# Je créé un df pour cela. 
datapop2017PROT = datapop2017[datapop2017['% de protéines']!=0]


# In[101]:


datapop2017PROT.groupby('item').mean().filter(['% de protéines']).sort_values(by = '% de protéines',ascending=False).head(20)


# In[102]:


# Pour trouver les valeurs 'inf'
datapop2017PROT[datapop2017PROT['% de protéines']>1000000000]


# In[103]:


# Je supprime les lignes contenant 'inf' dans le % de protéines. 
# Je créé un df pour cela. 
datapop2017PROT = datapop2017PROT.drop([55,137,157,229,303,304,324,419])


# In[104]:


# Je refais le group by
datapop2017PROT.groupby('item').mean().filter(['% de protéines']).sort_values(by = '% de protéines',ascending=False).head(20)


# Réponse à la question :   
# Soja  
# Viande, Autre  
# Légumineuses Autres  
# Pois  
# Arachides Decortiquees  

# ## Donnez les résultats des questions 6 à 14 pour l'année 2013 ainsi que pour la dernière année disponible dans les données de la FAO (actuellement 2017).

# # QUESTION 6

# ## Calculez, pour les produits végétaux uniquement, la disponibilité intérieure mondiale exprimée en kcal.

# ## Pour 2013 : 

# In[105]:


# Import des données des bilans alimentaires 2013
veg13 = pd.read_csv("C:/Users/Zang/Documents/APPRENDER/OPENCLASSROOMS/PARCOURS DA/P3_Etude_de_sante_publique/vegetal2013.csv")
ani13 = pd.read_csv("C:/Users/Zang/Documents/APPRENDER/OPENCLASSROOMS/PARCOURS DA/P3_Etude_de_sante_publique/animal2013.csv")


# In[106]:


# Ajout de la variable origin
ani13["origin"] = "animal"
veg13["origin"] = "vegetal"


# In[107]:


# On regroupe veg13 et ani13 en un unique dataframe, via une union
temp13 = ani13.append(veg13)


# In[108]:


temp13.columns = ["xx","xx2","country_code","country",'xx3','element','item_code','item','xx4',"year","unit","value"
                ,'origin']


# In[109]:


# Vérification
temp13.head()


# In[110]:


# Transformation de temp13 en table pivot
data13 = temp13.pivot_table(index=["country_code","country","item_code","item","year","origin"],columns = ["element"], 
values=["value"], aggfunc=sum)


# In[111]:


data13.head()


# In[112]:


# On renomme les colonnes
data13.columns = ['aliments pour animaux','autres utilisations (non alimentaire)',
                'disponibilité alimentaire (Kcal/personne/jour)','disponibilité alimentaire en quantité (kg/personne/an)',
                'Disponibilité de matière grasse en quantité (g/personne/jour)',
                'Disponibilité de protéines en quantité (g/personne/jour)','disponibilité intérieure (en milliers de tonnes)', 'export-qté',
                'import-qté','nourriture','pertes', 'production','semences','traitement','variation de stock']


# In[113]:


data13 = data13.reset_index()


# In[114]:


data13.shape


# In[115]:


data13 = data13[data13["country"]!="Chine - RAS de Hong-Kong"]


# In[116]:


data13 = data13[data13["country"]!="Chine - RAS de Macao"] 


# In[117]:


data13 = data13[data13["country"]!="Chine, continentale"]


# In[118]:


data13 = data13[data13["country"]!="Chine, Taiwan Province de"]


# In[119]:


data13.shape


# In[120]:


data13.head()


# In[121]:


pop2013 = pop[pop["Année"]==2013]


# In[122]:


pop2013.shape


# In[123]:


pop2013.head()


# In[124]:


pop2013 = pop2013.drop(["Code Domaine", "Domaine", "Code Élément", "Code Produit", "Produit", "Code année","Note"], axis=1)


# In[125]:


pop2013.shape


# In[126]:


# Je créé la colonne population
pop2013['population'] = pop2013['Valeur'] * 1000


# In[127]:


pop2013.head()


# In[128]:


# Je modifie le type de population en entier
pop2013 = pop2013.astype({'population':'int'})


# In[129]:


# Je garde les colonnes utiles pour la jointure
pop2013 = pop2013[['Code zone','population']]


# In[140]:


# Jointure entre data2013 et pop2013 sur Code zone 
datapop2013 = pd.merge(data13, pop2013, left_on=['country_code'], right_on=['Code zone'])


# In[141]:


datapop2013.head()


# In[142]:


datapop2013[datapop2013["country"]=='Chine - RAS de Hong-Kong']


# In[150]:


# Jointure sur item_code pour avoir le ratio Energie/poids
datapop2013rep = pd.merge(datapop2013, dfREP)


# In[151]:


datapop2013rep.head()


# In[152]:


datapop2013rep.shape


# In[153]:


datapop2013rep['disponibilité intérieure mondiale (kcal)'] = datapop2013rep['ratio énergie/poids (Kcal/kg)'] * datapop2013rep['disponibilité intérieure (en milliers de tonnes)'] * 1000000


# In[154]:


datapop2013rep.head()


# In[155]:


datapop2013rep['disponibilité intérieure mondiale (kcal)'].sum()


# Pour 2013 la disponibilité intérieure mondiale est de presque 1,4e16 kcal.  
# Ces chiffres sont toutefois peu cohérents avec 2017

# In[156]:


datapop2013rep['disponibilité intérieure mondiale (kcal)'].describe()


# Une dispo intérieure négative est a priori possible. 

# ## Pour 2017 : 

# In[157]:


datapop2017['disponibilité intérieure mondiale (kcal)'] = datapop2017['ratio énergie/poids (Kcal/kg)'] * datapop2017['disponibilité intérieure (en milliers de tonnes)'] * 1000000


# In[158]:


datapop2017['disponibilité intérieure mondiale (kcal)'].sum()


# In[159]:


# Pour trouver les valeurs 'inf'
datapop2017[datapop2017['disponibilité intérieure mondiale (kcal)']>1000000000000000000]


# In[160]:


# Je supprime les lignes contenant 'inf'. 
# Je suis apparemment obligé de créer un df pour cela. 
datapop2017dispint = datapop2017.drop([229,290,303,304,305,324,419])


# In[161]:


datapop2017dispint['disponibilité intérieure mondiale (kcal)'].sum()


# Pour 2017 la disponibilité intérieure mondiale serait de 5,3e14 kcal.

# In[163]:


datapop2017dispint['disponibilité intérieure mondiale (kcal)'].describe()


# # QUESTION 7

# ## Combien d'humains pourraient être nourris si toute la disponibilité intérieure mondiale de produits végétaux était utilisée pour de la nourriture ? Donnez les résultats en termes de calories, puis de protéines, et exprimez ensuite ces 2 résultats en pourcentage de la population mondiale.
