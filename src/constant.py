EVENT_DAYS = [
    ["0114", "다이어리데이", "연인끼리 서로 일기장을 선물하는 날"],
    ["0119", "찜질방데이", "따뜻하게 보내는 날"],
    ["0214", "발렌타인데이", "친구나 연인 사이에 초콜릿을 선물하는 날"],
    ["0222", "커플데이", "2프로데이"],
    ["0303", "삼겹살데이", "삼겹살 먹는 날"],
    ["0314", "화이트데이", "친구나 연인 사이에 설탕을 선물하는 날"],
    ["0414", "블랙데이", "솔로들이 짜장면 먹는 날"],
    ["0503", "오삼데이", "오징어와 삼겹살을 먹는 오삼불고기 날"],
    ["0514", "로즈데이", "연인끼리 장미꽃을 선물하는 날"],
    ["0606", "고기데이", "고기먹는 날"],
    ["0614", "키스데이", "연인끼리 입맞춤을 나누는 날"],
    ["0702", "체리데이", "발음이 체리라서 체리 데이"],
    ["0714", "실버데이", "연인끼리 은반지를 선물하는 날"],
    ["0808", "팔팔데이", "라면먹는 날"],
    ["0814", "그린데이", "연인끼리 산림욕을 하며 무더위를 달래는 날"],
    ["0914", "포토데이", "연인끼리 함께 기념사진을 찍는 날"],
    ["0917", "고백데이", "이때 사귀면 크리스마스 100인 날"],
    ["1014", "와인데이", "연인끼리 함께 포도주를 마꼐는 날"],
    ["1114", "무비데이", "연인끼리 함께 영화를 보는 날"],
    ["1214", "허그데이", "연인끼리 서로 안아주는 날"],
    ["1225", "크리스마스", "크리스마스는 크리스마스"],
    ["1111", "뺴빼로데이", "뺴배로데이"],
]
EVENT_COLS = ["날짜", "이벤트", "설명"]

GOOGLE_CALENDER_COLS = [
    "Subject",
    "Start Date",
    "Start Time",
    "End Date",
    "End Time",
    "All Day Event",
    "Description",
    "Location",
    "Private",
]

import datetime

DateToStr = lambda x: x.strftime("%m/%d/%Y") if isinstance(x, (datetime.datetime,)) else x
ToStr = lambda x: str(x)
ToBool = lambda x: bool(x)


GOOGLE_CALENDER_FUNCS = {
    "Subject": ToStr,
    "Start Date": DateToStr,
    "End Date": DateToStr,
    "Start Time": ToStr,
    "End Time": ToStr,
    "All Day Event": ToBool,
    "Description": ToStr,
    "Location": ToStr,
    "Private": ToBool,
}


GOOGLE_CALENDER_MAPS = {"이벤트": ["Subject"], "날짜": ["Start Date", "End Date"], "설명": ["Description"]}
