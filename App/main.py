#import
import pygame
import math
import serial
import pyautogui

#pygame init
pygame.init()
run=True
#window size
screen= pygame.display.set_mode((600,900))

#window title
try:
    pygame.display.set_caption('GameGlove')
    pygame.display.set_icon(pygame.image.load('assets/icon.png'))
    info=pygame.image.load('assets/info.png')
    on_button = pygame.image.load('assets/on.png')
    off_button = pygame.image.load('assets/off.png')
    theme_=pygame.image.load('assets/theme.png')
    connect_=pygame.image.load('assets/connect.png')
    connected_=pygame.image.load('assets/connected.png')
    #loading user saved data

    file=open('assets/state_data.txt','r')
    data=str(file.read()).split('\n')

    forward = data[0]
    backward =data[1]
    left = data[2]
    right = data[3]
    index = data[4]
    forward_left = data[5]
    forward_right = data[6]
    backward_left = data[7]
    backward_right = data[8]
except:
        print('You deleted the important files from assets')
        run=False

name=''

ip_screen='yes'
screen_1='no'
screen_2='no'

def write(txt,size,px,py,FONT=None):
    try:
        playfair=pygame.font.Font('assets/playfair.ttf',size)
        cream=pygame.font.Font('assets/cream.ttf',size)
    except:
        print('You deleted the important files from assets')
        run=False
    if FONT=='cream':
        screen.blit(cream.render(txt,True,(250,250,250)),(px,py))
    else:
        screen.blit(playfair.render(txt,True,(250,250,250)),(px,py))

#function for blit
def blitting(imag,posx,posy):
    screen.blit(imag,(posx,posy))

#check if click on
def check(mx,yx,r):
    x,y=pygame.mouse.get_pos()
    sqx = (x - (mx+r))**2
    sqy = (y - (yx+r))**2

    if math.sqrt(sqx + sqy) < r:
        return 'yes'
    return None


def SCREEN_1():
    global screen_1
    global screen_2
    global main_state
   
    global speak_off
    
    #main button
    if main_state=='on':
        blitting(on_button,140,40)
        write('GameGlove : ON',32,130,0)
    elif main_state=='off':
        blitting(off_button,140,40)
        write('Main: OFF',32,130,0)

    #info button
    blitting(info,355,5)

    



def SCREEN_2():
    blitting(back,355,5)
    write('Home Assistant',32,80,90)
    write('This is a home devices controller ',22,30,140,'cream')
    write('controlled using GUI inputs.',22,30,165,'cream')

    write('Note: ',26,30,400)
    write('Do not delete any files in ',22,30,435,'cream')
    write('assets folder',22,30,460,'cream')

    

def save_data():
    file=open('assets/state_data.txt','w')
    file.write(main_state+'\n'+button1_state+'\n'+button2_state+'\n'+button3_state+'\n'+button4_state+'\n'+speak_off)
    file.close()

def input_ip():
    global ip_screen
    global name
    global screen_1
    if ip_screen=='yes':
        if len(name)<15:
            name += event.unicode
    
        if event.key == pygame.K_BACKSPACE:
            name=name[:-1]
    
        elif event.key == pygame.K_RETURN:
            ip_screen='no'
            screen_1='yes'
            return
        
def events_1():
    global screen_1
    global screen_2
    global main_state
    if check(140,40,58)=='yes':
        if main_state=='off':
            if screen_1=='yes' and speak_off=='no':
                on_sound.play()
            main_state='on'
        elif main_state=='on':
            if speak_off=='no':
                off_sound.play()

            #switching of all the buttons
            main_state='off'
            button1_state='off'
            threading.Thread(target=send_url,args=('l1off',)).start()
            button2_state='off'
            threading.Thread(target=send_url,args=('fanoff',)).start()
            button3_state='off'
            threading.Thread(target=send_url,args=('l2off',)).start()
            button4_state='off'
            threading.Thread(target=send_url,args=('spoff',)).start()

    #button 1
    if check(30,220,58)=='yes':
        if main_state=='on':
            if button1_state=='off':
                if speak_off=='no':
                    on_sound.play()
                button1_state='on'
                threading.Thread(target=send_url,args=('l1on',)).start()
            elif button1_state=='on':
                if screen_1=='yes' and speak_off=='no':
                    off_sound.play()
                button1_state='off'
                threading.Thread(target=send_url,args=('l1off',)).start()

    #button 2
    if check(250,220,58)=='yes':
        if main_state=='on':
            if button2_state=='off':
                if speak_off=='no':
                    on_sound.play()
                button2_state='on'
                threading.Thread(target=send_url,args=('fanon',)).start()
            elif button2_state=='on':
                if screen_1=='yes' and speak_off=='no':
                    off_sound.play()
                button2_state='off'
                threading.Thread(target=send_url,args=('fanoff',)).start()
            
    #button 3
    if check(30,420,58)=='yes':
        if main_state=='on':
            if button3_state=='off':
                if speak_off=='no':
                    on_sound.play()
                button3_state='on'
                threading.Thread(target=send_url,args=('l2on',)).start()
            elif button3_state=='on':
                if screen_1=='yes' and speak_off=='no':
                    off_sound.play()
                button3_state='off'
                threading.Thread(target=send_url,args=('l2off',)).start()

    #button 4
    if check(250,420,58)=='yes':
        if main_state=='on':
            if button4_state=='off':
                if speak_off=='no':
                    on_sound.play()
                button4_state='on'
                threading.Thread(target=send_url,args=('spon',)).start()
            elif button4_state=='on':
                if screen_1=='yes' and speak_off=='no':
                    off_sound.play()
                button4_state='off'
                threading.Thread(target=send_url,args=('spoff',)).start()
    
    #info buttons    
    if check(355,5,20)=='yes':
        screen_2='yes'
        screen_1='no'
        screen_3='no'
        if speak_off=='no':
            click_sound.play()
        
    #sound button
    if check(355,55,20)=='yes':
        if speak_off=='yes':
            click_sound.play()
        if speak_off=='yes':
            speak_off='no'
        elif speak_off=='no':
            speak_off='yes'
            
    if check(355,105,20)=='yes':
        if speak_off=='no':
            click_sound.play()
        screen_1='no'
        screen_2='no'

    #change button
    if check(20,550,20)=='yes':
        if speak_off=='no':
            click_sound.play()
        ip_screen='yes'
        screen_1='no'
        screen_2='no'
    


def events_2():
    global speak_off
    global screen_2
    global screen_1
    global ip_screen
    if check(355,5,20)=='yes':
        screen_2='no'
        screen_1='yes'
        if speak_off=='no':
            click_sound.play()
        

# Main loop  
while run:
    screen.fill((255,255,255))
    blitting(theme_,0,0)

    if ip_screen=='yes':
        ip_welcome()
        
    elif screen_1=='yes':
        SCREEN_1()
        
    elif screen_2=='yes':
        SCREEN_2()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_data()
            run=False

        if event.type == pygame.KEYDOWN:
            input_ip()
                    
        elif event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                if screen_1=='yes':
                    events_1()
                    
            
                elif screen_2=='yes':
                    events_2()

    pygame.display.update()

pygame.quit()
