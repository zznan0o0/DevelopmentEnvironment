# -*- coding: utf-8 -*-  


from reportlab.pdfgen.canvas import Canvas  
from reportlab.pdfbase import pdfmetrics  
from reportlab.pdfbase.cidfonts import UnicodeCIDFont  
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image,Table,TableStyle
import time

def rpt():
    story=[]
    stylesheet=getSampleStyleSheet()
    normalStyle = stylesheet['Normal']

    curr_date = time.strftime("%Y-%m-%d", time.localtime())

    #标题：段落的用法详见reportlab-userguide.pdf中chapter 6 Paragraph
    rpt_title = '<para autoLeading="off" fontSize=15 align=center><b><font face="STSong-Light">XX项目日报%s</font></b><br/><br/><br/></para>' %(curr_date)
    story.append(Paragraph(rpt_title,normalStyle)) 

    text = '''<para autoLeading="off" fontSize=8><font face="STSong-Light" >程度定义：</font><br/>
    <font face="STSong-Light" color=red>1.Blocker：指系统无法执行。</font><br/><font face="STSong-Light" fontsize=7>例如：系统无法启动或退出等</font><br/>
    <font face="STSong-Light" color=orange>2.Critical：指系统崩溃或严重资源不足、应用模块无法启动或异常退出、无法测试、造成系统不稳定。</font><br/>
    <font face="STSong-Light" fontsize=7>例如：各类崩溃、死机、应用无法启动或退出、按键无响应、整屏花屏、死循环、数据丢失、安装错误等
    </font><br/>
    <font face="STSong-Light" color=darkblue>3.Major：指影响系统功能或操作，主要功能存在严重缺陷，但不会影响到系统稳定性、性能缺陷</font><br/><font face="STSong-Light" fontsize=7>例如：功能未做、功能实现与需求不一致、功能错误、声音问题、流程不正确、兼容性问题、查询结果不正确、性能不达标等
    </font><br/>
    <font face="STSong-Light" color=royalblue>4.Minor：指界面显示类问题</font><br/>
    <font face="STSong-Light" fontsize=7>例如：界面错误、边界错误、提示信息错误、翻页错误、兼容性问题、界面样式不统一、别字、排列不整齐，字体不符规范、内容、格式、滚动条等等
    </font><br/>
    <font face="STSong-Light" color=grey>5.Trivial：本状态保留暂时不用</font><br/>
    </para>'''
    story.append(Paragraph(text,normalStyle))

    text = '<para autoLeading="off" fontSize=9><br/><br/><br/><b><font face="STSong-Light">五、BUGLIST：</font></b><br/></para>'
    story.append(Paragraph(text,normalStyle))

   
    #表格数据：用法详见reportlab-userguide.pdf中chapter 7 Table
    component_data= [['模块', '', '', '',''],
    ['标记','bug-1','Major','some wrong','open','unresolved'],
    ['','bug-1','Major','some wrong','closed','fixed'], 
    ]
    #创建表格对象，并设定各列宽度
    component_table = Table(component_data, colWidths=[20,50,50, 150, 90, 90])
    #添加表格样式
    component_table.setStyle(TableStyle([
    # ('FONTSIZE',(0,0),(-1,-1),6),#字体大小
    # # ('SPAN',(0,0),(3,0)),#合并第一行前三列
    # ('BACKGROUND',(0,0),(-1,0), colors.lightskyblue),#设置第一行背景颜色
    # ('SPAN',(-1,0),(-2,0)), #合并第一行后两列
    # ('ALIGN',(-1,0),(-2,0),'RIGHT'),#对齐
    # ('VALIGN',(-1,0),(-2,0),'MIDDLE'),  #对齐
    # ('LINEBEFORE',(0,0),(0,-1),0.1,colors.grey),#设置表格左边线颜色为灰色，线宽为0.1
    # ('TEXTCOLOR',(0,1),(-2,-1),colors.royalblue),#设置表格内文字颜色
    ('GRID',(0,0),(-1,-1),0.5,colors.grey),#设置表格框线为红色，线宽为0.5
    ]))
    story.append(component_table)

    doc = SimpleDocTemplate('3.pdf')
    doc.build(story)

if __name__ == '__main__':
    rpt()