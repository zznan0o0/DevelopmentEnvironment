import sys
import xlrd
import random
import calendar
import datetime

from OpeartingDB import OpeartingDB
# from ExcelWriter import ExcelWriter
from CSVWriter import GenCSV


class RandomContract:
  def __init__(self, month_money):
    self._workbook = xlrd.open_workbook(excel_data_path)
    self._sheets = self._workbook.sheets()

    self._curtainSheet = self._sheets[0]
    self._factorySheet = self._sheets[1]
    self._specSheet = self._sheets[2]
    self._accessoriesSheet = self._sheets[3]
    self._technologySheet = self._sheets[4]

    self._curtainCol = self._curtainSheet.col_values(0)
    self._factoryCol = self._factorySheet.col_values(0)
    self._specColH = self._specSheet.col_values(0, start_rowx=1)
    self._specColW = self._specSheet.col_values(1, start_rowx=1)
    self._accessoriesCol = self._accessoriesSheet.col_values(0)
    self._technologyCol = self._technologySheet.col_values(0)

    self._monthMoney = month_money

    self._contractNoList = []
    self._orderNoList = []

    self._opeartingDB = OpeartingDB()
    self._connect, self._cursor = self._opeartingDB.connectionMysql('atjubodb')
    self._userDict = self.getUserData()
    self._opeartingDB.closeAll()


  def getUserData(self):
    sql = "select ID, Tel, LinkMan, Address, Company from U_User where ID in (%s)" % self._opeartingDB.getWhereInString(self._curtainCol + self._factoryCol)
    self._cursor.execute(sql)
    user_data = self._cursor.fetchall()

    user_dict = {}

    for item in user_data:
      user_dict[str(item['ID'])] = item

    return user_dict


  def randomContractPrice(self):
    contract_rule = rule['Contract']
    if self._monthMoney <= contract_rule['MaxTotalPrice']:
      contract_price = self._monthMoney
      self._monthMoney = 0
      return contract_price

    contract_price = random.uniform(contract_rule['MinTotalPrice'], contract_rule['MaxTotalPrice'])
    contract_price = round(contract_price, 2)
    self._monthMoney -= contract_price

    return contract_price

  def randomUnitPrice(self):
    order_rule = rule['Order']
    unit_price = random.uniform(order_rule['MinUnitPrice'], order_rule['MaxUnitPrice'])
    unit_price = round(unit_price, 2)
    return unit_price

  def randomTime(self):
    contract_rule = rule['Contract']
    monthRange = calendar.monthrange(year, month)[1]
    day = random.randint(1, monthRange)
    hour = random.randint(contract_rule['MinHour'], contract_rule['MaxHour'])
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    create_time = "%s-%s-%s %s:%s:%s" % (year, month, day, hour, minute, second)
    return create_time

  def randomPayTime(self, create_time):
    contract_rule = rule['Contract']
    
    day = random.randint(contract_rule['MinPayDay'], contract_rule['MaxPayDay'])
    hour = random.randint(contract_rule['MinHour'], contract_rule['MaxHour'])
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    create_stamp = datetime.datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')
    pay_stamp = create_stamp + datetime.timedelta(days=day, hours=hour, minutes=minute, seconds=second)
    pay_time = pay_stamp.strftime("%Y-%m-%d %H:%M:%S")

    return pay_time

  def randomContractNo(self, create_time):
    create_stamp = datetime.datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')
    time_str = datetime.datetime.strftime(create_stamp, "%Y%m%d%H%M%S")
    contractNo = '30' + time_str + str(random.randint(0, 9999)).zfill(4)

    return contractNo


  def randomContract(self):
    rule_constract = rule['Contract']

    curtain_id = str(int(random.choice(self._curtainCol)))
    factory_id = str(int(random.choice(self._factoryCol)))
    total_price = self.randomContractPrice()
    # unit_price = self.randomUnitPrice()
    # total_area = total_price / unit_price
    create_time = self.randomTime()
    pay_time = self.randomPayTime(create_time)
    contractNo = self.randomContractNo(create_time)

    airbnb_price = random.randint(rule_constract['AirbnbPrice'][0], rule_constract['AirbnbPrice'][1])

    while contractNo in self._contractNoList:
      contractNo = self.randomContractNo(create_time)

    self._contractNoList.append(contractNo)

    # glass_accessories = random.choice(self._accessoriesCol)
    # technology = random.choice(self._technologyCol)

    contract_dict = {
      "CurtainID": curtain_id,
      "FactoryID": factory_id,
      "TotalPrice": total_price,
      "availableMoney": total_price,
      # "UnitPrice": unit_price,
      # "TotalArea": total_area,
      "CreateTime": create_time,
      "PayTime": pay_time,
      "ContractNo": contractNo,
      "TotalArea": 0,
      "AirbnbPrice": airbnb_price
      # "GlassAccessories": glass_accessories,
      # "Technology": technology,
    }

    return contract_dict

  def genContractList(self):
    contract_list = []
    contract_rule = rule['Contract']

    while self._monthMoney >= contract_rule['MinTotalPrice']:
      contract_list.append(self.randomContract())

    return contract_list

  def randomOrderID(self, create_time):
    contract_rule = rule['Contract']
    order_rule = rule['Order']

    day = random.randint(order_rule['MinDelayDay'], order_rule['MaxDelayDay'])
    hour = random.randint(contract_rule['MinHour'], contract_rule['MaxHour'])
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    create_stamp = datetime.datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')
    order_create_stamp = create_stamp + datetime.timedelta(days=day, hours=hour, minutes=minute, seconds=second)
    order_create_time = datetime.datetime.strftime(order_create_stamp, "%Y%m%d%H%M%S")
    order_create_time2 = datetime.datetime.strftime(order_create_stamp, "%Y-%m-%d %H:%M:%S")
    order_id = '70' + order_create_time + str(random.randint(0, 9999)).zfill(4)
    return order_id, order_create_time2

  def randomOrderItem(self, contract_dict, identifiter, order_dict):
    order_rule = rule['Order']
    chip = random.randint(order_rule['MinChipCount'], order_rule['ManChipCount'])
    glass_accessories = random.choice(self._accessoriesCol)
    technology = random.choice(self._technologyCol)
    unit_price = self.randomUnitPrice()

    length = len(self._specColW)
    spec_index = random.randint(0, length-1)
    width = self._specColW[spec_index]
    height = self._specColH[spec_index]
    single_area = width * height / 1000 / 1000
    total_area = single_area * chip
    item_total_price = unit_price * total_area

    if item_total_price > contract_dict['availableMoney']:
      chip = int(contract_dict['availableMoney'] / single_area / unit_price)
      total_area = single_area * chip
      item_total_price = unit_price * total_area

    contract_dict['availableMoney'] -= item_total_price

    contract_dict['TotalArea'] += total_area
    order_dict["TotalArea"] += total_area
    order_dict["TotalPrice"] += item_total_price

    item_dict = {
      "Chips": chip,
      "GlassAccessories": glass_accessories,
      "Technology": technology,
      "UnitPrice": unit_price,
      "Width": width,
      "Height": height,
      "Area": total_area,
      "TotalPrice": item_total_price,
      "SingleArea": single_area,
      "Identifiter": identifiter
    }

    return item_dict


  def randomOrder(self, contract_dict):
    order_rule = rule['Order']
    order_dict = {
      "TotalArea": 0,
      "TotalPrice": 0
    }

    identifiter_head = ''.join(random.sample(order_rule['Letter'], 2))

    order_id, create_time = self.randomOrderID(contract_dict['CreateTime'])
    while order_id in self._orderNoList:
      order_id, create_time = self.randomOrderID(contract_dict['CreateTime'])

    item_length = random.randint(order_rule['MinItemCount'], order_rule['MaxItemCount'])
    item_list = []

    for index in range(item_length):
      if contract_dict['availableMoney'] > order_rule['MaxUnitPrice']:
        identifiter_index = str(index + 1).zfill(3)
        identifiter = identifiter_head + identifiter_index
        item_list.append(self.randomOrderItem(contract_dict, identifiter, order_dict))

    order_dict["OrderID"] = order_id
    order_dict["OrderItem"] = item_list
    order_dict["CreateTime"] = create_time
    return order_dict

  def genOrderList(self, contract_dict):
    order_rule = rule['Order']
    order_list = []


    while contract_dict['availableMoney'] > order_rule['MaxUnitPrice']:
      order_list.append(self.randomOrder(contract_dict))

    contract_dict['OrderList'] = order_list
    return contract_dict

  def addOrderList(self, contract_list):
    for item in contract_list:
      self.genOrderList(item)

    return contract_list



if __name__ == '__main__':
  # month_money = float(sys.argv[1]) * 1000 * 1000
  # year = sys.argv[2]
  # month = sys.argv[3]

  month_money = float(3) * 10000 * 10000
  year = 2018
  month = 4

  excel_data_path = 'data/data.xlsx'

  rule = {
    'Contract': {
      "MinTotalPrice": 500 * 10000,
      "MaxTotalPrice": 1500 * 10000,
      "MinHour": 8,
      "MaxHour": 17,
      "MinPayDay": 11,
      "MaxPayDay": 13,
      "AirbnbPrice": (50000, 200000)
    },

    "Order": {
      "MinUnitPrice": 100,
      "MaxUnitPrice": 300,
      "MinItemCount": 3,
      "MaxItemCount": 10,
      "MinChipCount": 1,
      "ManChipCount": 100,
      "MinDelayDay": 1,
      "MaxDelayDay": 10,
      "Letter": 'abcdefghijklmnopqrstuvwxyz'
    }
  }
  randomContract = RandomContract(month_money)
  contract_list = randomContract.genContractList()
  contract_list = randomContract.addOrderList(contract_list)

  genCSV = GenCSV(randomContract._userDict)
  genCSV.genCSV(contract_list)
  # excelWriter = ExcelWriter()
  # excelWriter.save('download', contract_list)
