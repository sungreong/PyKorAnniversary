import os, sys

dirname = os.path.dirname(__file__)
sys.path.append(dirname)
from google_calendar_api.cal_setup import get_calendar_service
import googleapiclient
from copy import deepcopy

LIST_FUNC_ARGUMENT = dict(
    calendarId="primary",
    orderBy=None,
    showHiddenInvitations=None,
    timeMin=None,
    privateExtendedProperty=None,
    pageToken=None,
    updatedMin=None,
    singleEvents=None,
    alwaysIncludeEmail=None,
    showDeleted=None,
    sharedExtendedProperty=None,
    maxAttendees=None,
    syncToken=None,
    iCalUID=None,
    maxResults=None,
    timeMax=None,
    q=None,
    timeZone=None,
)

INSERT_FUNC_ARGUMENT = dict(
    calendarId="primary",
    body=None,
    sendNotifications=None,
    supportsAttachments=None,
    sendUpdates=None,
    conferenceDataVersion=None,
    maxAttendees=None,
)
UPDATE_FUNC_ARGUMENT = dict(
    calendarId="primary",
    eventId=None,
    body=None,
    sendNotifications=None,
    alwaysIncludeEmail=None,
    supportsAttachments=None,
    maxAttendees=None,
    conferenceDataVersion=None,
    sendUpdates=None,
)

DELETE_FUNC_ARGUMENT = dict(calendarId="primary", eventId=None, sendNotifications=None, sendUpdates=None)
from datetime import datetime , timedelta


class CalendarControl:
    def __init__(self):
        self.service = get_calendar_service()

    def create_event(self, calendarId, body, insert_func_dict={}):
        insert_args = self._update_dict(INSERT_FUNC_ARGUMENT, insert_func_dict)
        insert_args["calendarId"] = calendarId
        insert_args["body"] = body

        if self.check_event(body) :
            event_result = self.service.events().insert(**insert_args).execute()
            print("created event")
            print("id: ", event_result["id"])
            print("summary: ", event_result["summary"])
            return event_result
        else :
            print("중복되는 일정이 존재합니다")
            return None 
        

    def _update_dict(self, base, new):
        base = deepcopy(base)
        base.update(new)
        return base

    def get_event_list(self, calendarId, list_func_dict={}):
        list_args = self._update_dict(LIST_FUNC_ARGUMENT, list_func_dict)
        list_args["calendarId"] = calendarId
        events_result = self.service.events().list(**list_args).execute()
        return events_result

    def get_event(self, calendarId, iCaiUID):
        events_result = (
            self.service.events()
            .list(
                calendarId=calendarId,
                iCalUID=iCaiUID,
            )
            .execute()
        )
        events = events_result.get("items", [])
        if not events:
            print("No upcoming events found.")
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])
        return events

    def update_event(self, calendarId, eventId, body, update_func_dict={}):
        update_args = self._update_dict(UPDATE_FUNC_ARGUMENT, update_func_dict)
        update_args["calendarId"] = calendarId
        update_args["eventId"] = eventId
        update_args["body"] = body
        event_result = self.service.events().update(**update_args).execute()

        print("updated event")
        print("id: ", event_result["id"])
        print("summary: ", event_result["summary"])
        print("starts at: ", event_result["start"]["dateTime"])
        print("ends at: ", event_result["end"]["dateTime"])
        return event_result

    def delete_event(self, calendarId, eventId, delete_func_dict={}):
        delete_args = self._update_dict(DELETE_FUNC_ARGUMENT, delete_func_dict)
        delete_args["calendarId"] = calendarId
        delete_args["eventId"] = eventId
        try:
            self.service.events().delete(**delete_args).execute()
        except googleapiclient.errors.HttpError:
            print("Failed to delete event")

    def check_event(self,  body ) :
        ## 기존 일정과 새로운 일정간의 중복 여부 체크
        if "date" in body["start"]:
            check_date = datetime.strptime(body["start"]["date"], "%Y-%m-%d")
        else:
            check_date = datetime.fromisoformat(body["start"]["dateTime"])
        check_date = check_date - timedelta(days=1)
        list_dict = dict(timeMin=check_date.isoformat() + "Z", singleEvents=True, orderBy="startTime", maxResults=10)
        events = self.get_event_list(calendarId="primary", list_func_dict=list_dict)
        items = events["items"]
        if len(items) == 0:
            return True 
        else:
            subjects = [item["summary"] for item in items]
            if body["summary"] in subjects:
                return False 
            else :
                return True
        