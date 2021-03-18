

from bs4 import BeautifulSoup 
import urllib.request as req

from GetHome.modules.house_data_manager import HouseInfo

def parse591(url):
    ret_house_info = HouseInfo()
    ret_house_info.source = url

    request = req.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    })

    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    ##########
    root = BeautifulSoup(data, "html.parser")
    info_box = root.find("div", class_="info-box")
    info_price = info_box.find("span", class_="info-price-num").string
    info_price_unit = info_box.find("span", class_="info-price-unit").string
    ret_house_info.price = info_price + info_price_unit

    ##########
    info_box_floor = root.find("div", class_="info-box-floor")
    info_box_floor_left = info_box_floor.find_all("div", class_="info-floor-left")
    for msg in info_box_floor_left:
        k = msg.find("div", class_="info-floor-value")
        v = msg.find("div", class_="info-floor-key")

        if v and k:
            v, k = v.text, k.text
            # print(v, k)
            if k == "屋齡":
                ret_house_info.age = v
            elif k == "格局":
                ret_house_info.house_pattern = v
            elif k == "權狀坪數":
                ret_house_info.ownership_size = v

    ##########
    info_box_addr = root.find("div", class_="info-box-addr")
    info_box_addr_content = info_box_addr.find_all("div", class_="info-addr-content")
    for content in info_box_addr_content:
        v = content.find("span", class_="info-addr-value")
        k = content.find("span", class_="info-addr-key")

        if v and k:
            v, k = v.text, k.text
            # print(k, v)
            if k == "樓層":
                ret_house_info.floors = v
            elif k == "朝向":
                ret_house_info.direction = v
            elif k == "社區":
                ret_house_info.apartment_complex = v
            elif k == "地址":
                ret_house_info.address = v

    ##########
    detail_house = root.find("section", class_=["detail-house", "navScroll", "detail-font-"])
    detail_house_items = detail_house.find_all("div", class_="detail-house-item")
    for item in detail_house_items:
        v = item.find("div", class_="detail-house-value")
        k = item.find("div", class_="detail-house-key")
        
        if v and k:
            v, k = v.text, k.text
            # print(k,v)
            if k == "型態":
                ret_house_info.building_type = v
            elif k == "主建物":
                ret_house_info.main_building_size = v
            elif k == "土地坪數":
                ret_house_info.land_size = v

    return ret_house_info
    