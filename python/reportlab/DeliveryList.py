# -*- coding: utf-8 -*-  
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.graphics.barcode import code39, code128, code93
from reportlab.pdfbase import pdfmetrics  
from reportlab.pdfbase.cidfonts import UnicodeCIDFont  
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image,Table,TableStyle, PageBreak
from reportlab.lib.units import mm


class DeliveryList:
  def __init__(self):
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
    stylesheet = getSampleStyleSheet()
    self._normalStyle = stylesheet['Normal']
    stylesheet.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY));
    self._justifyStyle = stylesheet['Justify']
    self._story = []

  def appendParagraph(self, element):
    self._story.append(Paragraph(element, self._normalStyle))

  def createDoc(self, lading_data, owner_name, file_name, isFinace=False):
    # 标题
    title = '''
      <para autoLeading="off" fontSize=15 align=center>
        <b>
          <font face="STSong-Light">%s送货清单</font>
        </b>
        <br /><br />
      </para>
    ''' % (lading_data['seller_name'])

    self.appendParagraph(title)

    barcode_val = file_name

    barcode = code128.Code128(value=barcode_val, barHeight=8 * mm)
    self._story.append(barcode)

    barcode_context = '''
      <para autoLeading="off" fontSize=9 face="STSong-Light" align=left>
        送货单号: %s &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 日期: %s
        <br />
      </para>
    ''' % (barcode_val, lading_data['effective_date'])

    self.appendParagraph(barcode_context)

    table_data = [
      ['收货单位', lading_data['buyer_name'], '', '', '', '', '订单号', lading_data['order_id'], ''],
      ['起运地', lading_data['depot_address'], '', '', '', '', '目的地', lading_data['delivery_address'], ''],
      ['车牌号', lading_data['plate_number'], '', '', '', '', '司机信息', '', ''],
      ['提货方式', lading_data['way_of_receiving'], '', '', '', '', '收款方式', lading_data['way_of_paid'], ''],
      ['品牌', '品类', '等级', '厚度', '规格', '包装', '片数/包', '包数 ',  '面积(㎡)', '备注'],

      # ['南玻', '白玻', '一等品', '4', '3660 * 1900', '裸包', '45', '6 ', '', '1877.58', '18.4' if isFinace else '***', '34547.47' if isFinace else '***'],
      # ['南玻', '其他', '一等品', '4', '3660 * 1900', '裸包', '45', '6 ', '', '1877.58', '18.4' if isFinace else '***', '34547.47' if isFinace else '***']
    ]
    
    for item in lading_data['lading_item_list']:
      str_spec =  str(int(item['width'])) + ' * ' + str(int(item['height']))
      table_data.append([
        item['brand'], 
        item['category'], 
        item['level'], 
        str(float(item['thickness'])), 
        str_spec, 
        item['packing'], 
        str(item['chip']), 
        str(item['packing_number']), 
        str(item['area']), 
        ''
      ])

    table_style = [
      ('FONTNAME',(0,0),(-1,-1),'STSong-Light'),
      ('GRID',(0,0),(-1,-1),0.5,colors.grey),

      ('SPAN',(1,0),(5,0)),
      ('SPAN',(7,0),(9,0)),

      ('SPAN',(1,1),(5,1)),
      ('SPAN',(7,1),(9,1)),

      ('SPAN',(1,2),(5,2)),
      ('SPAN',(7,2),(9,2)),

      ('SPAN',(1,3),(5,3)),
      ('SPAN',(7,3),(9,3)),

      ('SPAN',(0,-2),(9,-2)),

      ('SPAN',(0,-1),(4,-1)),
      ('SPAN',(5,-1),(9,-1)),
    ]

    

    table_data += [
      ['备注: 以上回执单用于证明发货、提货以及到货签收事实，便于供需双方对账之用。请收货方签字盖章后返回一份签字件'],
      ['送货人(签字)', '', '', '', '', '收货人(签字)', '', '', '', ''],
    ]

    order_item_table = Table(table_data, colWidths=[50, 45, 45, 35, 65, 45, 50, 35, 45, 145])
    order_item_table.setStyle(TableStyle(table_style))

    self._story.append(order_item_table)

    self.appendParagraph('<para autoLeading="off"><br /><br /><br /></para>')


  def build(self, lading_data, path, lading_id):
    file_name = 'DB' + lading_id
    file_type = 'pdf'
    path_all = path + file_name + '.' + file_type
    doc = SimpleDocTemplate(path_all, topMargin=0, leftMargin=10, rightMargin=10, bottomMargin=0)

    self.createDoc(lading_data, '财务', file_name)
    self.createDoc(lading_data, '运营', file_name)

    # self._story.append(PageBreak())

    self.createDoc(lading_data, '司机', file_name)
    doc.build(self._story)

    return {'file_name': file_name, 'file_path': path, 'file_type': file_type, 'path_all': path_all}


