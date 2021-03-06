# -*- coding: utf-8 -*-
"""
Created on Wed May  9 17:09:15 2018

@author: Sven

Dit script voorspelt de verdeling van zorgproducten door regressie.

To-Do:
    (1) Maak een eerste voorspelling met echte data
    (2) Voeg ridge-regressie toe
    (3) plot de gewichten van de maanden voor ieder lambda
    (4) maak een cross-validatie met de data
"""
import import_data as imp



def regressie_functie(verdeling):
    """Deze functie neemt een zorgprudctverdeling 'verdeling' (numpy-array)
    als vector als input en geeft een matrix terug, waarin voor ieder regel
    van de input een outputregel bestaat en waarin iedere kolom een andere
    functie is, namelijk [x, x^2, x^3, AVG(x), MEDIAN(x)]."""
    import numpy as np
    
    v = np.array(verdeling)
    v_vec = [v, v**2, v**3, np.mean(v)*np.ones_like(v), np.median(v)*np.ones_like(v)]
    
    return np.asmatrix(v_vec).T
    
def bepaal_gewichten(data, betrouwbaar_tot, maanden_terug = 12, maanden_vooruit = 1):
    """Deze functie voert de eigenlijke regressie uit.
        - data is een pandas.DataFrame;
        - betrouwbaar_tot is een Maand_Nr en geeft de laatste maand aan
        van welke de data nog betrouwbaar is om voor voorspellingen gebruikt te
        worden;
        - maanden_terug is het aantal maanden dat voor de voorspelling gebruikt
        wordt, exclusief de laatste betrouwbare maand;
        - maanden_vooruit is het aantal maanden dat in de toekomst wordt
        voorspelt, ten minste 1."""
    import numpy as np
    import pandas as pd
    
    decl = pd.DataFrame(data)
    m_min = np.min(decl.Maand_Nr) + maanden_terug
    
    #Maak de vector met resultaten van de regressie:
    y_chk  = decl.loc[:,("Maand_Nr","AANTAL")][(decl.Maand_Nr <= betrouwbaar_tot) &
                            (decl.Maand_Nr >= m_min)]
    print(y_chk.shape)
       
    #Maak de matrixes met de input voor de regressie:
    empty_out = regressie_functie(0) #Om te bepalen hoe groot de output van de regessiefuncties is. Dit is nodig voor het aanmaken van de X-dataframe.
    X_chk = pd.DataFrame({"AANTAL_{0}".format(ind): [-1,-1] for ind in range(maanden_terug * empty_out.size)})    
    
        #X_chk = pd.DataFrame(regressie_functie(decl.AANTAL[decl.Maand_Nr == m - maanden_terug]))
    
    for m in range(m_min, betrouwbaar_tot + 1):
        X_collect = list(regressie_functie(decl.AANTAL[decl.Maand_Nr == m_x]) for m_x in range(m - maanden_terug, m))
      #  X_collect = pd.DataFrame(np.asmatrix(X_collect))
        X_chk = pd.concat((X_chk,(pd.DataFrame(x) for x in X_collect)), axis = 1, ignore_index = True)
        
    print(X_chk)
    print(X_collect)        
    """
    #X_chk = list()
    
        
        X_step = list()
        
        for jaar_maand_cursor in declaraties.Jaar_Maand_Nr[(declaraties.Jaar_Maand_Nr < jaar_maand) & (declaraties.Jaar_Maand_Nr > jaar_maand - maanden_terug)]:
           X_collect = regressie_functie(declaraties.AANTAL[declaraties.Jaar_Maand_Nr == jaar_maand_cursor])
           X_step.append(X_collect)
        
    print(np.array(X_step).concate(axis = 0))
    
    
    
        #X_step = np.mat()
        
        
            
        #X_chk = np.concatenate(X_chk,X_step, axis = 0)
       """     
    return y_chk
    
#main:
declaratie_data = imp.maak_dummy_data()

zorgproductgewichten = bepaal_gewichten(data = declaratie_data, betrouwbaar_tot = 60)
#print(zorgproductgewichten)

