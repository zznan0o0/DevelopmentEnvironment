from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code39, code128, code93
import reportlab.pdfbase.ttfonts
from reportlab.lib.units import mm

# mm = 1.75


reportlab.pdfbase.pdfmetrics.registerFont(reportlab.pdfbase.ttfonts.TTFont('simhei', 'pycode/SIMSUN.TTC')) 

class GenBarCodePDF:
  def __init__(self, pdf_id):
    self._canvas = canvas.Canvas(pdf_id)
    

  def drawBarCode(self, barcode_value, x, y):
    # barcode = code39.Extended39(barcode_value)
    barcode = code128.Code128(value=barcode_value, barHeight=15*mm)
    barcode.drawOn(self._canvas, x, y)

  def drawString(self, value, x, y):
    self._canvas.drawString(x, y, str(value).encode('utf-8')) 

  def drawContainer(self, data, col_index):
    marginLeft = 9
    marginBottom = 8
    marginTopPerRow = 57

    marginLeftPerCol = 20
    containWidth = 97

    rowMarginBottom = marginBottom + marginTopPerRow * int(col_index / 2)

    colMarginLeft = marginLeftPerCol + marginLeft + (containWidth if col_index % 2 == 0 else 0)

    self._canvas.setFont('simhei', 8)
    self.drawString('品牌: ' + str(data[1]), colMarginLeft * mm, (rowMarginBottom + 46) * mm)
    self.drawString('品类: ' + str(data[2]), colMarginLeft * mm, (rowMarginBottom + 42) * mm)
    self.drawString('级别: ' + str(data[3]), colMarginLeft * mm, (rowMarginBottom + 38) * mm)
    self.drawString('片数: ' + str(data[4]), colMarginLeft * mm, (rowMarginBottom + 34) * mm)
    self.drawString('规格: ' + str(data[5]), colMarginLeft * mm, (rowMarginBottom + 30) * mm)

    self._canvas.setFont('simhei', 10)
    self.drawBarCode(data[0], colMarginLeft * mm, (rowMarginBottom + 8) * mm)
    self.drawString(data[0], (colMarginLeft + 6) * mm, (rowMarginBottom + 3) * mm)

  def drawPage(self, data):
    barcode_num_per_page = 10
    length = len(data)
    surplus = length % barcode_num_per_page
    pages = int(length / barcode_num_per_page) + (1 if surplus > 0 else 0)

    for page_index in range(pages):
      

      row_start = page_index * barcode_num_per_page
      row_end = row_start
      if page_index == pages - 1 and surplus > 0:
        row_end += surplus
      else:
        row_end += barcode_num_per_page

      for col_index in range(row_start, row_end):
        self.drawContainer(data[col_index], col_index - row_start)
      self._canvas.showPage()

    self._canvas.save()

  def convertData(self, glass_tuple_list):
    tuple_list = []

    for item in glass_tuple_list:
      tuple_list.append((
        item[0],
        item[1],
        item[3],
        item[4],
        str(int(item[8])),
        str(int(item[5])) + ' * ' + str(int(item[6])) + ' * ' + str(float(item[7])) + 'mm'
      ))

    return tuple_list





if __name__ == '__main__':
  data = [('20180301102857229784301', '本溪玉晶', '白玻', '一等品', '30片', '3660 * 2440 * 6mm')]

  for i in range(15):
    data += data[0:1]


  pdf_path = '2018020103635.pdf'
  genBarCodePDF = GenBarCodePDF(pdf_path)
  genBarCodePDF.drawPage(data)

