import sys

sys.path.append("./")

import pandas as pd
from datetime import datetime, timedelta
from google_calendar_api.control import CalendarControl
from datetime import datetime
import pickle
from event import CoupleEvent
from datetime import datetime


def make_time(date, time, all_day_event, flag="start"):
    time, d = time.split(" ")
    add_hour, add_minutes = [int(i) for i in time.split(":")]

    if d == "PM":
        add_hour += 12
    else:
        pass
    date_ = datetime.strptime(date, "%m/%d/%Y")
    dateTime = date_ + timedelta(hours=add_hour, minutes=add_minutes)
    timeZone = "Asia/Seoul"

    time_info = {"dateTime": dateTime.isoformat(), "timeZone": timeZone}
    if all_day_event:
        del time_info["dateTime"]
        if flag == "start":
            time_info["date"] = date_.strftime("%Y-%m-%d")
        else:
            time_info["date"] = date_.strftime("%Y-%m-%d")
            # time_info['date'] = (date_ + timedelta(days=1)).strftime("%Y-%m-%d")

    return time_info


if __name__ == "__main__":
    date_of_dating = "20220212"
    couple_event = CoupleEvent(date_of_dating=date_of_dating)

    # couple_event.make_anniversary(period=100)
    # couple_event.make_anniversary(period=365)

    # events = {"본인생일" :
    #         {"날짜" : "0101" , "설명" : "내 생일(필수)"},
    # }
    # couple_event.add_new_events(events)
    # event_details = {
    #     "100일" :
    #         {"Location" : "좋은 장소","Private" : True},
    #     "200일" :
    #         {"Location" : "좋은 장소","Private" : True},
    #     "300일" :
    #         {"Location" : "좋은 장소","Private" : True},
    # }
    # google_canlender_template = couple_event.make_google_calender_template(event_details=event_details)
    google_canlender_template = couple_event.make_google_calender_template(event_details={})
    couple_event.to_csv(google_canlender_template, "./google_calender_template_v0.csv", os="windows")

    CC = CalendarControl()
    google_calendar_df = pd.read_csv("./google_calender_template_v0.csv", encoding="cp949")

    google_calendar_df_ = google_calendar_df.copy()
    google_calendar_df_["start"] = google_calendar_df.apply(
        lambda x: make_time(x["Start Date"], x["Start Time"], x["All Day Event"], flag="start"), axis=1
    )
    google_calendar_df_["end"] = google_calendar_df.apply(
        lambda x: make_time(x["End Date"], x["End Time"], x["All Day Event"], flag="end"), axis=1
    )
    google_calendar_df_["visibility"] = google_calendar_df["Private"].apply(
        lambda x: "private" if x is True else "default"
    )
    google_calendar_df_ = google_calendar_df_.drop(
        ["Start Date", "End Date", "All Day Event", "Start Time", "End Time", "Private"], axis=1
    )
    google_calendar_df_.columns = ["summary", "description", "location", "start", "end", "visibility"]

    event_result_list = []
    for idx, body in google_calendar_df_.iterrows():
        body = dict(body)
        print(body)
        body["reminders"] = {
            "overrides": [{"method": "email", "minutes": 60 * 24 * 2}, {"method": "popup", "minutes": 60 * 24}],
            "useDefault": False,
        }
        
        ## 캘린더에 등록
        event_result = CC.create_event(calendarId="primary", body=body)
        if event_result is None :
            continue 
        else :
            event_result_list.append(event_result)
    else:
        print("캘린더에 등록하였습니다.")
        with open("./event_result.pkl", "wb") as wb:
            pickle.dump(event_result_list, wb)
        for i in event_result_list :
            
            event_id = i["id"]
            CC.delete_event(calendarId="primary",eventId=event_id)
        else :
            print("모두 제거 하였습니다.")