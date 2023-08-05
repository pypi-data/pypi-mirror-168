#!/usr/bin/env
#-*- coding: UTF-8 -*-

with open('.\ikun\\version.txt','r') as f1:version  =  f1.readline()
password_for_all='114514'
build_version  =  '10.7.1.19920'
mins=[0,0,0,0,0,0]
with open('.\ikun\\Password_for_Boss.txt','r') as f1:Password_for_Boss=f1.readline()# give "Password_for_Boss"
import sys,gc,datetime,webbrowser,random,os
import calendar as cal
import time as t
import turtle as t1
# import some modules

base_path='./'
file_name=base_path

# 测量文件的路径与大小
def file_count(file_dir):
    """

    # file count
    
    """
    count = 0
    for root, dirs, files in os.walk(file_dir):
        count += len(files)
    return count
def file_size(file_dir):
    """

    # file size

    """
    size = 0
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            size+=os.path.getsize(os.path.join(root, file))
    return size
# 在指定目录下统计所有的py文件，以列表形式返回
def collect_files(dir):
    filelist = []
    for parent,dirnames,filenames in os.walk(dir):
         for filename in filenames:
             if filename.endswith('.py'):
                 # 将文件名和目录名拼成绝对路径，添加到列表里
                 filelist.append(os.path.join(parent,filename))
    return filelist
# 计算单个文件内的代码行数
def calc_linenum(file):
    with open(file,encoding='UTF-8') as fp:
        content_list = fp.readlines()
        code_num = 0  # 当前文件代码行数计数变量
        blank_num = 0  # 当前文件空行数计数变量
        annotate_num =0  # 当前文件注释行数计数变量
        for content in content_list:
            content = content.strip()
            # 统计空行
            if content == '':
                blank_num += 1
            # 统计注释行
            elif content.startswith('#'):
                annotate_num += 1
            # 统计代码行
            else:
                code_num += 1
    # 返回代码行数，空行数，注释行数
    return code_num,blank_num,annotate_num
def file(qwe):
    files = collect_files(base_path)
    total_code_num = 0   # 统计文件代码行数计数变量
    total_blank_num = 0   # 统计文件空行数计数变量
    total_annotate_num = 0  # 统计文件注释行数计数变量
    for f in files:
        code_num, blank_num, annotate_num = calc_linenum(f)
        total_code_num += code_num
        total_blank_num += blank_num
        total_annotate_num += annotate_num

    print(u'代码总行数为：  %s' % total_code_num);print(u'空行总行数为：  %s' % total_blank_num);print(u'注释行总行数为： %s' % total_annotate_num)
    a12345=file_count(file_name)
    a09876=file_size(file_name)
    for root,dirs,files in os.walk(base_path):
        print(root)
        print(dirs)
        print(files,'\n')
    print('files:',a12345)
    print('large(MB)',(a09876)/1024/1024)
def Print_feigao_jiuban(qwe):
    nb='''

    .__  .__       .__                                                        
    |  | |__| ____ |  |__   ____   ____    ____   ____   ____   ____    ____  
    |  | |  |/ ___\|  |  \_/ __ \ /    \  / ___\ / ___\ /  _ \ /    \  / ___\ 
    |  |_|  \  \___|   Y  \  ___/|   |  \/ /_/  > /_/  >  <_> )   |  \/ /_/  >
    |____/__|\___  >___|  /\___  >___|  /\___  /\___  / \____/|___|  /\___  / 
                 \/     \/     \/     \//_____//_____/             \//_____/ 

    '''
    print(nb)
def Print_xinban_morden(qwe):
    nb='''

    .__  .__      .__                                                        
    ||`| |``/     ||`|
    |\-| |/` .___ | -|__  .___  .____   .____  .____  |___| .____   .____
    | ||.|_-|/`__\||/```\ /`__\ /`  `\  /`__`\ /`__`\ /` `\ /`  `\  /`__`\ 
    | ||/`.-T \___|`-Y `|T `__///  +  \///_/ `> /_/ `> (*) //  +  \///_/ `>
    |____/_ |\__``>__/` //\__``>__/` //\___.//\___.// \___/\__/` //\___.// 
           \/   \/     \/    \/    `\//_____//_____/  |` `|    `\//_____/ 

    '''
    print(nb)
def xiugay(qwe):
    try:
        def tailand(haaasfsa):
            t1.color('red','yellow')
            t1.hideturtle()
            t1.speed(35)
            t1.goto(-100,-10)
            t1.begin_fill()
            for i in range(50):
                t1.forward(200)
                t1.left(170)
            t1.end_fill()
        def LMX(x,y,d):
            t1.penup()
            t1.goto(x, y)
            t1.pendown()
            t1.seth(60)
            for i in range(3):
                t1.fd(d)
                t1.left(120)
            t1.pu()
            t1.goto(x, -y)
            t1.pd()
            t1.seth(-60)
            for i in range(3):
                t1.fd(d)
                t1.right(120)
                t1.hideturtle()
        def yuan(r):
            t1.pu()
            t1.goto(-r*pow(3,0.5)/2, -r/2)
            t1.pd()
            t1.circle(r)
            t1.hideturtle()
        def sixy(x,y,r):
            def txyuan(x,y,r):
                t1.seth(0)
                y-=r
                t1.pu()
                t1.goto(x, y)
                t1.pd()
                t1.pensize(2)
                t1.circle(r)
                t1.pu()
                t1.goto(x, y+3)
                t1.pd()
                r-=3
                y-=r
                t1.circle(r)
            t1.color("#5daed9") 
            txyuan(x,y,r)
            txyuan(-x,y,r)
            txyuan(-x,-y,r)
            txyuan(x,-y,r)
            txyuan(175,0,r)
            txyuan(-175,0,r)
            t1.hideturtle()
        def lbx(x,y):
            t1.penup()
            t1.goto(x, y)
            t1.pendown()
            for i in range(6):
                t1.fd(180)
                t1.left(60)
            t1.hideturtle()
        def yue(x,y,r):
            y-=r
            t1.penup()
            t1.goto(x,y)
            t1.pendown() 
            t1.circle(r)
            t1.circle(r-10)
            t1.hideturtle()
        def xingzuo(r,c,h):
            t1.penup()
            t1.pencolor("#fdcfad")
            t1.goto(-10,-10)
            t1.seth(-45)
            t1.fd(r)
            t1.pendown()
            xz=['♒','♓','♈','♉','♌','♍','♎','♏','♊','♋','♐','♑']
            for i in range(12):
                t1.write(xz[(i+h)%12],font=("", c, ""))
                t1.penup()
                t1.right(90)
                t1.circle(-r, 30)
                t1.left(90)
                t1.pendown()
            t1.hideturtle()
        def xingdui(r):
            for i in range(1,5):
                te=3;t1.penup();t1.goto(0,0);t1.seth(i*90);t1.pendown();t1.right(22.5);t1.fd(r)
                if i==1:
                    t1.goto(0,3*r-3);t1.goto(0,0);t1.seth(i * 90 + 22.5);t1.fd(r);t1.goto(0,3*r-3)
                elif i==2:
                    t1.goto(-3*r+3,0);t1.goto(0,0);t1.seth(i*90+22.5);t1.fd(r);t1.goto(-3*r+3,0)
                elif i==3:
                    t1.goto(0,-3*r+3);t1.goto(0,0);t1.seth(i*90+22.5);t1.fd(r);t1.goto(0,-3*r+3)
                else:
                    t1.goto(3*r+3,0);t1.goto(0,0);t1.seth(i*90+22.5);t1.fd(r);t1.goto(3*r+3,0)
                t1.hideturtle()
            x=pow(((2*r)**2)/2,0.5)-8
            for i in range(1,5):
                t1.pu();t1.goto(0,0);t1.seth(i*90);t1.pendown();t1.right(22.5);t1.fd(r)
                if i==1:
                    t1.goto(x,x);t1.goto(0,0);t1.right(45);t1.fd(r);t1.goto(x,x)
                elif i==2:
                    t1.goto(-x,x);t1.goto(0, 0);t1.right(45);t1.fd(r);t1.goto(-x,x)
                elif i==3:
                    t1.goto(-x,-x);t1.goto(0,0);t1.right(45);t1.fd(r);t1.goto(-x,-x)
                else:
                    t1.goto(x,-x);t1.goto(0,0);t1.right(45);t1.fd(r);t1.goto(x,-x)
                t1.hideturtle()
        def lx(rd,l,q,j):
            def Skip(step):
                t1.pu()
                t1.fd(step)
                t1.pd()
            CLA=['yellow','#7ecff1','black']
            for a in range(l):
                t1.pu()
                t1.goto(0,0)
                t1.pendown()
                degree=-360/l*a+q
                t1.seth(degree)
                Skip(rd)
                t1.begin_fill()
                t1.fillcolor(CLA[j])
                t1.pencolor(CLA[j])
                t1.right(30)
                t1.fd(25)        
                LZ=[60,120,60]
                for i in range(3):
                    t1.left(LZ[i])
                    t1.fd(25)
                t1.end_fill()
            t1.hideturtle()
        def stars(m):
            CLQ=['yellow','#7ecff1']
            for i in range(m):
                a=random.uniform(-m*2,m*2)
                b=random.uniform(-m*2,m*2)
                t1.begin_fill()
                t1.penup()
                t1.goto(a,b)
                t1.pendown()
                t1.speed(900)
                t1.fillcolor(CLQ[m%2])
                t1.pencolor(CLQ[m%2])
                t1.circle(m/200)
                t1.end_fill()
                t1.hideturtle()
        def xinghei(qwe):
            for _ in range(500):
                t1.color(random.choice([(0,0,0),(1,1,1)]))
                ext=random.random() * 90
                t1.circle(r, ext)
                acc_ext+=ext
                if acc_ext>360:
                  acc_ext=0
                  r+=3
                  t1.pu()
                  t1.goto(0,-r)
                  t1.seth(0)
                  t1.pd()
        #初始化
        colorslan=["black",
                   "#7ecff1",
                   ["#0489D4","#d9f1f1"],
                   ["#6cd1ef","#d9f1f1"],
                   ["#94d5f0","#acdefa"],
                   "#389bc8",
                   ["#54B6D8","#f0efeb"],
                   "#5daed9",
                   [-150,30,300,120],
                   ['#7ecff1','yellow','#7ecff1','yellow'],
                   "blue"]
        t1.setup(1,1,0,0)
        t1.bgcolor(colorslan[0])
        t1.pencolor(colorslan[1])
        t1.hideturtle()
        for i in range(2):
            t1.speed(1)
            t1.delay(0)
            t1.pensize(2-i*1.2)
            t1.color(colorslan[2][i]) 
            LMX(0,-70,122.5)
            LMX(0,-100,175)
            t1.pensize(3-i*1.6)
            t1.color(colorslan[3][i]) 
            LMX(0,-200,350)
            LMX(0,-220,385)
        for i in range(2):
            t1.speed(13)
            t1.pensize(3-i*1.5)
            t1.pencolor(colorslan[4][i])
            yuan(220+i)
            yuan(250+i)
            yuan(258+i)
            t1.pensize(1)
            t1.pencolor(colorslan[5])
            t1.speed(6)
            yuan(100+i)
            yuan(110+i)
            yuan(35+i)
            yuan(30+i)
        t.sleep(0.5)
        t1.speed(5)
        sixy(86,155,40)
        t1.speed(10)
        for i in range(2):
            t1.speed(5)
            t1.delay(0)
            t1.color(colorslan[6][i])
            t1.pensize(3-i*1.6)
            t1.seth(-12)
            lbx(-123,-135.88)
            t1.seth(0)
            lbx(-90,-155.88)
            t1.seth(12)
            lbx(-57,-175.88)
        t1.speed(10)
        t1.pencolor(colorslan[7])
        t1.pensize(1.3)
        for i in range(4):
            t1.seth(colorslan[8][i])
            yue(0,53,50)
        t1.delay(0)
        t1.pu()
        t1.goto(-400, 20)
        t1.pd()
        xingzuo(235,15,0)
        for i in range(2):
            t1.pensize(10-7.7*i)
            t1.speed(12)
            t1.pu()
            t1.goto(0, -254+i*34)
            t1.pd() 
            t1.pencolor(colorslan[0])
            t1.seth(0)
            t1.circle(254-i*34)
        t.sleep(2)
        t1.speed(35)
        for i in range(15):
            t1.pu()
            t1.goto(0,-240-i*4.5)
            t1.pd()
            t1.pencolor(colorslan[0])
            t1.pensize(35)
            t1.seth(0)
            t1.circle(240+i*4.5)
            xingzuo(240+i*4.5,17,i)
        t.sleep(1.5)
        t1.speed(15)
        t1.pencolor(colorslan[9][1])
        t1.pensize(0.7)
        xingdui(30)
        t.sleep(2)
        t1.reset()
        j=0
        for i in range(30,91,20):
            t1.delay(0)
            t1.pensize(0.1*(i-20)/10+0.7)
            t1.pencolor(colorslan[9][j])
            t1.speed(30)
            xingdui(i)
            t.sleep(1)
            j=j+1
            t1.reset()
        j=0
        t1.pencolor(colorslan[9][1])
        t1.pensize(1.4)
        t1.speed(30)
        xingdui(90)
        t1.speed(50)
        t1.delay(0)
        lx(280,8,0,0)
        t.sleep(1)
        lx(340,24,0,1)
        t.sleep(1)
        lx(400,8,0,0)
        t.sleep(1.5)
        lx(280,8,0,2)
        lx(340,24,0,2)
        lx(400,8,0,2)
        t.sleep(0.75)
        for i in range(3):
            t1.speed(150+i*100)
            t1.delay(0)
            lx(380+i*150,12,0,1)
            lx(380+i*150,6,0,0)
        t1.speed(20)
        stars(51)
        stars(100)
        stars(301)
        t1.pu()
        t1.home()
        t1.pd()
        tailand(114514)
        t1.home()
        t1.pencolor(colorslan[10])
        t1.speed(100)
        t1.hideturtle()
        for i in range(92):
            t1.forward(i)
            t1.left(91)
        t1.ht()
        t1.speed(0) 
        t1.pensize(2)
        t1.color(1,1,1)
        r=10
        t1.pu()
        t1.goto(0,-r)
        t1.pd()
        acc_ext=0
        xinghei(1)
        t1.home()
        t1.pencolor('blue')
        t1.write('OK!',align="center",font=("宋体",20,"normal"))
        t.sleep(3)
        t1.reset()
    except t1.Terminator:
        print('emm!',end='');print('你好像很心急');print('it seems that you are want to quicker');print('OK')
def sqrt(m):
    x0=m/2 #初始点，也可以是别的值
    x1=x0/2 + m/(x0*2)
    while abs(x1-x0)>1e-5:
        x0=x1;x1=x0/2 + m/(x0*2)
def CN_fanti_print(qwe):
    print('你幹甚麽')
def CN_print(qwe):
    print('宁干甚么')
def US_print(qwe):
    print('What do you want to do ?')
def filem(qwe):
    file_name=r'./'
    m1="▫"
    m2="▪"
    m3=0
    scale = 50
    start = t.perf_counter()
    
    for i in range(scale + 1):
        m4=m3%10
        m3+=1
        if m4==0:m5=m2+m2+m1+m1+m1+m1+m1+m1+m1+m1
        if m4==1:m5=m1+m2+m2+m1+m1+m1+m1+m1+m1+m1
        if m4==2:m5=m1+m1+m2+m2+m1+m1+m1+m1+m1+m1
        if m4==3:m5=m1+m1+m1+m2+m2+m1+m1+m1+m1+m1
        if m4==4:m5=m1+m1+m1+m1+m2+m2+m1+m1+m1+m1
        if m4==5:m5=m1+m1+m1+m1+m1+m2+m2+m1+m1+m1
        if m4==6:m5=m1+m1+m1+m1+m1+m1+m2+m2+m1+m1
        if m4==7:m5=m1+m1+m1+m1+m1+m1+m1+m2+m2+m1
        if m4==8:m5=m1+m1+m1+m1+m1+m1+m1+m1+m2+m2
        if m4==9:m5=m2+m1+m1+m1+m1+m1+m1+m1+m1+m2
        a = "|" * i
        b = "-" * (scale - i)
        c = (i / scale) * 100
        dur = t.perf_counter() - start
        print("\rLoading {:^3.0f}%[{}{}]{:.2f}s {}".format(c,a,b,dur,m5))
    print()
    print()
    print()
    file(1)
    del m1,m2,m3,m4,m5,i,scale,start,dur,a,b,c
    gc.collect()
    Print_xinban_morden(1)
    print('Welcome!')
def CN_fanti_allthing(qwe):
    global password_for_all
    global Password_for_Boss
    filem(1)
    global mins
    for i in range(6):
        a=random.randint(0,9)
        mins[i]=a
    minss=str(mins[0])+\
           str(mins[1])+\
           str(mins[2])+\
           str(mins[3])+\
           str(mins[4])+\
           str(mins[5])
    print('此處是驗證碼',minss,end=" ")
    ea=input('親輸入驗證碼:')
    if minss=='114514':
        print('哼哼哼哈哈哈哈哈哈哈哈~~~~~~~~~~')
        ea=minss
    if ea=='114514' or ea=='1919810':
        ea=minss
        print('好吧,勉強讓你過')
    while ea!=minss:
        print('驗證碼驗證失敗，請重試')
        for i in range(6):
            a=random.randint(0,9)
            mins[i]=a
        minss=str(mins[0])+\
               str(mins[1])+\
               str(mins[2])+\
               str(mins[3])+\
               str(mins[4])+\
               str(mins[5])
        if minss=='114514':print('哼哼哼哈哈哈哈哈哈哈哈~~~~~~~~~~')
        print('此處是驗證碼',minss,end=" ")
        ea=input('親輸入驗證碼:')
        if ea=='114514' or ea=='1919810':
            ea=minss
            print('好吧,勉強讓你過')
    del mins,minss
    del a
    gc.collect()
    print('驗證碼驗證成功')
    print('hallo,world =) ')
    
    m=input('請登錄,此處寫公共密碼:')
    while m!=password_for_all:
        print('登陸失敗,請重試')
        m=input('請登錄,此處寫公共密碼:')
    print('登陸成功')
    print('你好,用戶')

    ea=input('請您選擇用戶:1:boss,2:user,3:worker,4:roadman:')

    while 1:
        f=input('1:返回,2:繼續')
        if f=='1':
            print("Good bye!")
            ea=input('請您選擇用戶:1:boss,2:user,3:worker,4:roadman:')
        elif f=='2':
            if ea=='1':
                x=input('請登錄,此處寫密碼:')
                while x!=Password_for_Boss:
                    print('登陸失敗,請重試')
                    f=input('1:返回,2:繼續')
                    if f=='1':
                        print("Good bye!")
                        ea=input('請您選擇用戶:1:boss,2:user,3:worker,4:roadman:')
                    elif f=='2':x=input('請登錄,此處寫密碼:')
                    else:print('error')
                print('boss,您好')
                boss=1
                user=0
                worker=0
                roadman=0
                break
            if ea=='2':
                print('user,您好')
                boss=0
                user=1
                worker=0
                roadman=0
                break
            elif ea=='3':
                print(' worker,你好')
                boss=0
                user=0
                worker=1
                roadman=0
                break
            elif ea=='4':
                print('roadman,快去幹活')
                boss=0
                user=0
                worker=0
                roadman=1
                break
            else:
                print('error')
                ea=input('請您選擇用戶:1:boss,2:user,3:worker,4:roadman:')
        else:
            print('error')
    
    while 1:
        CN_fanti_print(1)
        print('0:開始菜單')
        print("1:時間,2:日期排序")
        print('3:退出賬號')
        print('註：關機用Ctrl+C')
        if boss==1:
            print("4:演示,5:密碼更改")
        a=input('請輸入:')
        if a=='0':
            while 1:
                print('開始菜單')
                CN_fanti_print(1)
                print("1:計算器")
                print('2:退出')
                a=input('請輸入:')
                if a=='1':
                    while 1:
                        f=input('1:返回,2:繼續')
                        if f=='1':
                            print("Good bye!")
                            break
                        elif f=='2':
                            print('1:加,2:減,3:乘,4:除:')
                            print('5:乘方,6:平方根,7:素數:')
                            print('8:9*9乘法表,9:因式分解,10:π:')
                            print('11:解一元一次方程,12:解一元二次方程:')
                            m=input('幹什麽:')
                                
                            if m=='1':
                                n1=int(input('請輸入一個數字'))
                                n2=int(input('請輸入另一個數字'))
                                print(n1+n2)
                            elif m=='2':
                                n1=int(input('請輸入一個數字'))
                                n2=int(input('請輸入另一個數字'))
                                print(n1-n2)
                            elif m=='3':
                                n1=int(input('請輸入一個數字'))
                                n2=int(input('請輸入另一個數字'))
                                print(n1*n2)
                            elif m=='4':
                                try:
                                    counttt=input('1:除,2:除(取整),6:除(取余)')
                                    n1=int(input('請輸入一個數字'))
                                    n2=int(input('請輸入另一個數字'))
                                    if n2==0:
                                        print('…………？')
                                    if counttt=='1':
                                        print(n1/n2)
                                    if counttt=='2':
                                        print(n1//n2)
                                    if counttt=='3':
                                        print(n1%n2)
                                except ZeroDivisionError:
                                    print('哼！')
                            elif m=='5':
                                n1=int(input('請輸入一個數字'))
                                n2=int(input('請輸入另一個數字'))
                                n1=(n1)**(n2)
                                print(n1)
                            elif m=='6':
                                n1=int(input('請輸入一個數字'))
                                n1=sqrt(n1)
                                print(n1)
                            elif m=='7':
                                p1=0
                                a=int(input('請輸入範圍(2<=a<=i):'))
                                b=int(input('請輸入範圍(i<=b):'))
                                for m in range(a,b+1):
                                    if m>=2:
                                        for i in range(2,m):
                                            if m%i==0:break
                                        else:
                                            p1=p1+1
                                            print(m,"是素數")
                                    else:print('error')
                                print("Good bye!")
                                print('有{0}個素數'.format(p1))
                                p1=0
                            elif m=='8':
                                for i in range(1, 10):
                                    print( )
                                    for j in range(1, i+1):
                                        print('{0}*{1}+={2}'.format(i,j,i*j),end=" ")
                                print('')
                            elif m=='9':
                                print('請不要輸入非負數或字符!')
                                n=int(input('請輸入一個數字(因式分解):'))
                                print('{}='.format(n),end="")
                                if not isinstance(n,int) or n<=0:
                                    print('請輸入一個正確的數字!')
                                    n=int(input('請輸入一個數字(因式分解):'))
                                    print('{}='.format(n),end="")
                                elif n in [1]:print('{0}'.format(n),end="")
                                while n not in [1]:
                                    for index in range(2,n+1):
                                        if n%index==0:
                                            n//=index
                                            if n==1:print(index,end="")
                                            else:print ('{0} *'.format(index),end=" ")
                                            break
                                print()
                            elif m=='10':
                                n=10000+4
                                p=2*10**n
                                a=p//3;p+=a
                                i=2
                                while a>0:
                                    a=a*i//(i*2+1);i+=1
                                    p+=a
                                p//=10000
                                with open('.\ikun\\pi.txt', "w", encoding="utf-8") as f1m1:f1m1.write(p)
                                os.startfile('.\ikun\\pi.txt')
                                print('已計算')
                                del n,p,a,i
                                gc.collect()
                            elif m=='11':
                                while 1:
                                    print('ax+b=c')
                                    a=float(input('a=   ,(a!=0)'))
                                    if a==0:print('a不得等於0')
                                    else:break
                                b=float(input('b=    '))
                                c=float(input('c=    '))
                                a114514=(c-b)/a
                                print('x=',a114514)
                            elif m=='12':
                                while 1:
                                    while 1:
                                        print('ax^2+bx+c=d')
                                        a=float(input('a=   ,(a!=0)'))
                                        if a==0:print('a不得等於0')
                                        else:break
                                    b=float(input('b=    '))
                                    c=float(input('c=    '))
                                    d=float(input('d=    '))
                                    a1919810=((4*a*d)-(4*a*c)+((b)**2))
                                    if a1919810<0:
                                        print('error')
                                    else:
                                        a19198101=(-b+sqrt(a1919810))/(2*a)
                                        a19198102=(-b-sqrt(a1919810))/(2*a)
                                        print('x1=',a19198101)
                                        print('x2=',a19198102)
                                        break
                            else:
                                print('error')
                        else:
                            print('error')
                elif a=='2':
                    break
                else:print('error')
        elif a=='1':
            while 1:
                f=int(input('1:返回,2:繼續'))
                if f==1:
                    print("Good bye!")
                    break
                elif f==2:
                    def get_month_days(year, month):
                        if month >12 or month <= 0:
                            return -1
                        if month == 2:
                            return 29 if year % 4 == 0 and year % 100 != 0 or year % 400 == 0 else 28
                        if month in (4, 6, 9, 11):
                            return 30
                        else:
                            return 31
                    print(t.strftime("%Y-%m-%d %H:%M:%S",t.localtime(t.time())))
                    year=int(t.strftime("%Y"))
                    month=int(t.strftime('%m'))
                    print("本月{}天".format(get_month_days(year,month)))
                    cal1=cal.month(year,month)
                    print("以下輸出{0}年{1}月份的日歷:".format(year,month))
                    print(cal1)
                    day=int(t.strftime('%d'))
                    months = (0,31,59,90,120,151,181,212,243,273,304,334)
                    sum=months[month - 1]
                    sum+=day
                    leap=0
                    if year%4==0 or year%400==0:leap=1
                    if leap==1 and month>2:sum+=1
                    print ('它是第%d天'%sum)
                    leap=0
                else:print('error')
        elif a=='2':
            while 1:
                f=int(input('1:返回，2:繼續'))
                if f==1:
                    print(" Good bye!")
                    break
                elif f==2:
                    year= int(float(input('年:')))
                    month=int(float(input('月:')))
                    day = int(float(input('日:')))
                    def get_month_days(year, month):
                        if month >12 or month <= 0:
                            return -1
                        if month == 2:
                            return 29 if year % 4 == 0 and year % 100 != 0 or year % 400 == 0 else 28
                        if month in (4, 6, 9, 11):
                            return 30
                        else:
                            return 31
                    print("本月{}天".format(get_month_days(year,month)))
                    months= (0,31,59,90,120,151,181,212,243,273,304,334)
                    if 0<month<=12:sum=months[month - 1]
                    else:print('error')
                    if 0<day<=31:pass
                    else:print('error')
                    sum+=day
                    leap=0
                    if year%4==0 or year%400==0:leap=1
                    if leap==1 and month>2:sum+=1
                    print ('它是第%d天'%sum)
                    leap=0
                else :print('error')
        elif a=='3':
            ea=input('請您選擇用戶:1:boss,2:user,3:worker,4:roadman:')
            while 1:
                f=input('1:返回,2:繼續')
                if f=='1':
                    print("Good bye!")
                    ea=input('請您選擇用戶:1:boss,2:user,3:worker,4:roadman:')
                elif f=='2':
                    if ea=='1':
                        x=input('請登錄,此處寫密碼:')
                        while x!=Password_for_Boss:
                            print('登陸失敗,請重試')
                            f=input('1:返回,2:繼續')
                            if f=='1':
                                print("Good bye!")
                                ea=input('請您選擇用戶:1:boss,2:user,3:worker,4:roadman:')
                            elif f=='2':x=input('請登錄,此處寫密碼:')
                            else:print('error')
                        print('boss,您好')
                        boss=1
                        user=0
                        worker=0
                        roadman=0
                        break
                    if ea=='2':
                        print('user,您好')
                        boss=0
                        user=1
                        worker=0
                        roadman=0
                        break
                    elif ea=='3':
                        print(' worker,你好')
                        boss=0
                        user=0
                        worker=1
                        roadman=0
                        break
                    elif ea=='4':
                        print('roadman,快去幹活')
                        boss=0
                        user=0
                        worker=0
                        roadman=1
                        break
                    else:
                        print('error')
                        ea=input('請您選擇用戶:1:boss,2:user,3:worker,4:roadman:')
                else:print('error')
    
        elif a=='4':
            while 1:
                if boss!=1:
                    if roadman==1:print('※你無權訪問,你越界了！')
                    if worker==1:print('你有這個資格嗎,去工作吧,請')
                    if user==1:print('你沒有足夠的權限')
                f=int(input('1:返回,2:繼續'))
                if f==1:
                    print("Good bye!")
                    break
                elif f==2:
                    a=input('1:普通演示,2:權限演示')
                    if a=='1':
                        while 1:
                            f=input('1:返回,2:繼續')
                            if f=='1':
                                print("Good bye!")
                                break
                            elif f=='2':print('404 Not Found')
                            else:print('error')
                    elif a=='2':
                        while 1:
                            if boss!=1:
                                if roadman==1:
                                    print('※你無權訪問,你越界了！')
                                if worker==1:
                                    print('你有這個資格嗎,去工作吧,請')
                                if user==1:
                                    print('你沒有足夠的權限')
                            f=int(input('1:返回,2:繼續'))
                            if f==1:
                                print("Good bye!")
                                break
                            elif f==2:print('404 Not Found')
                            else:print('error')
                else:print('error')
        elif a=='5':
            while 1:
                if boss!=1:
                    if roadman==1:print('※你無權訪問,你越界了！')
                    if worker==1:print('你有這個資格嗎,去工作吧,請')
                    if user==1:print('你沒有足夠的權限')
                f=int(input('1:返回,2:繼續'))
                if f==1:
                    print("Good bye!")
                    break
                elif f==2:
                    num10=input('boss,請輸入原始密碼:')
                    if num10!=Password_for_Boss:
                        print('密碼錯誤')
                        num10=input('boss,請輸入原始密碼:')
                    Password_for_Boss=input('請輸入新密碼:')
                    xiugay(1)
                    with open('.\ikun\\Password_for_Boss.txt','w') as f2:f2.write(Password_for_Boss)
                    os.startfile('.\ikun\\Password_for_Boss.txt')
                    print('boss您的新密碼是{0}'.format(Password_for_Boss))
                else:print('error')
        else :
            print('error')
def CN_allthing(qwe):
    filem(1)
    global password_for_all
    global Password_for_Boss
    global mins
    for i in range(6):
        a=random.randint(0,9)
        mins[i]=a
    minss=str(mins[0])+\
           str(mins[1])+\
           str(mins[2])+\
           str(mins[3])+\
           str(mins[4])+\
           str(mins[5])
    print('此处是验证码',minss,end=" ")
    ea=input('亲输入验证码:')
    if minss=='114514':
        print('哼哼哼哈哈哈哈哈哈哈哈~~~~~~~~~~')
        ea=minss
    if ea=='114514' or ea=='1919810':
        ea=minss
        print('好吧,勉强让你过')
    while ea!=minss:
        print('验证码验证失败，请重试')
        for i in range(6):
            a=random.randint(0,9)
            mins[i]=a
        minss=str(mins[0])+\
               str(mins[1])+\
               str(mins[2])+\
               str(mins[3])+\
               str(mins[4])+\
               str(mins[5])
        if minss=='114514':print('哼哼哼哈哈哈哈哈哈哈哈~~~~~~~~~~')
        print('此处是验证码',minss,end=" ")
        ea=input('亲输入验证码:')
        if ea=='114514' or ea=='1919810':
            ea=minss
            print('好吧,勉强让你过')
    del mins,minss
    del a
    gc.collect()
    print('验证码验证成功')
    print('hallo,world =) ')
    
    m=input('请登录,此处写公共密码:')
    while m!=password_for_all:
        print('登陆失败,请重试')
        m=input('请登录,此处写公共密码:')
    print('登陆成功')
    print('你好,用户')

    ea=input('请您选择用户:1:boss,2:user,3:worker,4:roadman:')

    while 1:
        f=input('1:返回,2:继续')
        if f=='1':
            print("Good bye!")
            ea=input('请您选择用户:1:boss,2:user,3:worker,4:roadman:')
        elif f=='2':
            if ea=='1':
                x=input('请登录,此处写密码:')
                while x!=Password_for_Boss:
                    print('登陆失败,请重试')
                    f=input('1:返回,2:继续')
                    if f=='1':
                        print("Good bye!")
                        ea=input('请您选择用户:1:boss,2:user,3:worker,4:roadman:')
                    elif f=='2':x=input('请登录,此处写密码:')
                    else:print('error')
                print('boss,您好')
                boss=1
                user=0
                worker=0
                roadman=0
                break
            if ea=='2':
                print('user,您好')
                boss=0
                user=1
                worker=0
                roadman=0
                break
            elif ea=='3':
                print(' worker,你好')
                boss=0
                user=0
                worker=1
                roadman=0
                break
            elif ea=='4':
                print('roadman,快去干活')
                boss=0
                user=0
                worker=0
                roadman=1
                break
            else:
                print('error')
                ea=input('请您选择用户:1:boss,2:user,3:worker,4:roadman:')
        else:
            print('error')
    while 1:
        CN_print(1)
        print('0:开始菜单')
        print("1:时间,2:日期排序")
        print('3:退出账号')
        print('注：关机用Ctrl+C')
        if boss==1:
            print("4:演示,5:密码更改")
        a=input('请输入:')
        if a=='0':
            while 1:
                print('开始菜单')
                CN_print(1)
                print("1:计算器")
                print('2:退出')
                a=input('请输入:')
                if a=='1':
                    while 1:
                        f=input('1:返回,2:继续')
                        if f=='1':
                            print("Good bye!")
                            break
                        elif f=='2':
                            print('1:加,2:减,3:乘,4:除:')
                            print('5:乘方,6:平方根,7:素数:')
                            print('8:9*9乘法表,9:因式分解,10:π:')
                            print('11:解一元一次方程,12:解一元二次方程:')
                            m=input('干什么:')
                                
                            if m=='1':
                                n1=int(input('请输入一个数字'))
                                n2=int(input('请输入另一个数字'))
                                print(n1+n2)
                            elif m=='2':
                                n1=int(input('请输入一个数字'))
                                n2=int(input('请输入另一个数字'))
                                print(n1-n2)
                            elif m=='3':
                                n1=int(input('请输入一个数字'))
                                n2=int(input('请输入另一个数字'))
                                print(n1*n2)
                            elif m=='4':
                                try:
                                    counttt=input('1:除,2:除(取整),6:除(取余)')
                                    n1=int(input('请输入一个数字'))
                                    n2=int(input('请输入另一个数字'))
                                    if n2==0:
                                        print('…………？')
                                    if counttt=='1':
                                        print(n1/n2)
                                    if counttt=='2':
                                        print(n1//n2)
                                    if counttt=='3':
                                        print(n1%n2)
                                except ZeroDivisionError:
                                    print('哼！')
                            elif m=='5':
                                n1=int(input('请输入一个数字'))
                                n2=int(input('请输入另一个数字'))
                                n1=(n1)**(n2)
                                print(n1)
                            elif m=='6':
                                n1=int(input('请输入一个数字'))
                                n1=sqrt(n1)
                                print(n1)
                            elif m=='7':
                                p1=0
                                a=int(input('请输入范围(2<=a<=i):'))
                                b=int(input('请输入范围(i<=b):'))
                                for m in range(a,b+1):
                                    if m>=2:
                                        for i in range(2,m):
                                            if m%i==0:break
                                        else:
                                            p1=p1+1
                                            print(m,"是素数")
                                    else:print('error')
                                print("Good bye!")
                                print('有{0}个素数'.format(p1))
                                p1=0
                            elif m=='8':
                                for i in range(1, 10):
                                    print( )
                                    for j in range(1, i+1):
                                        print('{0}*{1}+={2}'.format(i,j,i*j),end=" ")
                                print('')
                            elif m=='9':
                                print('请不要输入非负数或字符!')
                                n=int(input('请输入一个数字(因式分解):'))
                                print('{}='.format(n),end="")
                                if not isinstance(n,int) or n<=0:
                                    print('请输入一个正确的数字!')
                                    n=int(input('请输入一个数字(因式分解):'))
                                    print('{}='.format(n),end="")
                                elif n in [1]:print('{0}'.format(n),end="")
                                while n not in [1]:
                                    for index in range(2,n+1):
                                        if n%index==0:
                                            n//=index
                                            if n==1:print(index,end="")
                                            else:print ('{0} *'.format(index),end=" ")
                                            break
                                print()
                            elif m=='10':
                                n=10000+4
                                p=2*10**n
                                a=p//3;p+=a
                                i=2
                                while a>0:
                                    a=a*i//(i*2+1);i+=1
                                    p+=a
                                p//=10000
                                with open('.\ikun\\pi.txt', "w", encoding="utf-8") as f1m1:f1m1.write(p)
                                os.startfile('.\ikun\\pi.txt')
                                print('已计算')
                                del n,p,a,i
                                gc.collect()
                            elif m=='11':
                                while 1:
                                    print('ax+b=c')
                                    a=float(input('a=   ,(a!=0)'))
                                    if a==0:print('a不得等于0')
                                    else:break
                                b=float(input('b=    '))
                                c=float(input('c=    '))
                                a114514=(c-b)/a
                                print('x=',a114514)
                            elif m=='12':
                                while 1:
                                    while 1:
                                        print('ax^2+bx+c=d')
                                        a=float(input('a=   ,(a!=0)'))
                                        if a==0:print('a不得等于0')
                                        else:break
                                    b=float(input('b=    '))
                                    c=float(input('c=    '))
                                    d=float(input('d=    '))
                                    a1919810=((4*a*d)-(4*a*c)+((b)**2))
                                    if a1919810<0:
                                        print('error')
                                    else:
                                        a19198101=(-b+sqrt(a1919810))/(2*a)
                                        a19198102=(-b-sqrt(a1919810))/(2*a)
                                        print('x1=',a19198101)
                                        print('x2=',a19198102)
                                        break
                            else:
                                print('error')
                        else:
                            print('error')
                elif a=='2':
                    break
                else:print('error')
        elif a=='1':
            while 1:
                f=int(input('1:返回,2:继续'))
                if f==1:
                    print("Good bye!")
                    break
                elif f==2:
                    def get_month_days(year, month):
                        if month >12 or month <= 0:
                            return -1
                        if month == 2:
                            return 29 if year % 4 == 0 and year % 100 != 0 or year % 400 == 0 else 28
                        if month in (4, 6, 9, 11):
                            return 30
                        else:
                            return 31
                    print(t.strftime("%Y-%m-%d %H:%M:%S",t.localtime(t.time())))
                    year=int(t.strftime("%Y"))
                    month=int(t.strftime('%m'))
                    print("本月{}天".format(get_month_days(year,month)))
                    cal1=cal.month(year,month)
                    print("以下输出{0}年{1}月份的日历:".format(year,month))
                    print(cal1)
                    day=int(t.strftime('%d'))
                    months = (0,31,59,90,120,151,181,212,243,273,304,334)
                    sum=months[month - 1]
                    sum+=day
                    leap=0
                    if year%4==0 or year%400==0:leap=1
                    if leap==1 and month>2:sum+=1
                    print ('它是第%d天'%sum)
                    leap=0
                else:print('error')
        elif a=='2':
            while 1:
                f=int(input('1:返回，2:继续'))
                if f==1:
                    print(" Good bye!")
                    break
                elif f==2:
                    year= int(float(input('年:')))
                    month=int(float(input('月:')))
                    day = int(float(input('日:')))
                    def get_month_days(year, month):
                        if month >12 or month <= 0:
                            return -1
                        if month == 2:
                            return 29 if year % 4 == 0 and year % 100 != 0 or year % 400 == 0 else 28
                        if month in (4, 6, 9, 11):
                            return 30
                        else:
                            return 31
                    print("本月{}天".format(get_month_days(year,month)))
                    months= (0,31,59,90,120,151,181,212,243,273,304,334)
                    if 0<month<=12:sum=months[month - 1]
                    else:print('error')
                    if 0<day<=31:pass
                    else:print('error')
                    sum+=day
                    leap=0
                    if year%4==0 or year%400==0:leap=1
                    if leap==1 and month>2:sum+=1
                    print ('它是第%d天'%sum)
                    leap=0
                else :print('error')
        elif a=='3':
            ea=input('请您选择用户:1:boss,2:user,3:worker,4:roadman:')
            while 1:
                f=input('1:返回,2:继续')
                if f=='1':
                    print("Good bye!")
                    ea=input('请您选择用户:1:boss,2:user,3:worker,4:roadman:')
                elif f=='2':
                    if ea=='1':
                        x=input('请登录,此处写密码:')
                        while x!=Password_for_Boss:
                            print('登陆失败,请重试')
                            f=input('1:返回,2:继续')
                            if f=='1':
                                print("Good bye!")
                                ea=input('请您选择用户:1:boss,2:user,3:worker,4:roadman:')
                            elif f=='2':x=input('请登录,此处写密码:')
                            else:print('error')
                        print('boss,您好')
                        boss=1
                        user=0
                        worker=0
                        roadman=0
                        break
                    if ea=='2':
                        print('user,您好')
                        boss=0
                        user=1
                        worker=0
                        roadman=0
                        break
                    elif ea=='3':
                        print(' worker,你好')
                        boss=0
                        user=0
                        worker=1
                        roadman=0
                        break
                    elif ea=='4':
                        print('roadman,快去干活')
                        boss=0
                        user=0
                        worker=0
                        roadman=1
                        break
                    else:
                        print('error')
                        ea=input('请您选择用户:1:boss,2:user,3:worker,4:roadman:')
                else:print('error')
    
        elif a=='4':
            while 1:
                if boss!=1:
                    if roadman==1:print('※你无权访问,你越界了！')
                    if worker==1:print('你有这个资格吗,去工作吧,请')
                    if user==1:print('你没有足够的权限')
                f=int(input('1:返回,2:继续'))
                if f==1:
                    print("Good bye!")
                    break
                elif f==2:
                    a=input('1:普通演示,2:权限演示')
                    if a=='1':
                        while 1:
                            f=input('1:返回,2:继续')
                            if f=='1':
                                print("Good bye!")
                                break
                            elif f=='2':print('404 Not Found')
                            else:print('error')
                    elif a=='2':
                        while 1:
                            if boss!=1:
                                if roadman==1:
                                    print('※你无权访问,你越界了！')
                                if worker==1:
                                    print('你有这个资格吗,去工作吧,请')
                                if user==1:
                                    print('你没有足够的权限')
                            f=int(input('1:返回,2:继续'))
                            if f==1:
                                print("Good bye!")
                                break
                            elif f==2:print('404 Not Found')
                            else:print('error')
                else:print('error')
        elif a=='5':
            while 1:
                if boss!=1:
                    if roadman==1:print('※你无权访问,你越界了！')
                    if worker==1:print('你有这个资格吗,去工作吧,请')
                    if user==1:print('你没有足够的权限')
                f=int(input('1:返回,2:继续'))
                if f==1:
                    print("Good bye!")
                    break
                elif f==2:
                    num10=input('boss,请输入原始密码:')
                    if num10!=Password_for_Boss:
                        print('密码错误')
                        num10=input('boss,请输入原始密码:')
                    Password_for_Boss=input('请输入新密码:')
                    xiugay(1)
                    with open('.\ikun\\Password_for_Boss.txt','w') as f2:f2.write(Password_for_Boss)
                    os.startfile('.\ikun\\Password_for_Boss.txt')
                    print('boss您的新密码是{0}'.format(Password_for_Boss))
                else:print('error')
        else :
            print('error')
def US_allthing(qwe):
    filem(1)
    global password_for_all 
    global Password_for_Boss
    global mins
    for i in range(6):
        a=random.randint(0,9)
        mins[i]=a
    minss=str(mins[0])+str(mins[1])+str(mins[2])+str(mins[3])+str(mins[4])+str(mins[5])
    print('Verification Code',minss,end=" ")
    ea=input('please input:')
    while ea!=minss:
        print('CAPTCHA error,Please try again')
        for i in range(6):
            a=random.randint(0,9)
            mins[i]=a
        minss=str(mins[0])+\
               str(mins[1])+\
               str(mins[2])+\
               str(mins[3])+\
               str(mins[4])+\
               str(mins[5])
        print('Verification Code',minss,end=" ")
        ea=input('please input:')
    del mins,minss
    gc.collect()
    print('OK!')
    print('hallo,world =) ')
    
    m=input('Public password:')
    while m!=password_for_all:
        print('Login failed, please try again')
        m=input('Public password:')
    print('Login successfully')
    print('Hello, user')

    ea=input('Users:1:boss,2:user,3:worker,4:roadman:')

    while 1:
        f=input('1:back,2:continue')
        if f=='1':
            print("Good bye!")
            ea=input('Users:1:boss,2:user,3:worker,4:roadman:')
        elif f=='2':
            if ea=='1':
                x=input('Please log in and write your password here:')
                while x!=Password_for_Boss:
                    print('Login failed, please try again')
                    f=input('1:back,2:continue')
                    if f=='1':
                        print("Good bye!")
                        ea=input('Users:1:boss,2:user,3:worker,4:roadman:')
                    elif f=='2':x=input('Please log in and write your password here:')
                    else:print('error')
                print('Hello,boss')
                boss=1
                user=0
                worker=0
                roadman=0
                break
            if ea=='2':
                print('Hello,user')
                boss=0
                user=1
                worker=0
                roadman=0
                break
            elif ea=='3':
                print('Ah,worker,Hello')
                boss=0
                user=0
                worker=1
                roadman=0
                break
            elif ea=='4':
                print('roadman,get to work!')
                boss=0
                user=0
                worker=0
                roadman=1
                break
            else:
                print('error')
                print('well')
                ea=input('Users:1:boss,2:user,3:worker,4:roadman:')
        else:
            print('error')
    
    while 1:
        US_print(1)
        print('0:Start menu')
        print("1:Time,2:Sort date")
        print('3:Log out')
        print('Note: Ctrl+C for shutdown')
        if boss==1:print("4:sample,5:Password Change")
        a=input('input:')
        if a=='0':
            print("Here're 'Start menu'")
            US_print(1)
            print("1:calc")
            print('2:back')
            a=input('input:')
            while 1:
                if a=='1':
                    while 1:
                        f=input('1,back,2:continue')
                        if f=='1':
                            print("Good bye!")
                            break
                        elif f=='2':
                            print('1:add,2:minus,3:multiply,4:divide')
                            print('5:involution,6:sqrt,7:prime number')
                            print('8:9*9 tables,9:factorization,10:pi')
                            print('11:linear equation,12:quadratic equation')
                            m=input('input:')
                                
                            if m=='1':
                                n1=int(input('Please input a number'))
                                n2=int(input('Please input another number'))
                                print(n1+n2)
                            elif m=='2':
                                n1=int(input('Please input a number'))
                                n2=int(input('Please input another number'))
                                print(n1-n2)
                            elif m=='3':
                                n1=int(input('Please input a number'))
                                n2=int(input('Please input another number'))
                                print(n1*n2)
                            elif m=='4':
                                try:
                                    counttt=input('1:divide,2:divide(take an integer),6:divide(take the remainder)')
                                    count(1)
                                    if n2==0:
                                        print('NO!')
                                    if counttt=='1':
                                        print(n1/n2)
                                    if counttt=='2':
                                        print(n1//n2)
                                    if counttt=='3':
                                        print(n1%n2)
                                except ZeroDivisionError:
                                    print('Ahhh!~')
                            elif m=='5':
                                n1=int(input('Please input a number'))
                                n2=int(input('Please input another number'))
                                n1=(n1)**(n2)
                                print(n1)
                            elif m=='6':
                                n1=int(input('Please input a number'))
                                n1=sqrt(n1)
                                print(n1)
                            elif m=='7':
                                p1=0
                                a=int(input('input a range(2<=a<=i):'))
                                b=int(input('input a range(i<=b):'))
                                for m in range(a,b+1):
                                    if m>=2:
                                        for i in range(2,m):
                                            if m%i==0:break
                                        else:
                                            p1=p1+1
                                            print(m,"Is A Factorization")
                                    else:print('error')
                                print("Good bye!")
                                print('{0}Factorization'.format(p1))
                                p1=0
                            elif m=='8':
                                for i in range(1, 10):
                                    print( )
                                    for j in range(1, i+1):
                                        print('{0}*{1}+={2}'.format(i,j,i*j),end=" ")
                                print('')
                            elif m=='9':
                                print("Don't input a non-negative number or Str!")
                                n=int(input('input:'))
                                print('{}='.format(n),end="")
                                if not isinstance(n,int) or n<=0:
                                    print('………………？')
                                    n=int(input('input:'))
                                    print('{}='.format(n),end="")
                                elif n in [1]:print('{0}'.format(n),end="")
                                while n not in [1]:
                                    for index in range(2,n+1):
                                        if n%index==0:
                                            n//=index
                                            if n==1:print(index,end="")
                                            else:print ('{0} *'.format(index),end=" ")
                                            break
                                print()
                            elif m=='10':
                                n=10000+4
                                p=2*10**n
                                a=p//3;p+=a
                                i=2
                                while a>0:
                                    a=a*i//(i*2+1);i+=1
                                    p+=a
                                p//=10000
                                with open('.\ikun\\pi.txt', "w", encoding="utf-8") as f1m1:f1m1.write(p)
                                os.startfile('.\ikun\\pi.txt')
                                print('OK!!!')
                                del n,p,a,i
                                gc.collect()
                            elif m=='11':
                                while 1:
                                    print('ax+b=c')
                                    a=float(input('a=   ,(a!=0)'))
                                    if a==0:print("a can't be 0")
                                    else:break
                                b=float(input('b=    '))
                                c=float(input('c=    '))
                                a114514=(c-b)/a
                                print('x=',a114514)
                            elif m=='12':
                                while 1:
                                    while 1:
                                        print('ax^2+bx+c=d')
                                        a=float(input('a=   ,(a!=0)'))
                                        if a==0:print("a can't be 0")
                                        else:break
                                    b=float(input('b=    '))
                                    c=float(input('c=    '))
                                    d=float(input('d=    '))
                                    a1919810=((4*a*d)-(4*a*c)+((b)**2))
                                    if a1919810<0:
                                        print('error')
                                    else:
                                        a19198101=(-b+sqrt(a1919810))/(2*a)
                                        a19198102=(-b-sqrt(a1919810))/(2*a)
                                        print('x1=',a19198101)
                                        print('x2=',a19198102)
                            else:print('error')
                        else:print('error')
                elif a=='2':
                    break
                else:print('error')
        elif a=='1':
            while 1:
                f=int(input('1:back,2:continue'))
                if f==1:
                    print("Good bye!")
                    break
                elif f==2:
                    def get_month_days(year, month):
                        if month >12 or month <= 0:
                            return -1
                        if month == 2:
                            return 29 if year % 4 == 0 and year % 100 != 0 or year % 400 == 0 else 28
                        if month in (4, 6, 9, 11):
                            return 30
                        else:
                            return 31
                    print(t.strftime("%Y-%m-%d %H:%M:%S",t.localtime(t.time())))
                    year=int(t.strftime("%Y"))
                    month=int(t.strftime('%m'))
                    print("This month {} days!".format(get_month_days(year,month)))
                    cal1=cal.month(year,month)
                    print(" {0} year {1} 月mouth's calendar:".format(year,month))
                    print(cal1)
                    day=int(t.strftime('%d'))
                    months = (0,31,59,90,120,151,181,212,243,273,304,334)
                    sum=months[month - 1]
                    sum+=day
                    leap=0
                    if year%4==0 or year%400==0:leap=1
                    if leap==1 and month>2:sum+=1
                    print ('the %d day'%sum)
                    leap=0
                else:print('error')
        elif a=='2':
            while 1:
                f=int(input('1:back，2:continue'))
                if f==1:
                    print(" Good bye!")
                    break
                elif f==2:
                    year= int(float(input('year:')))
                    month=int(float(input('mouth:')))
                    day = int(float(input('day:')))
                    def get_month_days(year, month):
                        if month >12 or month <= 0:
                            return -1
                        if month == 2:
                            return 29 if year % 4 == 0 and year % 100 != 0 or year % 400 == 0 else 28
                        if month in (4, 6, 9, 11):
                            return 30
                        else:
                            return 31
                    print("This month {} days".format(get_month_days(year,month)))
                    months= (0,31,59,90,120,151,181,212,243,273,304,334)
                    if 0<month<=12:sum=months[month - 1]
                    else:print('error')
                    if 0<day<=31:pass
                    else:print('error')
                    sum+=day
                    leap=0
                    if year%4==0 or year%400==0:leap=1
                    if leap==1 and month>2:sum+=1
                    print ('the %d day'%sum)
                    leap=0
                else :print('error')
        elif a=='3':
            ea=input('Users:1:boss,2:user,3:worker,4:roadman:')
            while 1:
                f=input('1:back,2:continue')
                if f=='1':
                    print("Good bye!")
                    ea=input('Users:1:boss,2:user,3:worker,4:roadman:')
                elif f=='2':
                    if ea=='1':
                        x=input('Please log in and write your password here:')
                        while x!=Password_for_Boss:
                            print('Login failed, please try again')
                            f=input('1:back,2:continue')
                            if f=='1':
                                print("Good bye!")
                                ea=input('Users:1:boss,2:user,3:worker,4:roadman:')
                            elif f=='2':x=input('Please log in and write your password here:')
                            else:print('error')
                        print('boss,Hallo!')
                        boss=1
                        user=0
                        worker=0
                        roadman=0
                        break
                    if ea=='2':
                        print('user,Hallo')
                        boss=0
                        user=1
                        worker=0
                        roadman=0
                        break
                    elif ea=='3':
                        print('Ah,worker,Hallo')
                        boss=0
                        user=0
                        worker=1
                        roadman=0
                        break
                    elif ea=='4':
                        print('roadman,go to work!')
                        boss=0
                        user=0
                        worker=0
                        roadman=1
                        break
                    else:
                        print('error')
                        ea=input('Users:1:boss,2:user,3:worker,4:roadman:')
                else:print('error')
    
        elif a=='4':
            while 1:
                if boss!=1:
                    if roadman==1:print('※NO')
                    if worker==1:print('Get back to work')
                    if user==1:print("You Don't have enough access")
                f=int(input('1:back,2:continue'))
                if f==1:
                    print("Good bye!")
                    break
                elif f==2:
                    a=input('1:simple,2:up')
                    if a=='1':
                        while 1:
                            f=input('1:back,2:continue')
                            if f=='1':
                                print("Good bye!")
                                break
                            elif f=='2':print('404 Not Found')
                            else:print('error')
                    elif a=='2':
                        while 1:
                            if boss!=1:
                                if roadman==1:print('※NO')
                                if worker==1:print('Get back to work')
                                if user==1:print("You Don't have enough access")
                            f=int(input('1:back,2:continue'))
                            if f==1:
                                print("Good bye!")
                                break
                            elif f==2:print('404 Not Found')
                            else:print('error')
                else:print('error')
        elif a=='5':
            while 1:
                if boss!=1:
                    if roadman==1:print('※NO')
                    if worker==1:print('Get back to work')
                    if user==1:print("You Don't have enough access")
                f=int(input('1:back,2:continue'))
                if f==1:
                    print("Good bye!")
                    break
                elif f==2:
                    num10=input('boss,Please enter your original password:')
                    if num10!=Password_for_Boss:
                        print('Password error')
                        num10=input('boss,Please enter your original password:')
                    Password_for_Boss=input('Please enter a new password:')
                    xiugay(1)
                    with open('.\ikun\\Password_for_Boss.txt','w') as f2:f2.write(Password_for_Boss)
                    os.startfile('.\ikun\\Password_for_Boss.txt')
                    print('boss~your new password is :{0}'.format(Password_for_Boss))
                else:print('error')
        else :
            print('error')
def main(qwe):
    print("开始运行,wish haven't ERROR")
    with open('.\ikun\\upgrade.txt','r') as fp:
        upgrade=fp.readline()
    if upgrade=='True':
        print()
        print('您是初次使用我们巨硬的产品 noodows (R才怪) {0}(内部版本 {1}) 无图像版'.format(version,build_version))
        print("You're use noodows (no R) {0}( {1} build) no Image by Bignesshard".format(version,build_version))
        print()
        print('设置语言')
        print('Setup language')
        print()
        while 1:
            lauguage=input('1:English,2:简体中文,3:繁體中文')
            if lauguage=='1':
                print('OK!')
                break
            elif lauguage=='2':
                print('OK!')
                break
            elif lauguage=='3':
                print('OK!')
                break
            else:print('error')
        print('马上就好')
        print("It'll only take a second")
        print()
        with open('.\ikun\\lauguage.txt', "w", encoding="utf-8") as fp1:
            fp1.write(lauguage)
        upgrade='False'
        with open('.\ikun\\upgrade.txt', "w", encoding="utf-8") as fp1:
            fp1.write(upgrade)
        print('欢迎使用')
        print('Thank you for your support!')
        with open('.\ikun\\lauguage.txt', "r", encoding="utf-8") as fpp1:
            lauguage=fpp1.readline()
        if lauguage=='1':
            US_allthing(1)
        elif lauguage=='2':
            CN_allthing(1)
        elif lauguage=='3':
            CN_fanti_allthing(1)
        else :
            print('error')
    elif upgrade=='False':
        with open('.\ikun\\lauguage.txt', "r", encoding="utf-8") as fpp1:
            lauguage=fpp1.readline()
        if lauguage=='1':
            print('Hallo!')
            US_allthing(1)
        elif lauguage=='2':
            print('你好')
            CN_allthing(1)
        elif lauguage=='3':
            print('你好')
            CN_fanti_allthing(1)
        else :
            print('error')
    else :
        print('error')
'''
以下是正文
'''
def __Lidao_Main__(qwe):
    while 1:
        try:
            main(1)
        except IOError:
            print()
            print('Error!!!!')
            print('Y O U  DELETE  SOME THIN G VERY IMPO RT !!!')
            print('noodows 正在尝试重启')
        except KeyboardInterrupt:
            print()
            print('Error!!!!')
            print('Y O U  B R E A K  T H E  WHILE TURE?')
            a=input('Did you mean it? 1:yes,2:no    ')
            a=int(float(a))
            if a==1:
                print('OK')
                break
            if a==2:
                print('noodows 正在尝试重启')
if __name__=='__main__':
    __Lidao_Main__(1)
