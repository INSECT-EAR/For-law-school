# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 20:25:39 2024

@author: INSECT EAR 【小红书号】1161453270
*版权所有，供学习交流使用，禁止用于商业用途，转载请注明来源。
"""

import streamlit as st
import re
import pyperclip

def switch_button(raw_string_list): #定义单击按钮后的转换函数
    string_list=[]
    show_list=[]
    result_list=[]
    
    for line in raw_string_list:
        line=re.sub(r'^\[\d*\]','',line,re.M) #删除引文开头处序号
        line=re.sub(r'DOI.*$','',line,re.M) #删除引文结尾处DOI号
        line=line.replace('：', ':').replace('，', ',').replace('。', '.')
        #替换可能存在的全角字符
        string_list.append(line)
    
    for line in string_list:
        if not line:
            pass
        elif re.search(r'[\u4e00-\u9fa5]', line):
            if line.find('[J]')>0: #匹配期刊论文引文格式
                pattern=re.compile(r'^([^\.]*)\.([^\.]*)\.([^\,.]*),?([\d-]*),?(\d*)?\(?(\d*)?\)?:?([+\d-]*)?\.$',re.M)
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
                        show_list.append('{0}：《{1}》，载《{2}》{3}年第{4}卷第{5}期，第{6}页。'.format(author,title,source,year,volume,period,pages))
                        result_list.append('{0}：《{1}》，载《{2}》{3}年第{4}卷第{5}期，第{6}页。'.format(author,title,source,year,volume,period,pages)) 
                    elif pages:
                        show_list.append('{0}：《{1}》，载《{2}》{3}年第{4}期，第{5}页。'.format(author,title,source,year,period,pages))
                        result_list.append('{0}：《{1}》，载《{2}》{3}年第{4}期，第{5}页。'.format(author,title,source,year,period,pages))
                    elif volume:
                        show_list.append('{0}：《{1}》，载《{2}》{3}年第{4}卷第{5}期。'.format(author,title,source,year,volume,period))
                        result_list.append('{0}：《{1}》，载《{2}》{3}年第{4}期，第{5}页。'.format(author,title,source,year,period,pages))
                    else:
                        show_list.append('{0}：《{1}》，载《{2}》{3}年第{4}期。'.format(author,title,source,year,period))
                        result_list.append('{0}：《{1}》，载《{2}》{3}年第{4}期。'.format(author,title,source,year,period))
                else:
                    show_list.append('无法识别的中文期刊论文格式')
            
            elif line.find('[M]')>0: #匹配图书引文格式
                pattern=re.compile(r'^([^\.]*)\.([^（\.]*)（?第?(\d*)版?）?\[M]\.([^\,.:]*):?([\d\.-]*)?$')
                #利用正则表达式提取引文中的作者、书名、出版社及出版年份
                match=pattern.search(line)
                
                if match:
                    author=str(match.group(1)).replace(',', '、')
                    book_name=re.sub(r'\[.\]', '',str(match.group(2)))
                    book_name=book_name.replace('《', '〈').replace('》', '〉')
                    edition=str(match.group(3))
                    publisher=str(match.group(4))
                    year=str(match.group(5))[0:4]
                    if edition:
                        show_list.append('{0}：《{1}》（第{2}版），{3}：{4}年版。'.format(author,book_name,edition,publisher,year))
                        result_list.append('{0}：《{1}》（第{2}版），{3}：{4}年版。'.format(author,book_name,edition,publisher,year))
                    else:
                        show_list.append('{0}：《{1}》，{2}：{3}年版。'.format(author,book_name,publisher,year))
                        result_list.append('{0}：《{1}》，{2}：{3}年版。'.format(author,book_name,publisher,year))
                else:
                    show_list.append('无法识别的中文图书格式')                    
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
                    show_list.append('{0}：《{1}》，{2}{3}年博士论文。'.format(author,title,source,year))
                    result_list.append('{0}：《{1}》，{2}{3}年博士论文。'.format(author,title,source,year))
                else:
                    show_list.append('无法识别的中文学位论文格式')
                    
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
                        show_list.append('{0}：《{1}》，载《{2}》{3}年{4}月{5}日，第{6}版。'.format(author,title,source,year,month,day,pages))
                        result_list.append('{0}：《{1}》，载《{2}》{3}年{4}月{5}日，第{6}版。'.format(author,title,source,year,month,day,pages))
                    else:
                        show_list.append('{0}：《{1}》，载《{2}》{3}，第{4}版。'.format(author,title,source,pubdate,pages))
                        result_list.append('{0}：《{1}》，载《{2}》{3}，第{4}版。'.format(author,title,source,pubdate,pages))
                        #若原引文出版时间未以“yyyy-mm-dd”形式排列，请用户手动调整。
                else:
                    show_list.append('无法识别的中文报纸格式')
                        
            else:
                show_list.append('仅支持带有[J][M][D][N]四种标识符的中文引文识别。\n未检索到有效的文献类型标识符，请检查原引文格式的有效性。')
            
        else:
            if line.find('[J]')>0:
                pattern=re.compile(r'^([^\.]*)\.([^\.]*)\.([^\.,]*),(\d*),(\d*)\((\d*)\):?([\d-]*)?\.?$',re.M)
                match=re.search(pattern, line)
                if match:
                    author=str(match.group(1)).strip().replace(',', '&') #提取作者
                    title=re.sub(r'\[.\]', '',str(match.group(2)))
                    title=re.sub('(:)(.)',r'\1 \2',title) #防止引号后无空格时被markdown格式错误识别
                    title='*'+title.strip()+'*' #利用markdown的斜体功能将论文标题转为斜体格式
                    source=str(match.group(3)).strip() #提取文献来源
                    year=str(match.group(4))[0:4].strip()
                    volume=str(match.group(5)).strip()
                    period=str(match.group(6)).strip()
                    pages=str(match.group(7)).strip()
                    show_list.append('{0}, {1}, {2}, Vol.{3}:{4}, p.{5}({6}).'.format(author,title,source,volume,period,pages,year))
                    result_list.append('{0}, {1}, {2}, Vol.{3}:{4}, p.{5}({6}).'.format(author,title,source,volume,period,pages,year))

                else:
                    show_list.append('无法识别的外文期刊论文格式')
                    
            elif line.find('[M]')>0:
                pattern=re.compile(r'^([^\.]*)\.([^\.]*)\.([^\:]*):([\d-]*)\.?',re.M)
                match=re.search(pattern, line)
                if match:
                    author=str(match.group(1)).strip().replace(',', '&') #提取作者
                    title=re.sub(r'\[.\]', '',str(match.group(2)))
                    title=re.sub('(:)(.)',r'\1 \2',title) #防止引号后无空格时被markdown格式错误识别
                    title='*'+title.strip()+'*'
                    source=str(match.group(3)).strip()
                    year=str(match.group(4))[0:4].strip()
                    show_list.append('{0}, {1}, {2}, {3}.'.format(author,title,source,year))
                    result_list.append('{0}, {1}, {2}, {3}.'.format(author,title,source,year))

                else:
                    show_list.append('无法识别的外文图书格式')
                    
            else:
                show_list.append('仅支持带有[J][M]两种标识符的英文引文识别。\n未检索到有效的文献类型标识符，请检查原引文格式的有效性。')

    st.session_state.show=show_list
    st.session_state.result=result_list
     
def show_result(): #定义显示结果函数，将持续显示作为全局变量的session_state.result
    if st.session_state.show:
        for line in st.session_state.show:
            st.markdown(line)
st.header('GB/T格式——法学引注手册格式自动转换')
    
tab1,tab2=st.tabs([':gear: 转换器 ',':question: 帮助页 '])
     
if 'show' not in st.session_state:
    st.session_state.show=False

container = st.container()

# 使用st.markdown嵌入HTML和CSS来实现版权文字居中
with container:
    st.markdown(
        """
        <div style="text-align: center; position: fixed; bottom: 0; width: 50%; padding: 3px;">
            <span style="color: #808080; font-size: 10px;">
            <p style="margin: 20;">南京大学法学院 INSECT EAR     版权所有</p></span>
        </div>
        """,
        unsafe_allow_html=True
    )

with tab1:
    st.write('')
    st.write('')
    default_text="赵旭东.从资本信用到资产信用[J].法学研究,2003,(05):109-123.\n范健,王建文.公司法（第6版）[M].法律出版社:202408.\n胡云腾.正确把握认罪认罚从宽保证严格公正高效司法[N].人民法院报,2019-10-24(005).\nBeuthien V .Bürgerlichrechtliche Innengesellschaft – zurück damit ins Römische Recht?[J].Zeitschrift für Unternehmens- und Gesellschaftsrecht,2024,53(4):549-573."
    string=st.text_area('请在此处输入原引文格式',value=default_text,max_chars=20000)
        
    if st.button('开始转换'):
        raw_string_list=string.strip().split('\n')
        switch_button(raw_string_list)
    
    if st.button('复制结果'):    
        if st.session_state.result:
            st.info('已将转换结果复制到剪贴板')        
        pyperclip.copy('\n'.join(st.session_state.result))
        
    show_result()
    
with tab2:
    
    with st.expander('一、获取GB/T格式引文'):
        st.write('在知网上找到欲转引的论文后，点击直接复制“GB/T 7714-2015 格式引文”后的内容并粘贴至转换器中即可一键实现格式转换。转换器会自动去除序号和DOI号。\n\n转换器支持批量转换引文，此时请分行输入。')
    with st.expander('二、中文引文格式要求'):
        st.write('1、期刊格式\n\n作者.标题[J].期刊名,年份,卷数(期数):页码数.')
        st.write('2、图书格式\n\n作者.书名[M].出版社:出版时间.（出版年份应位于出版时间的前四位）')
        st.write('3、学位论文格式\n\n作者.标题[D].研究机构,年份.')
        st.write('4、报纸格式\n\n作者.标题[N].报刊名,发行时间(版数).')
        st.write('注：报纸的发行时间应以yyyy-mm-dd形式记录')
    with st.expander('三、外文引文格式要求'):
        st.write('1、期刊格式\n\n作者.标题[J].期刊名,年份,卷数(期数):页码数.')
        st.write('2、图书格式\n\n作者.书名[M].出版社:出版时间.（出版年份应位于出版时间的前四位）')
        st.write('注意：外文引文中作者名有缩写的应去掉缩写符号“.”，否则无法识别；\n\n输出的期刊名斜体格式无法通过剪贴板复制，请手动添加斜体或在网页上Ctrl+c自行复制。目前仅主要支持英文及德文的引文转换。')
    
