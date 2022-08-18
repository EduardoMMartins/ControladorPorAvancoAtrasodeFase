#Código do Projeto de Controlador por Avanço e Atraso de Fase

#Importando Funções
from ctypes.wintypes import WCHAR
import numpy as np
import control.matlab as ml
import matplotlib.pyplot as plt
import math
import scipy
from scipy.interpolate import interp1d
from control import *

#Definindo erro estático de velocidade constante (kv)
kv = 20 #[VALOR ADICIONADO]

#Definindo margem de fase desejada (pmd)
pmd = 50 #[VALOR ADICIONADO]

#Definindo g(s) 
num = np.array([2]) #[VALOR ADICIONADO]
den = np.polymul(np.array([1,2,0]),np.array([1,5])) #[VALOR ADICIONADO]
g = ml.tf(num,den)
print("Função de Transferência G(s): ", g)

#Definindo K
k = 5*kv #[EQUAÇÃO ADICIONADA]
print("K = ", k)

#Definindo G1(s)
g1 = k*g
print("Função de Transferência G1(s): ", g1)
mag,phase,w = ml.bode(g1)

#Calculando a Margem de Ganho e Fase
gm,pm,wg,wp = margin(g1)
print("Margem de Ganho: ", gm)
#pm = math.ceil(pm) #Arredonda o valor da Margem de Fase para cima
print("Margem de Fase: ", pm)
wc = wg
print("wc = ", wg)

#Definindo Ângulo de fase requerido (phim)
anguloAvanco = 5 #[VALOR ADICIONADO] 5 <= x <= 12
phim = -(180 + (-180)) + pmd + anguloAvanco
print("Ângulo de fase requerida = ", phim)

#Calculando alpha
alpha = (1-np.sin(np.deg2rad(phim)))/(1+np.sin(np.deg2rad(phim)))
print("Alpha: ", alpha)

#Calculando Beta
beta = 1/alpha
print("Beta = ", beta)

#Definindo Frequênica de Fase (wpm)
wpm = wc
print("Frequência de Fase: ", wpm)

#Definindo Zero Avanço
zeroAvanco = wpm*np.sqrt(alpha)
print("Zero Avanço = ", zeroAvanco)

#Definindo Polo Avanço
poloAvanco = zeroAvanco/alpha
print("Polo Avanco = ", poloAvanco)

#Definindo Zero Atraso
zeroAtraso = 0.1*wpm
print("Zero Atraso = ", zeroAtraso)

#Definindo Polo Atraso
poloAtraso = zeroAtraso/beta
print("Polo Atraso = ", poloAtraso)

#Definindo Função de Transferência do Compensador Gc(s)
numC = np.polymul(np.array([k,k*zeroAtraso]),np.array([1,zeroAvanco]))
denC = np.polymul(np.array([1,poloAtraso]),np.array([1,poloAvanco]))
gc = ml.tf(numC, denC)
print("Função de Transferência do Compensador: ", gc)

#Produto das Funções G(s) e Gc(s)
gIterada = g*gc
print("Função de Transferência Iterada: ", gIterada)
magIt,phaseIt,wIt = ml.bode(gIterada)

#Calculando a Margem de Fase da Função de Transferência Iterada
gmIt,pmIt,wgIt,wpIt = margin(gIterada)
print("Margem de Fase da FT Iterada: ", pmIt)
print("Margem de Fase Desejada: ", pmd)
print("Diferença entre a Margem de Fase Desejada e a Obitida: ", pmd - pmIt)