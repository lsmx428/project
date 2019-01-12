#  -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.select import Select
import pandas as pd

# 定义常量
ALL_VALUE = '所有'
PROVINCE = 'Province'
CITY = 'City'

provinces = []

# 创建浏览器对象
driver = webdriver.Firefox()
url = ...  # 快递公司的网点查询网址
driver.get(url)
driver.implicitly_wait(20) # 设置一个超时等待时间

# 获取省份下拉框选项
province_options = driver.find_element_by_id('sheng').find_elements_by_tag_name('option')
for province in province_options: # provinces[0] = 全国
    provinces.append(province.text)

# 定义省份临时空列表，城市空列表，索引空列表
provinces_temp = []
cites_temp = []
index_temp = []

index = 1
len_province = len(provinces)  # 省份列表长度

# 获取省份及相关城市的列表
for p in range(1,len_province):

    province = provinces[p]
    sheng = driver.find_element_by_id("sheng")
    option = Select(sheng).select_by_visible_text(province)          # 获取“省”下拉框列表
    driver.find_element_by_xpath("//input[@value=' ']").click()   # 然后，点击“搜索”按钮
    city_options = driver.find_element_by_id('city').find_elements_by_tag_name('option') # 获取某省所对应的“城市”下拉框列表

    for c in city_options:
        if c.text != ALL_VALUE: # 不存储城市列表中，“所有”字段选项
            cites_temp.append(c.text)
            provinces_temp.append(province)
            index_temp.append(index)
            index += 1

# 把省、城市放入到DataFrame中
data = { PROVINCE: provinces_temp,
         CITY:cites_temp}
df = pd.DataFrame(data, columns=[PROVINCE,CITY],index=index_temp)
print(df)

# 电子表格输出
df.to_excel('excel_output.xls',sheet_name='city',index=False)
driver.quit()


