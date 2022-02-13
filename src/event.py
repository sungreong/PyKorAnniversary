from datetime import datetime
from datetime import timedelta

import pandas as pd
from typing import Mapping
import os, sys

dirname = os.path.dirname(__file__)
sys.path.append(dirname)
from constant import GOOGLE_CALENDER_COLS, GOOGLE_CALENDER_FUNCS, GOOGLE_CALENDER_MAPS, EVENT_DAYS, EVENT_COLS


class CoupleEvent(object):
    def __init__(self, date_of_dating=None):
        if date_of_dating is None:
            pass
        else:
            self.date_of_dating = self._get_date_to_str(date_of_dating)
        self.events = pd.DataFrame(EVENT_DAYS, columns=EVENT_COLS)
        self.events = self._transform_date(self.events)

    def replace_event_table(self, events):
        self.events = events

    def get_events(self, d_days=True):
        self._preprocess()
        if d_days:
            events = self.events.copy()
            events["D-Days"] = (events["날짜"] - self.get_today()).apply(
                lambda x: f"D-{x.days+1}" if x.days + 1 > 0 else "Terminate"
            )
            return events
        else:
            return self.events

    def add_new_events(self, events: Mapping[str, Mapping[str, str]] = {}):
        new_events = []
        for event_name, event_desc in events.items():
            new_event = {"이벤트": event_name, "날짜": event_desc["날짜"], "설명": event_desc["설명"]}
            new_events.append(new_event)

        new_df = self._transform_date(pd.DataFrame(new_events))
        self.events = pd.concat([self.events, new_df], axis=0)
        self._preprocess()

    def _transform_date(self, df: pd.DataFrame):
        df_ = df.copy()
        current_year = self.get_today().year
        df_["날짜"] = df["날짜"].apply(lambda x: datetime.strptime(f"{current_year}{x}", "%Y%m%d"))
        return df_

    def _preprocess(self):
        self._drop_duplicated()
        self._sort_by_date()
        self._reset_index()

    def _reset_index(self):
        self.events = self.events.reset_index(drop=True)

    def _drop_duplicated(self):
        self.events = self.events.drop_duplicates()

    def _sort_by_date(self):
        self.events = self.events.sort_values(by=["날짜"])

    def _get_date_to_str(self, string_date_Ymd="%Y%m%d"):
        return datetime.strptime(string_date_Ymd, "%Y%m%d")

    def add_days(self, date: datetime, number_of_day: int):
        return date + timedelta(number_of_day)

    def get_today(self):
        today = datetime.today()
        return today

    def get_current_year(self):
        today = self.get_today()
        current_year_first_day = today.replace(month=1, day=1)
        return current_year_first_day

    def get_next_year(self):
        today = self.get_today()
        next_year_first_day = today.replace(today.year + 1, month=1, day=1)
        return next_year_first_day

    def make_anniversary(self, period: int = 100):

        new_date = self.date_of_dating
        current_year_first_day = self.get_current_year()
        next_year_first_day = self.get_next_year()

        number_of_periods = 0
        current_year_event_collection = []
        while True:
            number_of_periods += period
            new_date = self.add_days(new_date, period)
            if (new_date > current_year_first_day) & (new_date < next_year_first_day):

                if number_of_periods % 365 == 0:
                    event_year = int(number_of_periods / 365)
                    event = {"날짜": new_date, "이벤트": f"{event_year}주년", "설명": f"{event_year}주년(필수)"}
                else:
                    event = {"날짜": new_date, "이벤트": f"{number_of_periods}일", "설명": f"{number_of_periods}일"}
                current_year_event_collection.append(event)
            else:
                if new_date > next_year_first_day:
                    break
        new_df = pd.DataFrame(current_year_event_collection)
        self.events = pd.concat([self.events, new_df], axis=0)

    def make_google_calender_template(
        self, private: bool = True, all_day_event: bool = True, event_details: Mapping[str, Mapping[str, str]] = {}
    ):
        self._preprocess()
        google_sheets = []
        for _, row in self.events.iterrows():
            one_line = {}
            event_name = row.get("이벤트")
            for key, lists in GOOGLE_CALENDER_MAPS.items():
                for v in lists:
                    func = GOOGLE_CALENDER_FUNCS[v]
                    one_line[v] = func(row.get(key))
            else:
                one_line["All Day Event"] = all_day_event
                one_line["Private"] = private
                one_line["Start Time"] = "00:00 AM"
                one_line["End Time"] = "00:00 PM"
                if event_name in event_details:
                    event_info = event_details[event_name]
                    for key, value in event_info.items():
                        if key in GOOGLE_CALENDER_FUNCS:
                            func = GOOGLE_CALENDER_FUNCS[key]
                            one_line[key] = func(value)

            for key in GOOGLE_CALENDER_COLS:
                if key in one_line:
                    continue
                else:
                    one_line[key] = None
            else:
                google_sheets.append(one_line)
        else:
            google_template = pd.DataFrame(google_sheets)
            return google_template[GOOGLE_CALENDER_COLS]

    def to_csv(self, df: pd.DataFrame, path: str, os: str = "windwos"):
        os_type = {"windows": "cp949", "linux": "utf-8"}
        df.to_csv(path, encoding=os_type.get(os, "linux"), index=False)
