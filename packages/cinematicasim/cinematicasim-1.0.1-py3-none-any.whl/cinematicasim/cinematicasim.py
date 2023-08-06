#..........importar bibliotecas e definir funçoes opcionais
import os
import time
from vpython import *
def clear(): #..........Define a função para limpar o terminal (linux)
    os.system('clear')
def sleep(x): #.........Define a função para simplificar o sleep da biblioteca time
    time.sleep(x)
def voltar():
    input('\nvoltar ao menu [enter]--->')

#..........................................................subfunções:....................................
#aceleração média:
def a_media(): 
    clear()
    print("\nAceleração média\n")
    v_var = float(input("Variação da velocidade:\n--->"))
    inter_temp = float(input("Intervalo de tempo:\n--->"))
    a_media = v_var / inter_temp
    print(f'Aceleração média = {a_media}')
    voltar()
#Função horária da velocidade:
def v_funcao(): 
    clear()
    print("\nFunção horária da velocidade\n")
    vo = float(input("Velocidade inicial:\n--->"))
    a = float(input("Aceleração\n--->"))
    inter_temp = float(input("Tempo\n--->"))
    v = vo + (a * inter_temp)
    print(f'V = {v}')
    simular = input("[1] para iniciar simulação\n[Enter] para voltar\n--->")
    if simular == '1':
        simulacao_vfuncao(vo,a,inter_temp)
    else:
        return
    voltar()
#Função horária da velocidade vertical:
def v_funcao_vert():
    clear()
    print("\nFunção horária da velocidade no movimento vertical\n")
    vo = float(input("Velocidade inicial:\n--->"))
    t = float(input("Tempo\n--->"))
    v = vo + (9.8 * t)
    print(f'Velocidade = {v}')
    voltar()
#Função horaria da posição em função do tempo no movimento vertical:
def s_funcao_tempo_vert():
    clear()
    print("\nFunção horária da posição em função do tempo no movimento vertical")
    so = float(input("Altura inicial:\n--->"))
    vo = float(input("Velocidade inicial:\n--->"))
    t = float(input("Tempo\n--->"))
    a = 9.8
    s = so + (vo * t) + ((1/2)* a*(t**2))
    print(f'Altura = {s}')
    voltar()
#Função horária da posição em função do tempo
def s_funcao_tempo():
    clear()
    print("\nFunção horária da posição em função do tempo")
    so = float(input("Posição inicial:\n--->"))
    vo = float(input("Velocidade inicial:\n--->"))
    inter_temp = float(input("Tempo\n--->"))
    a = float(input("Aceleração\n--->"))
    s = so + (vo * inter_temp) + ((1/2)* a*(inter_temp**2))
    print(f'Posição = {s}')
    simular = input("[1] para iniciar simulação\n[Enter] para voltar\n--->")
    if simular == '1':
        simulacao_sfuncaotempo(so,vo,inter_temp,a)
    else:
        return
    voltar()
#Função horária da posição em função da posição
def s_funcao_s():
    clear()
    print("\nFunção horária da posição em função da posição")
    s = float(input("Posição final:\n--->"))
    so = float(input("Posição inicial:\n-->"))
    vo = float(input("Velocidade inicial:\n--->"))
    inter_temp = float(input("Tempo\n--->"))
    a = (so + (vo * inter_temp) + ((1/2) * (inter_temp**2))) / s
    print(f'Aceleração= {a}')
    simular = input("[1] para iniciar simulação\n[Enter] para voltar\n--->")
    if simular == '1':
        simulacao_sfuncaoposicao(so,vo,inter_temp,s)
    else:
        return
    voltar()

#equação torricelli:
def torricelli_v():
    clear()
    print("\nTorricelli (v=vo² + 2as)")
    vo = float(input("Velocidade inicial:\n--->"))
    a = float(input("Aceleração\n--->"))
    dist_perc = float(input("Distância percorrida:\n--->"))
    v = pow((vo**2) + 2*a*dist_perc,1/2)
    print(f'V² = {v}')
    simular = input("[1] para iniciar simulação\n[Enter] para voltar\n--->")
    if simular == '1':
        simulacao_torricelliv(vo, a, dist_perc)
    else:
        return
    voltar()
#Torricelli para descobrir aceleração
def torricelli_a():
    clear()
    print("\nTorricelli ( a = (vo² + v²)  / (2s) )")
    vo = float(input("Velocidade inicial:\n--->"))
    v = float(input("Velocidade final\n--->"))
    dist_perc = float(input("Distância percorrida:\n--->"))
    a = ((vo**2) + (v**2))  / (2 * dist_perc)
    print(f'V² = {a}')
    simular = input("[1] para iniciar simulação\n[Enter] para voltar\n--->")
    if simular == '1':
        simulacao_torricellia(vo, v, dist_perc)
    else:
        return
    voltar()
#Torricelli vertical
def torricelli_vert():
    clear()
    print("\nTorricelli no movimento vertical")
    vo = float(input("Velocidade inicial:\n--->"))
    dist_perc = float(input("Distância percorrida:\n--->"))
    a = 9.8
    v = pow((vo**2) + 2*a*dist_perc,1/2)
    print(f'V = {v}')
    voltar()
    
#tempo função da posiçãõ vertical:
def tempo_funcao_s_vert():
    clear()
    print("\nFunção horária do tempo em função da posição no movimento vertical")
    so = float(input("Altura:\n--->"))
    s = 0
    vo = float(input("Velocidade inicial:\n--->"))
    a = 9.8
    inter_temp = vo + pow(((so*2)/a),1/2)
    print(f'Tempo = {inter_temp}')
    voltar()
#tempo função da velocidade vertical:
def tempo_funcao_v_vert():
    clear()
    print("\nFunção horária do tempo em função da posição no movimento vertical")
    s = 0
    vo = float(input("Velocidade inicial:\n--->"))
    v = float(input("Velocidade final:\n--->"))
    a = 9.8
    inter_temp = vo + (v/a)
    print(f'Tempo = {inter_temp}')
    voltar()

#.............................................funções principais:.........................................
#Velocidade média:
def velocidade():
    clear()
    print("\nVelocidade média\n")
    dist_perc = float(input("Distância percorrida:\n--->"))
    inter_temp = float(input("Intervalo de tempo:\n--->"))
    vlcmedia = dist_perc/inter_temp #.......................fórmula velocidade média
    print(f"Velocidade média = {vlcmedia}")
    voltar()
#Movimento uniformemente variado:
def unif_var():
    clear()
    print("\nMovimento uniformemente variado:\n")
    print("\n[1] Aceleração média")
    print("\n[2] Função horária da velocidade")
    print("\n[3] Função horária da posição em função da posiçao")
    print("\n[4] Função horária da posição em função do tempo")
    print("\n[5] Equação de Torricelli (descobrir velocidade)")
    print("\n[6] Equação de Torricelli (descobrir aceleração)")
    unif_var_escolha = int(input('--->'))
    if unif_var_escolha == 1:
        sleep(0.5)
        a_media()
    elif unif_var_escolha == 2:
        sleep(0.5)
        v_funcao()
    elif unif_var_escolha == 3:
        sleep(0.5)
        s_funcao_s()
    elif unif_var_escolha == 4:
        sleep(0.5)
        s_funcao_tempo()
    elif unif_var_escolha == 5:
        sleep(0.5)
        torricelli_v()
    elif unif_var_escolha == 6:
        sleep(0.5)
        torricelli_a()
#Movimento vertical:
def vert():
    clear()
    print("\nMovimento vertical:\n")
    print("\n[1] Função horária da velocidade no movimento vertical")
    print("\n[2] Função horária da posição em função do tempo no movimento vertical")
    print("\n[3] Função horária do tempo em função da posição no movimento vertical")
    print("\n[4] Função horária do tempo em função da velocidade no movimento vertical")
    print("\n[5] Equação de Torricelli no movimento vertical")
    unif_var_escolha = int(input('--->'))
    if unif_var_escolha == 1:
        sleep(0.5)
        v_funcao_vert()
    elif unif_var_escolha == 2:
        sleep(0.5)
        s_funcao_tempo_vert()
    elif unif_var_escolha == 3:
        sleep(0.5)
        tempo_funcao_s_vert()
    elif unif_var_escolha == 4:
        sleep(0.5)
        tempo_funcao_v_vert()
    elif unif_var_escolha == 5:
        sleep(0.5)
        torricelli_vert()
#função horaria do deslocamento:
def s_funcao():
    clear()
    print("\nFunção horária do deslocamento\n")
    so = float(input("Posição inicial:\n--->"))
    v = float(input("Velocidade:\n--->"))
    inter_temp = float(input("Intervalo de tempo:\n--->"))
    s =   so + v * inter_temp#...............função horária do deslocamento
    print(f"S = {s}")
    simular = input("[1] para iniciar simulação\n[Enter] para voltar\n--->")
    if simular == '1':
        simulacao_mru(so,v,inter_temp)
    else:
        return
    voltar()

#......................................simulações movimento retilineo:...............................
def simulacao_mru(so,v,inter_temp):
    #cena:
    scene.background = color.hsv_to_rgb(vector(0.1,0.1,0.2))
    scene.autoscale = False
    scene.append_to_title("<b>Movimento Retilineo Uniforme</b>")
    scene.append_to_caption(f'\tInformações:\n\tVelocidade: {v}\n\tPosição inicial: {so}\n\tIntervalo de tempo: {inter_temp}')
    scene.align = 'left'
    
    obj = sphere(pos=vector(so,0,0),velocidade=vector(v,0,0),color=color.red,make_trail=True,trail_color=color.white)
    texto = label(pos=vector(obj.pos.x,obj.pos.y - 3,0),text=f'S = {obj.pos.x}',color=color.white,opacity=0,box=False)
    textovelocidade = label(text=f'V ={obj.velocidade.x}',color=color.white,opacity=0,box=False)
    
    #trail = curve(color=color.white)
    flecha = arrow(pos=obj.pos,axis=obj.velocidade,color=color.blue,round=True,shaftwidth=0.6)
    dt=0.01
    t=0
    textotempo = label(text=f'{t}',color=color.white,opacity=1,background=color.black,box=False)
    while t <= inter_temp:
        rate(100)
        #objeto:
        obj.pos.x = obj.pos.x + obj.velocidade.x * dt
        #labels:
        texto.pos.x = obj.pos.x #label informando posição
        texto.text = f'S = {obj.pos.x}' #texto da label
        textovelocidade.text = f'V = {obj.velocidade.x}'
        textovelocidade.pos = obj.pos
        textovelocidade.pos.x = obj.pos.x + 2 
        textovelocidade.pos.y = obj.pos.y + 1

        textotempo.text = f'{t:.0f}s'
        #flecha:
        flecha.pos=obj.pos #Flecha do objeto
        flecha.pos.x=obj.pos.x + 0.7
        flecha.axis=obj.velocidade*0.5 #Para onde a flecha aponta
        #cenario camera:
        scene.camera.follow(obj) #cenario
        t=t+dt
        
    sleep(0.5)
    print(f'S = {obj.pos.x} ')

def simulacao_vfuncao(vo,a,inter_temp):
    #cena:
    scene.background = color.hsv_to_rgb(vector(0.1,0.1,0.2))
    scene.autoscale = False
    scene.append_to_title("<b>Função horária da velocidade</b>")
    scene.append_to_caption(f'\tInformações:\n\tVelocidade inicial: {vo}\n\tAceleração: {a}\n\tTempo: {inter_temp}')
    scene.align = 'left'
    
    obj = sphere(pos=vector(0,0,0),velocidade=vector(vo,0,0),aceleracao=vector(a,0,0),color=color.red,make_trail=True,trail_color=color.white)
    
    
    
    flecha = arrow(pos=obj.pos,axis=obj.velocidade,color=color.blue,round=True,shaftwidth=0.2)
    flechaaceleracao = arrow(pos=obj.pos,axis=obj.aceleracao,color=color.yellow,round=True,shaftwidth=0.2)

    textoaceleracao = label(pos=flechaaceleracao.pos,text=f'a = {a}²',color=color.white,opacity=0,box=False)
    textovelocidade = label(text=f'V ={obj.velocidade.x}',color=color.white,opacity=0,box=False)
    dt=0.01
    t=0
    
    while t < inter_temp:
        rate(100)
        obj.velocidade = obj.velocidade + (obj.aceleracao * dt)
        obj.pos = obj.pos + (obj.velocidade * dt) #movimento do objeto
        #labels:

        textoaceleracao.pos.x = flechaaceleracao.pos.x + 5
        textoaceleracao.pos.y = flechaaceleracao.pos.y + 1
        textoaceleracao.text = f'a = {obj.aceleracao.x}²'

        textovelocidade.pos = textoaceleracao.pos
        textovelocidade.pos.y = textoaceleracao.pos.y - 3
        textovelocidade.text = f'V = {obj.velocidade.x}' 
        #flecha:
        flecha.pos=obj.pos
        flecha.pos.x = obj.pos.x + 0.7
        flecha.pos.y=obj.pos.y-0.5
        flecha.axis=obj.velocidade*0.5 #Para onde a flecha aponta
        #flecha da aceleração:
        flechaaceleracao.pos=obj.pos
        flechaaceleracao.pos.x = obj.pos.x + 0.7
        flechaaceleracao.pos.y=obj.pos.y + 0.5
        flechaaceleracao.axis=obj.aceleracao*1
        scene.camera.follow(obj) #cenario
        t=t+dt
        
    sleep(0.5)
    print(f'v = {obj.velocidade.x} ')

def simulacao_sfuncaotempo(so,vo,inter_temp,a):
    #cena:
    scene.background = color.hsv_to_rgb(vector(0.1,0.1,0.2))
    scene.autoscale = False
    scene.append_to_title("<b>Função horária da posição em função do tempo</b>")
    scene.append_to_caption(f'\tInformações:\n\tPosição inicial: {so}\n\tVelocidade inicial: {vo}\n\tAceleração: {a}\n\tTempo: {inter_temp}\n\t')
    scene.align = 'left'
    
    obj = sphere(pos=vector(so,0,0),velocidade=vector(vo,0,0),aceleracao=vector(a,0,0),color=color.red,make_trail=True,trail_color=color.white)
    
    
    
    flecha = arrow(pos=obj.pos,axis=obj.velocidade,color=color.blue,round=True,shaftwidth=0.2)
    flechaaceleracao = arrow(pos=obj.pos,axis=obj.aceleracao,color=color.yellow,round=True,shaftwidth=0.2)

    texto = label(pos=vector(obj.pos.x,obj.pos.y - 3,0),text=f'S = {obj.pos.x}',color=color.white,opacity=0,box=False)
    textoaceleracao = label(pos=flechaaceleracao.pos,text=f'a = {a}²',color=color.white,opacity=0,box=False)
    textovelocidade = label(text=f'V ={obj.velocidade.x}',color=color.white,opacity=0,box=False)
    dt=0.01
    t=0
    
    while t < inter_temp:
        rate(100)
        obj.velocidade = obj.velocidade + (obj.aceleracao * dt)
        obj.pos = obj.pos + (obj.velocidade * dt) #movimento do objeto
        #labels:
        texto.pos.x = obj.pos.x # posição da label informando
        texto.text = f'S = {obj.pos.x}' #texto da label

        textoaceleracao.pos.x = flechaaceleracao.pos.x + 5
        textoaceleracao.pos.y = flechaaceleracao.pos.y + 1
        textoaceleracao.text = f'a = {obj.aceleracao.x}²'

        textovelocidade.pos = textoaceleracao.pos
        textovelocidade.pos.y = textoaceleracao.pos.y - 3
        textovelocidade.text = f'V = {obj.velocidade.x}' 
        #flecha:
        flecha.pos=obj.pos
        flecha.pos.x = obj.pos.x + 0.7
        flecha.pos.y=obj.pos.y-0.5
        flecha.axis=obj.velocidade*0.5 #Para onde a flecha aponta
        #flecha da aceleração:
        flechaaceleracao.pos=obj.pos
        flechaaceleracao.pos.x = obj.pos.x + 0.7
        flechaaceleracao.pos.y=obj.pos.y + 0.5
        flechaaceleracao.axis=obj.aceleracao*1
        scene.camera.follow(obj) #cenario
        t=t+dt
        
    sleep(0.5)
    print(f'v = {obj.velocidade.x} ')

def simulacao_sfuncaoposicao(so,vo,inter_temp,s):
    a = (so + (vo * inter_temp) + ((1/2) * (inter_temp**2))) / s
    #cena:
    scene.background = color.hsv_to_rgb(vector(0.1,0.1,0.2))
    scene.autoscale = False
    scene.append_to_title("<b>Função horária da posição em função da posição</b>")
    scene.append_to_caption(f'\tInformações:\n\tPosição inicial: {so}\n\tVelocidade inicial: {vo}\n\tPosição final: {s}\n\tTempo: {inter_temp}\n\t')
    scene.align = 'left'
    
    obj = sphere(pos=vector(so,0,0),velocidade=vector(vo,0,0),aceleracao=vector(a,0,0),color=color.red,make_trail=True,trail_color=color.white)
    
    flecha = arrow(pos=obj.pos,axis=obj.velocidade,color=color.blue,round=True,shaftwidth=0.2)
    flechaaceleracao = arrow(pos=obj.pos,axis=obj.aceleracao,color=color.yellow,round=True,shaftwidth=0.2)

    texto = label(pos=vector(obj.pos.x,obj.pos.y - 3,0),text=f'S = {obj.pos.x}',color=color.white,opacity=0,box=False)
    textoaceleracao = label(pos=flechaaceleracao.pos,text=f'a = {a}²',color=color.white,opacity=0,box=False)
    textovelocidade = label(text=f'V ={obj.velocidade.x}',color=color.white,opacity=0,box=False)
    dt=0.01
    t=0
    
    while obj.pos.x <= s:
        rate(100)
        obj.velocidade = obj.velocidade + (obj.aceleracao * dt)
        obj.pos = obj.pos + (obj.velocidade * dt) #movimento do objeto
        #labels:
        texto.pos.x = obj.pos.x # posição da label informando
        texto.text = f'S = {obj.pos.x}' #texto da label

        textoaceleracao.pos.x = flechaaceleracao.pos.x + 5
        textoaceleracao.pos.y = flechaaceleracao.pos.y + 1
        textoaceleracao.text = f'a = {obj.aceleracao.x}²'

        textovelocidade.pos = textoaceleracao.pos
        textovelocidade.pos.y = textoaceleracao.pos.y - 3
        textovelocidade.text = f'V = {obj.velocidade.x}' 
        #flecha:
        flecha.pos=obj.pos
        flecha.pos.x = obj.pos.x + 0.7
        flecha.pos.y=obj.pos.y-0.5
        flecha.axis=obj.velocidade*0.5 #Para onde a flecha aponta
        #flecha da aceleração:
        flechaaceleracao.pos=obj.pos
        flechaaceleracao.pos.x = obj.pos.x + 0.7
        flechaaceleracao.pos.y=obj.pos.y + 0.5
        flechaaceleracao.axis=obj.aceleracao*1
        scene.camera.follow(obj) #cenario
        t=t+dt
        
    sleep(0.5)
    print(f'a = {obj.aceleracao.x} ')

def simulacao_torricelliv(vo,a,dist_perc):
    #cena:
    scene.background = color.hsv_to_rgb(vector(0.1,0.1,0.2))
    scene.autoscale = False
    scene.append_to_title("<b>Torricelli</b>")
    scene.append_to_caption(f'\tInformações:\n\tVelocidade inicial: {vo}\n\tAceleração: {a}\n\tDistância: {dist_perc}\n\t')
    scene.align = 'left'
    
    obj = sphere(pos=vector(0,0,0),velocidade=vector(vo,0,0),aceleracao=vector(a,0,0),color=color.red,make_trail=True,trail_color=color.white)
    
    
    
    flecha = arrow(pos=obj.pos,axis=obj.velocidade,color=color.blue,round=True,shaftwidth=0.2)
    flechaaceleracao = arrow(pos=obj.pos,axis=obj.aceleracao,color=color.yellow,round=True,shaftwidth=0.2)

    texto = label(pos=vector(obj.pos.x,obj.pos.y - 3,0),text=f'S = {obj.pos.x}',color=color.white,opacity=0,box=False)
    textoaceleracao = label(pos=flechaaceleracao.pos,text=f'a = {a}²',color=color.white,opacity=0,box=False)
    textovelocidade = label(text=f'V ={obj.velocidade.x}',color=color.white,opacity=0,box=False)
    dt=0.01
    t=0
    
    while obj.pos.x <= dist_perc:
        rate(100)
        obj.velocidade = obj.velocidade + (obj.aceleracao * dt)
        obj.pos = obj.pos + (obj.velocidade * dt) #movimento do objeto
        #labels:
        texto.pos.x = obj.pos.x # posição da label informando
        texto.text = f'S = {obj.pos.x}' #texto da label

        textoaceleracao.pos.x = flechaaceleracao.pos.x + 5
        textoaceleracao.pos.y = flechaaceleracao.pos.y + 1
        textoaceleracao.text = f'a = {obj.aceleracao.x}²'

        textovelocidade.pos = textoaceleracao.pos
        textovelocidade.pos.y = textoaceleracao.pos.y - 3
        textovelocidade.text = f'V = {obj.velocidade.x}' 
        #flecha:
        flecha.pos=obj.pos
        flecha.pos.x = obj.pos.x + 0.7
        flecha.pos.y=obj.pos.y-0.5
        flecha.axis=obj.velocidade*0.5 #Para onde a flecha aponta
        #flecha da aceleração:
        flechaaceleracao.pos=obj.pos
        flechaaceleracao.pos.x = obj.pos.x + 0.7
        flechaaceleracao.pos.y=obj.pos.y + 0.5
        flechaaceleracao.axis=obj.aceleracao*1
        scene.camera.follow(obj) #cenario
        t=t+dt
        
    sleep(0.5)
    print(f'v = {obj.velocidade.x} ')

def simulacao_torricellia(vo,v,dist_perc):
    #cena:
    scene.background = color.hsv_to_rgb(vector(0.1,0.1,0.2))
    scene.autoscale = False
    scene.append_to_title("<b>Torricelli</b>")
    scene.append_to_caption(f'\tInformações:\n\tVelocidade inicial: {vo}\n\tVelocidade final: {v}\n\tDistância: {dist_perc}\n\t')
    scene.align = 'left'
    a = ((vo**2) + (v**2))  / (2 * dist_perc)
    obj = sphere(pos=vector(0,0,0),velocidade=vector(vo,0,0),aceleracao=vector(a,0,0),color=color.red,make_trail=True,trail_color=color.white)
    
    
    
    flecha = arrow(pos=obj.pos,axis=obj.velocidade,color=color.blue,round=True,shaftwidth=0.2)
    flechaaceleracao = arrow(pos=obj.pos,axis=obj.aceleracao,color=color.yellow,round=True,shaftwidth=0.2)

    texto = label(pos=vector(obj.pos.x,obj.pos.y - 3,0),text=f'S = {obj.pos.x}',color=color.white,opacity=0,box=False)
    textoaceleracao = label(pos=flechaaceleracao.pos,text=f'a = {a}²',color=color.white,opacity=0,box=False)
    textovelocidade = label(text=f'V ={obj.velocidade.x}',color=color.white,opacity=0,box=False)
    dt=0.01
    t=0
    
    while obj.velocidade.x < v:
        rate(100)
        obj.velocidade = obj.velocidade + (obj.aceleracao * dt)
        obj.pos = obj.pos + (obj.velocidade * dt) #movimento do objeto
        #labels:
        texto.pos.x = obj.pos.x # posição da label informando
        texto.text = f'S = {obj.pos.x}' #texto da label

        textoaceleracao.pos.x = flechaaceleracao.pos.x + 5
        textoaceleracao.pos.y = flechaaceleracao.pos.y + 1
        textoaceleracao.text = f'a = {obj.aceleracao.x}²'

        textovelocidade.pos = textoaceleracao.pos
        textovelocidade.pos.y = textoaceleracao.pos.y - 3
        textovelocidade.text = f'V = {obj.velocidade.x}' 
        #flecha:
        flecha.pos=obj.pos
        flecha.pos.x = obj.pos.x + 0.7
        flecha.pos.y=obj.pos.y-0.5
        flecha.axis=obj.velocidade*0.5 #Para onde a flecha aponta
        #flecha da aceleração:
        flechaaceleracao.pos=obj.pos
        flechaaceleracao.pos.x = obj.pos.x + 0.7
        flechaaceleracao.pos.y=obj.pos.y + 0.5
        flechaaceleracao.axis=obj.aceleracao*1
        scene.camera.follow(obj) #cenario
        t=t+dt
        
    sleep(0.5)
    print(f'v = {obj.velocidade.x} ')

menuprincipal = 20
while menuprincipal != 0:
    clear()
    print("\nbem vindo")
    print("[0] Sair do script")
    print("\nCinemática: \n")
    print("\n[1] Velocidade média")
    print("\n[2] Movimento uniforme (função horária do deslocamento)")
    print("\n[3] Movimento uniformemente variado")
    print("\n[4] Movimento vertical")
    print("\n[5] Lançamento Oblíquo")
    menuprincipal = int(input('--->'))
    
    if menuprincipal == 1: #.........................velocidade media
        print(f'Você selecionou [{menuprincipal}]')
        sleep(0.5)
        velocidade()
    elif menuprincipal == 2: #......................função horaria do deslocamento
        print(f'Você selecionou [{menuprincipal}]')
        sleep(0.5)
        s_funcao()
    elif menuprincipal == 3: #........................movimento uniformemente variado
        print(f'Você selecionou [{menuprincipal}]')
        sleep(0.5)
        unif_var()
    elif menuprincipal == 4: #........................movimento vertical
        print(f'Você selecionou [{menuprincipal}]')
        sleep(0.5)
        vert()
    elif menuprincipal == 5:#.......................lançamento obliquo
        print(f'Você selecionou [{menuprincipal}]')
        sleep(0.5)
        #oblq()
    elif menuprincipal == 6:#.......................lançamento obliquo
        print(f'Você selecionou [{menuprincipal}]')
        simulacao()
    rate(60)
