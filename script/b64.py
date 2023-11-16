#_-_ coding: utf-8 _-_
'''
    项目名:Base64编码解码
    作者:ZZhangC
    创作时间:2020.4.18-2020.4.19
    原项目地址:https://github.com/ZZhangC/Python-Base64EncodeAndDecode/blob/master/b64.py
'''

#base64字母表
b64_table = {
'0':'A',
'1':'B',
'2':'C',
'3':'D',
'4':'E',
'5':'F',
'6':'G',
'7':'H',
'8':'I',
'9':'J',
'10':'K',
'11':'L',
'12':'M',
'13':'N',
'14':'O',
'15':'P',
'16':'Q',
'17':'R',
'18':'S',
'19':'T',
'20':'U',
'21':'V',
'22':'W',
'23':'X',
'24':'Y',
'25':'Z',
'26':'a',
'27':'b',
'28':'c',
'29':'d',
'30':'e',
'31':'f',
'32':'g',
'33':'h',
'34':'i',
'35':'j',
'36':'k',
'37':'l',
'38':'m',
'39':'n',
'40':'o',
'41':'p',
'42':'q',
'43':'r',
'44':'s',
'45':'t',
'46':'u',
'47':'v',
'48':'w',
'49':'x',
'50':'y',
'51':'z',
'52':'0',
'53':'1',
'54':'2',
'55':'3',
'56':'4',
'57':'5',
'58':'6',
'59':'7',
'60':'8',
'61':'9',
'62':'+',
'63':'/'
}
b64_table1 = {
'A':'0',
'B':'1',
'C':'2',
'D':'3',
'E':'4',
'F':'5',
'G':'6',
'H':'7',
'I':'8',
'J':'9',
'K':'10',
'L':'11',
'M':'12',
'N':'13',
'O':'14',
'P':'15',
'Q':'16',
'R':'17',
'S':'18',
'T':'19',
'U':'20',
'V':'21',
'W':'22',
'X':'23',
'Y':'24',
'Z':'25',
'a':'26',
'b':'27',
'c':'28',
'd':'29',
'e':'30',
'f':'31',
'g':'32',
'h':'33',
'i':'34',
'j':'35',
'k':'36',
'l':'37',
'm':'38',
'n':'39',
'o':'40',
'p':'41',
'q':'42',
'r':'43',
's':'44',
't':'45',
'u':'46',
'v':'47',
'w':'48',
'x':'49',
'y':'50',
'z':'51',
'0':'52',
'1':'53',
'2':'54',
'3':'55',
'4':'56',
'5':'57',
'6':'58',
'7':'59',
'8':'60',
'9':'61',
'+':'62',
'/':'63'
}



#自定义函数:加密，形参s，转成str类型存储在str中
def b64encode(s):
    s1 = str(s)
    addcount = 0
    #字符串的长度
    lenth = len(s1)
    #三个临时变量，tmp用来储存二进制版字符串ascii码，tmp2储存所有字符串，tmp3存储十进制的转换后的代码，res存储结果
    tmp = []
    tmp2 = ''
    tmp3 = []
    res = ''
    #把输入的字符串转换成ascii码，再转换成二进制，再把二进制的前缀去掉，储存在tmp中。如果位数不够的就在前面添加0
    for i in range(lenth):
        tmp.append(bin(int(ord(s1[i]))))
        tmp[i] = tmp[i][2:]
        if len(tmp[i]) != 8:
            while len(tmp[i]) != 8:
                tmp[i] = '0' + tmp[i]
    #把字符串全部存储在tmp2中，不足二十四位的在后面添加0
    for i in tmp:
        tmp2 += i
    if len(tmp2) % 24 != 0:
        while len(tmp2) % 24 != 0:
            tmp2 += '0'
            addcount += 1
    #把字符串6个一组存储在tmp3中，并把二进制转换成十进制
    for i in range(int(len(tmp2)/6)):
        tmp3.append(tmp2[i*6:i*6+6])
        tmp3[i] = int(tmp3[i],2)
    #把数字转换成字母，并添加'='
    for i in tmp3:
        res += b64_table[str(i)]
    if addcount / 6 > 1:
        addcount = int(addcount)
        i = int(addcount/6)
        eqtmp = '=' * i
        res = res[0:-i] + eqtmp
    #返回res
    return res




#自定义函数:解密，形参s，转成str类型存储在str中
def b64decode(s):
    s1= str(s)
    tmp = []
    tmp2 = []
    tmp3 = ''
    tmp4 = []
    tmp5 = []
    res = ''
    c = s1.count('=') * 6
    #把'='转成字母A，再把字母转成数字
    s1 = s1.strip('=')
    s1 += 'A' * int(c/6)
    #把字符转成数字，存储在tmp中，再转成二进制，存储在tmp2中。不足六位的补足
    for i in range(len(s1)):
        tmp.append(b64_table1[s1[i]])
        tmp[i] = bin(int(tmp[i]))
        tmp2.append(str(tmp[i]))
        tmp2[i] = tmp2[i][2:]
        if len(tmp2[i]) != 6:
            while len(tmp2[i]) != 6:
                tmp2[i] = '0' + tmp2[i]
        
    #把字符串连接起来，存储在tmp3中
    for i in range(len(s1)):
        tmp3 += tmp2[i]
    #去掉多余的0
    tmp3 = tmp3[0:len(tmp3)-c+1]
    c = int(len(tmp3) / 8) * 8 +1 
    tmp3 = tmp3[0:c]
    #把二进制数8个为一组存储在tmp4中再转换成十进制数
    for i in range(int(len(tmp3)/8)):
        tmp4.append(tmp3[i*8:i*8+8])
        tmp4[i] = int(tmp4[i],2)
    #把十进制数作为ascii码转成字符存储在tmp5中
    for i in tmp4:
        tmp5.append(chr(i))
    #把字符串联起来返回
    for i in tmp5:
        res += i
    return res



if __name__ == '__main__':
    string = ' '
    string = input("string:")
    res = b64encode(string)
    print(res)
    res = b64decode(res)
    print(res)
