from PIL import Image
import streamlit as st
import random
from pydub import AudioSegment
import pyecharts
import json
import math22
#首页
user_name = '未登录'
with open("client/users.json",'r',encoding='utf-8') as f:
    users = {}
    users = json.load(f)
filters = {
    "模糊滤镜": ImageFilter.BLUR,
    "轮廓滤镜": ImageFilter.CONTOUR,
    "边缘增强滤镜": ImageFilter.EDGE_ENHANCE,
    "浮雕滤镜": ImageFilter.EMBOSS,
    "锐化滤镜": ImageFilter.SHARPEN,
    "平滑滤镜": ImageFilter.SMOOTH,
}

col1,col2,col3,col4 = st.columns([1,1,1,1])
def register_and_login():    
            st.title('登录/注册')
            st.write("尊敬的用户，请先登录/注册才能享受更多功能哦")
            c = st.selectbox("请选择操作", ["登录", "注册"])
            if c == '登录':
                user_name = st.text_input("请输入用户名：")
                if user_name in users:
                    user_password = st.text_input("请输入密码：",type='password')
                    if st.button("登录"): 
                        if users[user_name] == user_password:
                            st.success(f"欢迎，{user_name}！登录成功！")
                        else:
                            st.error("密码错误！")
                            user_name = '未登录'
                else:
                    st.error("该用户名不存在，请重新输入！")
            if c == '注册':
                new_user_name = st.text_input("请输入新的用户名：")
                if new_user_name not in users:
                    new_user_password = st.text_input("请输入密码", type='password')
                    users[new_user_name] = new_user_password
                    st.success(f"用户 {new_user_name} 注册成功！")
                else:
                    st.error("该用户名已存在，请重新输入！")
def image_filters():
    global filters
    st.subheader(":green[:sparkles:图片滤镜调整工具:sparkles:]")
    st.text("自定义调整图片滤镜")
    type_list=["png","jpeg","jpg","gif","bmp","webp"]
    uploaded_file = st.file_uploader("上传图片", type=type_list)
    if(uploaded_file):
        # 获取图片文件的名称.类型.大小
        file_name = uploaded_file.name  # 文件名字
        file_type = uploaded_file.type  # 文件格式
        file_size = uploaded_file.size  # 文件大小
        img = Image.open(uploaded_file)
        st.image(img)
        # 定义选项列表
        options = ['请选择...', '模糊滤镜', '轮廓滤镜', '边缘增强滤镜', '浮雕滤镜', '锐化滤镜', '平滑滤镜', '素描风格转化', '字符画风格转化(实验性功能)','图片尺寸转换','图片RGB换色']
        # 使用selectbox方法显示下拉选择框
        selected_filter = st.selectbox('请选择一个工具', options)
        # 处理图片
        if("滤镜" in selected_filter):
            st.write("处理结果：")
            img_temp = img.filter(filters[selected_filter]).convert("RGBA")
            st.image(img_temp)
            st.success("图片转换成功！")
            st.info("处理好后的图片可以直接右击并选择【将图像另存为】将其保存到本地")
        elif(selected_filter == "素描风格转化"):
            st.write("处理结果：")
            img_temp = to_sketch(img)
            st.image(img_temp)
            st.success("图片转换成功！")
            st.info("处理好后的图片可以直接右击并选择【将图像另存为】将其保存到本地")
        elif(selected_filter == "字符画风格转化(实验性功能)"):
            st.info("字符画风格转化为实验性功能, 可能会出现转换有误的问题,或者出现不清楚的情况")
            st.write("处理结果：")
            img_temp = to_char(img)
            st.image(img_temp)
            st.success("图片转换成功！")
            st.info("处理好后的图片可以直接右击并选择【将图像另存为】将其保存到本地")
        elif(selected_filter == "图片尺寸转换"):
            img = Image.open(uploaded_file)
            st.image(img)
            old_width, old_height = img.size
            st.write(f"原图尺寸: {old_width}×{old_height}")
            cab_1, cab_2 = st.columns([1,1])
            with cab_1:
                new_width = st.number_input(label="请输入新图片的宽", min_value=1, value=old_width, step=1)
            with cab_2:
                new_height = st.number_input(label="请输入新图片的高", min_value=1, value=old_height, step=1)
            if(st.button("确定")):
                st.write(f"处理结果({new_width}×{new_height})：")
                img1 = img.resize(( int(new_width), int(new_height) ))
                st.image(img1)
                st.success("图片转换成功！")
                st.info("处理好后的图片可以直接右击并选择【将图像另存为】将其保存到本地")
        elif (selected_filter == "图片RGB换色"):
            file_name = uploaded_file.name
            file_type = uploaded_file.type
            file_size = uploaded_file.size
            img=Image.open(uploaded_file)
            img_tab1,img_tab2,img_tab3,img_tab4 = st.tabs(["原图","颜色失真1","颜色失真2","颜色失真3"])
            with img_tab1:
                st.image(img)
                st.success("图片加载成功！")
            with img_tab2:
                try:
                    st.image(image_change(img,0,2,1))
                    st.success("图片转换成功！")
                except:
                    st.error("转换失败！")
            with img_tab3:
                try:
                    st.image(image_change(img,2,1,0))
                    st.success("图片转换成功！")
                except:
                    st.error("转换失败！")
            with img_tab4:
                try:
                    st.image(image_change(img,1,0,2))
                    st.success("图片转换成功！")
                except:
                    st.error("转换失败！")

with col4:
    if st.button("登录/注册"):
        register_and_login()
PVZ_file = 'game\PVZ\PVZ.rar'
PVZ_95_file = 'game\PVZ\PVZ_95.rar'
PVZ_β_file = 'game\PVZ\PVZ_β.rar'
PVZ_E_file = 'game\PVZ\PVZ_E支.rar'
PVZ_wuming_file = 'game\PVZ\PVZ_无名.rar'
PVZ_random_file = 'game\PVZ\PVZ_随机.rar'
PVZ_Rouge_file = 'game\PVZ\PVZ_Rouge.rar'
PVZ_xiugaiqi_file = 'game\PVZ\PVZ_修改器.rar'
raft_file = r'C:\Users\sunxi\Desktop\python冬令营孙鹏飞\game\raft\raft.rar'
balloon_snow_open = True
st.divider()
#或下载一些实用小工具
#代码分站：上传自己喜欢的作品，下载一些通用的小工具，python制作的哦
#'代码分站',
st.text("""
工作室名字：飞·网
根据地用户：所有人
根据地用途：综合
现有模块：兴趣推荐、图片处理、词典、聊天室
原创模块：常用网站、游戏分站、音乐分站、代码分站、世界地图
原创模块一句话介绍：
    常用网站：新闻网呀、天气网呀、B站啊、某音啊...
    游戏分站：上传和下载一些游戏的文件，免费玩到一些付费游戏，不能商业化使用哦
    音乐分站：上传自己喜欢的音乐，也可以在线收听，不能商业化使用哦
    世界地图：找找你的家乡在哪
""")
if st.toggle('气球/雪花特效 开/关'):
    balloon_snow_open = True
else:
    balloon_snow_open = False
choice = st.slider('控制气球/雪花特效数量',1,50,1)
web = st.sidebar.radio('首页',['兴趣推荐','图片处理','发现','聊天室','常用网站','影音专区','游戏专区','世界地图','设置'])
if balloon_snow_open:
    for i in range(int(choice)):
        if random.randint(1,2) == 1:
            st.snow()
        st.balloons()
def bgm():
    with open ('music\BGM.mp3','rb') as f:
        mymusic = f.read()
    st.audio(mymusic,format='audio/mp3',start_time=0)
    with open ('music\BGM2.mp3','rb') as g:
        mymusic2 = g.read()
    st.audio(mymusic2,format='audio/mp3',start_time=0)

#侧边栏
def image_change(img,rc,gc,bc):
    width,height = img.size
    img_array = img.load()
    for x in range(width):
        for y in range(height):
            r = img_array[x,y][rc]
            g = img_array[x,y][gc]
            b = img_array[x,y][bc]
            img_array[x,y] = (r,g,b)
    return img
def to_sketch(img):
    width,height = img.size
    # 转灰度图
    img_gray = img.convert("L")
    # 反色
    img_invert = ImageOps.invert(img_gray)
    # 高斯模糊
    img_gaussian = img_invert.filter(ImageFilter.GaussianBlur(5))
    # 颜色减淡
    for x in range(width):
        for y in range(height):
            pos = (x,y)
            # 获取灰度图与高斯图的像素值
            A = img_gray.getpixel(pos)
            B = img_gaussian.getpixel(pos)
            # 颜色减淡公式
            img_gray.putpixel(pos,min(int(A+A*B/(255-B+1)),255))  # 手动防止除以零
    return img_gray
def to_char(img):
    # 图片宽高
    width, height = (70, 70)
    # 灰度图
    img = img.convert("L").resize((width, height))
    # 70 level 字符串
    ASCII_HIGH = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. """
    # 灰度转字符串
    txt = ""
    for y in range(width):
        for x in range(height):
            pos = (x,y)
            gray = img.getpixel(pos)  # 0-255
            index = int(gray/256*70)
            txt += ASCII_HIGH[index] + " "
        txt += "\n"
    # 字符串转图片
    img_new = Image.new("RGB",(width*12,height*15),'white')
    draw = ImageDraw.Draw(img_new)
    draw.text((0,0), txt, fill='black', font=ImageFont.truetype("fly_net_char_img_font",10))
    return img_new.resize((width*12,width*12)).convert("RGBA")
def page1():
    st.header("欢迎来到飞·网！")
    st.subheader("在这里，你可以尽情浏览内容，或听听音乐，或与其他人聊天，或尽情畅玩，一起嗨皮吧！")
    bgm()
def page2():
    st.write(":blue[图片处理]")
    st.write(":icecream:一个有一点简单的图片处理小程序:icecream:")
    image_filters()
def dict():
    st.write("输入英文单词，该词典可以帮你查询它的中文意思~")
    with open("data\words_space.txt",'r',encoding="utf-8") as f:
        word_list = f.read().split('\n')
        for i in range(len(word_list)):
            word_list[i]=word_list[i].split("#")
        words_dict = {}
        for i in word_list:
            words_dict[i[1]]=[int(i[0]),i[2]]#单词：[编号，意思]

        with open("data\check_out_times.txt","r",encoding='utf-8') as f:
            times_list = f.read().split('\n')
        for i in range(len(times_list)):
            times_list[i] = times_list[i].split('#')
        times_dict = {}
        for i in times_list:
            times_dict[int(i[0])] = int(i[1])#编号：次数
    word=st.text_input("在这里键入你要搜索的单词：")
    if st.button("收起"):
        d.close()
    while word:
        if word in words_dict:
            st.write(words_dict[word])
            n = words_dict[word][0]
            if n in times_dict:
                times_dict[n] += 1
            else:
                times_dict[n] = 1
            if times_dict[n] >= 50:
                st.write("该单词已经被查询了：",times_dict[n],"次，是个高频词汇呦！")
            else:
                st.write("该单词已经被查询了：",times_dict[n],"次")
            with open("data\check_out_times.txt","w",encoding="utf-8") as f:
                msg = ''
                for k, v in times_dict.items():
                    msg += str(k) + "#" + str(v) + '\n'
                msg = msg[:-1]
                f.write(msg)
            if word == 'python':
                st.code('''
                            #彩蛋！这个网站就是用python这门语言编写的呦！下面是词典页面的源代码：
                            st.write(':blue[词典]')
                            st.write("输入英文单词，该词典可以帮你查询它的中文意思~")
                        with open("data\words_space.txt",'r',encoding="utf-8") as f:
                            word_list = f.read().split('\n')
                        for i in range(len(word_list)):
                            word_list[i]=word_list[i].split("#")
                            words_dict = {}
                        for i in word_list:
                            words_dict[i[1]]=[int(i[0]),i[2]]#单词：[编号，意思]
    
                        with open("data\check_out_times.txt","r",encoding='utf-8') as f:
                            times_list = f.read().split('\n')
                        for i in range(len(times_list)):
                            times_list[i] = times_list[i].split('#')
                        times_dict = {}
                        for i in times_list:
                            times_dict[int(i[0])] = int(i[1])#编号：次数
                    word=st.text_input("在这里键入你要搜索的单词：")
                    while word:
                        if word in words_dict:
                            st.write(words_dict[word])
                            n = words_dict[word][0]
                            if n in times_dict:
                                times_dict[n] += 1
                            else:
                                times_dict[n] = 1
                            if times_dict[n] >= 50:
                                st.write("该单词已经被查询了：",times_dict[n],"次，是个高频词汇呦！")
                            else:
                                st.write("该单词已经被查询了：",times_dict[n],"次")
                            with open("data\check_out_times.txt","w",encoding="utf-8") as f:
                                msg = ''
                                for k, v in times_dict.items():
                                    msg += str(k) + "#" + str(v) + '\n'
                                msg = msg[:-1]
                                f.write(msg)
                        ''')
            
            if word == 'balloon' or word == 'birthday':
                st.balloons()
            if word == 'snow' or word == 'winter':
                st.snow()
            if word == 'win' or word == 'success':
                st.success("恭喜你又触发了一个彩蛋！")
            break
        else:
            st.text("""检索错误。
                    可能是你输入的单词不合规范，也可能是你要查找的单词不在词典中。
                    如果是后者，请联系我们，我们会尽快加入缺失的内容""")
            break
def page3():
    st.write(':blue[发现]')
    st.write("在这里，发现实用小工具！")
    dict = st.button("词典")
    if dict:
        dict()
    if st.button("世界地图"):
        st.write(":sunglasses:超详细的世界地图~快来看看你的家乡在哪？:sunglasses:")
        st.map()
    if st.button("图表绘制器"):
        pass
def page4():
    st.write(":blue[聊天室]")
    st.write("这就是聊天室啦，在这里你可以留言，与他人聊天，享受交往的乐趣。现在开始吧！")
    with open("data\leave_messages.txt",'r',encoding='utf-8') as f:
        msg_list = f.read().split('\n')
    for i in range(len(msg_list)):
        msg_list[i] = msg_list[i].split("#")
    for i in msg_list:
        if i[1] == '阿短':
            with st.chat_message('🌽'):
                st.write(i[1],"：",i[2])
        elif i[1] == '编程猫':
            with st.chat_message('🌈'):
                st.write(i[1],"：",i[2])
        elif i[1] == '制作组':
            with st.chat_message('🧑‍🔬'):
                st.write(i[1],"：",i[2])
        elif i[1] == '匿名用户1':
            with st.chat_message('🧨'):
                st.write(i[1],"：",i[2])
        elif i[1] == '匿名用户2':
            with st.chat_message('🧧'):
                st.write(i[1],"：",i[2])
        elif i[1] == '匿名用户3':
            with st.chat_message('🪄'):
                st.write(i[1],"：",i[2])
    name = st.selectbox("你的名字是：",['阿短','编程猫','制作组','匿名用户1','匿名用户2','匿名用户3'])
    new_msg = st.text_input("冒个泡吧：")
    if st.button('发送'):
        msg_list.append([str(int(msg_list[-1][0])+1),name,new_msg])
        with open("data\leave_messages.txt",'w',encoding='utf-8') as f:
            msg=''
            for i in msg_list:
                msg += i[0] + '#' + i[1] + '#' + i[2] + '\n'
            msg = msg[:-1]
            f.write(msg)
def page5():
    st.write(":blue[常用网站]")
    st.write("你可以在这里找到平时常用的各大网站，如果在本站逛累了就可以来这里哦")
    col1,col2,col3,col4 = st.columns([1,1,1,1])
    with col1:
        st.link_button('百度','https://www.baidu.com/')
        st.link_button('bilibili','https://www.bilibili.com/')
        st.link_button('中国天气网','https://www.xiaohongshu.com/')
        st.link_button('酷狗音乐','https://www.kugou.com/')
        st.link_button('python','https://www.python.org/')
    with col2:
        st.link_button('Bing','https://www.bing.com/')
        st.link_button('抖音','https://www.douyin.com/')
        st.link_button('中国科技网','http://www.stdaily.com/')
        st.link_button('网易云音乐','https://music.163.com/')
        st.link_button('Github','https://github.com/')
    with col3:  
        st.link_button('360','https://hao.360.com/')
        st.link_button('快手','https://www.kuaishou.com/')
        st.link_button('中国教育考试网','https://www.neea.edu.cn/')
        st.link_button('QQ音乐','https://y.qq.com/')
        st.link_button('Steam','https://store.steampowered.com/')
    with col4:
        st.link_button('Google','https://www.google.com/')
        st.link_button('小红书','https://www.xiaohongshu.com/')
        st.link_button('中国新闻网','https://www.chinanews.com.cn/')
        st.link_button('酷我音乐','http://www.kuwo.cn/')
        st.link_button('4399','https://www.4399.com/')
def page6():
    st.write(":blue[音乐分站]")
    st.write("这是本站的音乐分站，大家有喜欢听的音乐可以上传到这里，我们会把他它加载到网站上，让大家随时收听哦~")
    st.write("我先来！众所周知，作者很喜欢玩植物大战僵尸，所以作者推荐的也是植物大战僵尸的BGM，当然不是原版，是B站一位叫虽华的UP主改编的,废话不多说，上音乐！")
    with open('music\Grasswalk.mp3','rb') as f:
        m = f.read()
    st.audio(m,format='audio/mp3',start_time=0)
    st.write("植物大战僵尸白天BGM")
    with open('music\Moongrains.mp3','rb') as f:
        m = f.read()
    st.audio(m,format='audio/mp3',start_time=0)
    st.write("植物大战僵尸夜晚BGM")
    with open('music\Watery Graves.mp3','rb') as f:
        m = f.read()
    st.audio(m,format='audio/mp3',start_time=0)
    st.write("植物大战僵尸泳池BGM")
    with open('music\Rigor Mormist.mp3','rb') as f:
        m3= f.read()
    st.audio(m,format='audio/mp3',start_time=0)
    st.write("植物大战僵尸迷雾BGM")
    with open('music\Graze the Roof.mp3','rb') as f:
        m = f.read()
    st.audio(m,format='audio/mp3',start_time=0)
    st.write("植物大战僵尸屋顶BGM")
    with open('music\Brainiac Maniac.mp3','rb') as f:
        m = f.read()
    st.audio(m,format='audio/mp3',start_time=0)
    st.write("植物大战僵尸僵王BGM")
    with open('music\Crazy Dave.mp3','rb') as f:
        m = f.read()
    st.audio(m,format='audio/mp3',start_time=0)
    st.write("植物大战僵尸主界面BGM")
    with open('music\Zen Garden.mp3','rb') as f:
        m = f.read()
    st.audio(m,format='audio/mp3',start_time=0)
    st.write("植物大战僵尸禅境花园BGM")
    # st.write("如果大家有推荐的音乐，可以在下面上传哦~")
    # uploaded_music = st.file_uploader("在这里上传你要上传的音乐",type=['mp3','wav'])
    # if uploaded_music:
    #     sound_name = uploaded_music.name
    #     sound_type = uploaded_music.type
    #     sound = AudioSegment.from_file(uploaded_music)
    #     sound.export(f'music\{sound_name}',format=sound_type)
def page7():
    st.write(":blue[游戏分站]")
    st.write("这里是游戏分站，这里有许多免费的游戏资源，你可以下载它们，然后免费畅玩。")
    global PVZ_file,PVZ_95_file,PVZ_β_file,PVZ_E_file,PVZ_wuming_file,PVZ_random_file,PVZ_Rouge_file,PVZ_xiugaiqi_file,raft_file
    col1,col2,col3,col4 = st.columns([2,1,2,1])
    with open(PVZ_file,"rb") as file:
        btn = st.download_button(
            label="PVZ原版下载（汉化第二版图鉴加强）",
            data=file,
            file_name="PVZ.rar",
            mime="application/octet-stream"
        )
    with open(PVZ_95_file,"rb") as file:
        btn = st.download_button(
            label="PVZ95版下载",
            data=file,
            file_name="PVZ_95.rar",
            mime="application/octet-stream"
        )
    with open(PVZ_β_file,"rb") as file:
        btn = st.download_button(
            label="PVZβ版v6.66下载",
            data=file,
            file_name="PVZ_β.rar",
            mime="application/octet-stream"
        )
    with open(PVZ_E_file,"rb") as file:
        btn = st.download_button(
            label="PVZ E版支线v1.9.7下载",
            data=file,
            file_name="PVZ_E支.rar",
            mime="application/octet-stream"
        )
    with open(PVZ_wuming_file,"rb") as file:
        btn = st.download_button(
            label="PVZ无名版v1.2.4下载",
            data=file,
            file_name="PVZ_无名.rar",
            mime="application/octet-stream"
        )
    with open(PVZ_random_file,"rb") as file:
        btn = st.download_button(
            label="PVZ随机模仿者版下载",
            data=file,
            file_name="PVZ_随机.rar",
            mime="application/octet-stream"
        )
    with open(PVZ_Rouge_file,"rb") as file:
        btn = st.download_button(
            label="PVZ_Rougev1.4.5下载",
            data=file,
            file_name="PVZ_Rouge.rar",
            mime="application/octet-stream"
        )
    st.write("说明：这个是植物大战僵尸的衍生作品，由B站一坨馬制作")
    with open(PVZ_xiugaiqi_file,"rb") as file:
        btn = st.download_button(
            label="PVZ修改器（包括PvZ_Tools和Winkle_雪线制作的我是僵尸布阵器）",
            data=file,
            file_name="PVZ_修改器.rar",
            mime="application/octet-stream"
        )
    # with open(raft_file,"rb") as file:
    #     btn = st.download_button(
    #         label="木筏求生v1.0.9下载",
    #         data=file,
    #         file_name="raft.rar",
    #         mime="application/octet-stream"
    #     )
    st.text("下载打开后如果出错，请移动到其他文件夹并以管理员权限运行！！！")
    st.write("注意：下载完成后将压缩包全部选中解压，这样可以将文件解压到同一个路径，还很方便。另外下载完后一定要将游戏目录下带有中文的文件夹全部改成英文，否则玩游戏是可能会报错导致死机！！！")
    st.write("解压步骤：将分卷压缩包全部选中后右击，选择‘全部解压缩’（或者‘解压文件...’）,等待解压完成即可")
    st.write("目前只有这些游戏，更多游戏在持续更新中，敬请期待！")
def page8():
    st.write(":blue[世界地图]")
    
def page9():
    st.write(":blue[意见反馈]")
    advice = ''
    st.write("为我们的开发提出意见，以帮助我们更好的完善本站。")
    # st.write("1.在访问本站的过程中，您对本站的视觉效果如何评价？")
    # c = st.radio('',['非常不满意','不满意','还行','满意','非常满意'])
    # if st.button("确定"):
    #     if c == '非常不满意':
    #         advice += 'A'
    #     elif c == '不满意':
    #         advice += 'B'
    #     elif c == '还行':
    #         advice += 'C'
    #     elif c == '满意':
    #         advice += 'D'
    #     elif c == '非常满意':
    #         advice += 'E'
    # st.write("2.在访问本站的过程中，您对本站的实用性如何评价？")
    # c1 = st.radio('',['非常不满意','不满意','还行','满意','非常满意'])
    # if st.button("确定"):
    #     if c1 == '非常不满意':
    #         advice += 'A'
    #     elif c1 == '不满意':
    #         advice += 'B'
    #     elif c1 == '还行':
    #         advice += 'C'
    #     elif c1 == '满意':
    #         advice += 'D'
    #     elif c1 == '非常满意':
    #         advice += 'E'
    # st.write("3.在访问本站的过程中，您对本站的交互性如何评价？")
    # c2 = st.radio('',['非常不满意','不满意','还行','满意','非常满意'])
    # if st.button("确定"):
    #     if c2 == '非常不满意':
    #         advice += 'A'
    #     elif c2 == '不满意':
    #         advice += 'B'
    #     elif c2 == '还行':
    #         advice += 'C'
    #     elif c2 == '满意':
    #         advice += 'D'
    #     elif c2 == '非常满意':
    #         advice += 'E'
    st.write("请给出您的综合评价：")
    c3 = st.radio('',['非常不满意','不满意','还行','满意','非常满意'])
    if st.button("确定"):
        if c3 == '非常不满意':
            advice += 'A'
        elif c3 == '不满意':
            advice += 'B'
        elif c3 == '还行':
            advice += 'C'
        elif c3 == '满意':
            advice += 'D'
        elif c3 == '非常满意':
            advice += 'E'
    ad = st.text_input("如果您还有其他的建议，请写在下面：")
    if st.button('提交'):
        advice += ad
        print(advice)
if web == '兴趣推荐':
    page1()
elif web == '图片处理':
    page2()
elif web == '发现':
    page3()
elif web == '聊天室':
    page4()
elif web == '常用网站':
    page5()
elif web == '影音专区':
    page6()
elif web == '游戏专区':
    page7()
elif web == '世界地图':
    page8()
elif web == '设置':
    page9()


