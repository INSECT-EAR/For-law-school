# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 20:25:39 2024

@author: INSECT EAR 【小红书号】1161453270
*版权所有，供学习交流使用，禁止用于商业用途，转载请注明来源。
"""

import re
import streamlit as st

st.title('法学引注格式自动转换-测试版')
string=st.text_area(label='请输入原引文格式：',height=8)
raw_string_list=string.strip().split('\n')
string_list=[]
result_list=[]


for line in raw_string_list: #初步加工原始列表中的每一行
    line=re.sub(r'^\[\d*\]','',line,re.M) #删除引文开头处序号
    line=re.sub(r'DOI.*$','',line,re.M) #删除引文结尾处DOI号
    line=line.replace('：', ':').replace('，', ',').replace('。', '.').replace(' ', '') 
    #替换可能存在的全角字符
    string_list.append(line) #将完成加工的引文加入新列表中以便后续调用

if st.button('开始转换'):
    
    for line in string_list: #逐项检索新列表中的元素，根据文献类型标识识别对应格式并进行转换
        if line.find('[J]')>0: #匹配期刊论文引文格式
            pattern=re.compile(r'^([^\.]*)\.([^\.]*)\.([^\,.]*),?([\d-]*),?(\d*)?\(?(\d*)?\)?:?([\d-]*)?\.$',re.M)
            #利用正则表达式提取引文中的作者、标题、文献来源、出版年份、期数及页码
            match=pattern.search(line)
            
            if match:
                author=str(match.group(1)).replace(',', '、') #提取作者
                title=re.sub(r'\[.\]', '',str(match.group(2))) #提取文章标题，并删除其中的文献类型标识
                title=title.replace('《', '〈').replace('》', '〉') #将标题中的双书名号换成单书名号
                source=str(match.group(3)) #提取文献来源
                year=str(match.group(4))[0:4] #提取出版年份，删除出版日期后可能存在的月、日
                volume=str(match.group(5)).lstrip('0') #提取卷数
                period=str(match.group(6)).lstrip('0') #提取期数
                pages=str(match.group(7)).lstrip('0') #提取页码
                if pages and volume:
                    result_list.append('{0}：《{1}》，载《{2}》{3}年第{4}卷第{5}期，第{6}页。'.format(author,title,source,year,volume,period,pages))
                elif pages:
                    result_list.append('{0}：《{1}》，载《{2}》{3}年第{4}期，第{5}页。'.format(author,title,source,year,period,pages))
                elif volume:
                    result_list.append('{0}：《{1}》，载《{2}》{3}年第{4}卷第{5}期。'.format(author,title,source,year,volume,period))
                else:
                    result_list.append('{0}：《{1}》，载《{2}》{3}年第{4}期。'.format(author,title,source,year,period))
            else:
                result_list.append('无法识别的期刊论文格式')
                
        elif line.find('[M]')>0: #匹配图书引文格式
            pattern=re.compile(r'^([^\.]*)\.([^\.]*)\.([^\,.:]*):?([\d\.-]*)?$')
            #利用正则表达式提取引文中的作者、书名、出版社及出版年份
            match=pattern.search(line)
            
            if match:
                author=str(match.group(1)).replace(',', '、')
                book_name=re.sub(r'\[.\]', '',str(match.group(2)))
                book_name=book_name.replace('《', '〈').replace('》', '〉')
                publisher=str(match.group(3))
                year=str(match.group(4))[0:4]
                result_list.append('{0}：《{1}》，{2}：{3}年版。'.format(author,book_name,publisher,year))
            else:
                result_list.append('无法识别的图书格式')
                
        elif line.find('[D]')>0: #匹配学位论文引文格式
            pattern=re.compile(r'^([^\.]*)\.([^\.]*).([^\.,]*),(\d*).$',re.M)
            #利用正则表达式提取引文中的作者、标题、学校及学位授予年份
            match=pattern.search(line)
            
            if match:
                author=str(match.group(1))
                title=re.sub(r'\[.\]', '',str(match.group(2)))
                title=title.replace('《', '〈').replace('》', '〉')
                source=str(match.group(3))
                year=str(match.group(4))
                result_list.append('{0}：《{1}》，{2}{3}年博士论文。'.format(author,title,source,year))
                #默认引用的学位论文为博士论文，欲引用硕士论文请手动更改
            else:
                result_list.append('无法识别的学位论文格式')
                
        elif line.find('[N]')>0:
            pattern=re.compile(r'^([^\.]*)\.([^\.]*)\.([^\.,]*),([\d-]*)\(([\d\w]*)\)\.$',re.M)
            #利用正则表达式提取引文中的作者、标题、报刊来源、出版日期及页码
            match=pattern.search(line)
            
            if match:
                author=str(match.group(1)).replace(',', '、')
                title=re.sub(r'\[.\]', '',str(match.group(2)))
                title=title.replace('《', '〈').replace('》', '〉')
                source=str(match.group(3))
                pubdate=str(match.group(4))
                if pubdate.find('-')>0:
                    pubdate=pubdate.split('-') #将出版时间拆解为年月日
                    year=pubdate[0]
                    month=pubdate[1].lstrip('0')
                    day=pubdate[2].lstrip('0')
                pages=match.group(5).lstrip('0')
                if type(pubdate)==list:
                    result_list.append('{0}：《{1}》，载《{2}》{3}年{4}月{5}日，第{6}版。'.format(author,title,source,year,month,day,pages))
                else:
                    result_list.append('{0}：《{1}》，载《{2}》{3}，第{4}版。'.format(author,title,source,pubdate,pages))
                    #若原引文出版时间未以“yyyy-mm-dd”形式排列，请用户手动调整
            else:
                result_list.append('无法识别的报纸格式')
                    
        else:
            result_list.append('未检索到有效的文献类型标识符，请检查原引文格式的有效性。')
        
for line in result_list:
    st.markdown(line)
 #以分行形式输出结果列表的每一项