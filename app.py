from datetime import date
from dash import Dash, html, dcc, dash_table
import pandas as pd
from dash.exceptions import PreventUpdate
from dash_extensions import Download
from dash.dependencies import Input, Output, State
import io, os, sys
from flask import request, Response

dirname = os.path.dirname(__file__)
sys.path.append(dirname)
from src.constant import GOOGLE_CALENDER_COLS, EVENT_COLS
from src.event import CoupleEvent

external_stylesheets = []

app = Dash(__name__, title="Anniversary", external_stylesheets=external_stylesheets)
app._favicon = "./calendar.ico"


d_day_table = dash_table.DataTable(
    id="event-table",
    columns=[{"name": i, "id": i} for i in EVENT_COLS],
    data=[{}],
    fixed_rows={"headers": True, "data": 0},
    fixed_columns={"headers": True, "data": 0},
    page_size=30,
    editable=True,
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    virtualization=True,
    row_selectable="multi",
    row_deletable=True,
    column_selectable="single",
    style_cell={
        "height": "auto",
        # all three widths are needed
        "minWidth": "180px",
        "width": "180px",
        "maxWidth": "180px",
        "whiteSpace": "normal",
    },
    style_table={"overflowY": "auto", "minWidth": "100%"},
    style_header={
        "overflow": "hidden",
        "textOverflow": "ellipsis",
        "maxWidth": 400,
    },
    fill_width=True,
    export_format="csv",
)


calendar_table = dash_table.DataTable(
    id="calendar-table",
    columns=[{"name": i, "id": i} for i in GOOGLE_CALENDER_COLS],
    data=[{}],
    fixed_rows={"headers": True, "data": 0},
    fixed_columns={"headers": True, "data": 0},
    page_size=30,
    editable=True,
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    virtualization=True,
    row_selectable="multi",
    row_deletable=True,
    column_selectable="single",
    style_cell={
        "height": "auto",
        # all three widths are needed
        "minWidth": "180px",
        "width": "180px",
        "maxWidth": "180px",
        "whiteSpace": "normal",
    },
    style_table={"overflowY": "auto", "minWidth": "100%"},
    style_header={
        "overflow": "hidden",
        "textOverflow": "ellipsis",
        "maxWidth": 400,
    },
    fill_width=True,
    export_format="csv",
)

event_table_div = html.Div(
    [
        html.H1("Event Table"),
        html.Label("Check D Day"),
        html.Br(),
        dcc.RadioItems(["True", "False"], "True", id="d-day-id"),
        html.Button("Click", id="event-table-button"),
        html.Br(),
        d_day_table,
    ]
)


calendar_table_div = html.Div(
    [
        html.H1("Google Calendar Table"),
        html.Button("Click", id="event-make-button"),
        html.Br(),
        # Download(id="event-download"),
        # html.Button("Save", id="event-save-button"),
        # html.Div("Press button to save data at your desktop", id="output-1"),
        calendar_table,
    ]
)

calendar_main_div = html.Div(
    children=[
        html.Label("Date of Dating"),
        html.Br(),
        dcc.Input(value="20220101", type="text", id="event-id"),
        html.Br(),
        html.Label("Anniversary (Period)"),
        html.Br(),
        dcc.Input(value="100,365", type="text", id="event-period"),
        html.Br(),
        event_table_div,
        html.Br(),
        calendar_table_div,
    ],
    style={"padding": 10, "flex": 1},
)


@app.callback(
    Output("calendar-table", "data"),
    [Input("event-make-button", "n_clicks")],
    [State("event-id", "value"), State("event-period", "value")],
)
def make_google_calendar(n_clicks, date_of_dating, event_period):
    if not n_clicks:
        raise PreventUpdate
    event_periods = [int(i) for i in event_period.split(",")]
    couple_event = CoupleEvent(date_of_dating=date_of_dating)
    for period in event_periods:
        couple_event.make_anniversary(period=period)
    google_canlender_template = couple_event.make_google_calender_template(event_details={})
    return google_canlender_template.to_dict("rows")


@app.callback(
    [Output("event-table", "data"), Output("event-table", "columns")],
    [Input("event-table-button", "n_clicks")],
    [State("event-id", "value"), State("event-period", "value"), State("d-day-id", "value")],
)
def make_google_calendar(n_clicks, date_of_dating, event_period, check_d_day):

    if not n_clicks:
        raise PreventUpdate
    check_d_day = eval(check_d_day)

    event_periods = [int(i) for i in event_period.split(",")]
    couple_event = CoupleEvent(date_of_dating=date_of_dating)
    for period in event_periods:
        couple_event.make_anniversary(period=period)
    event_table = couple_event.get_events(d_days=check_d_day)
    new_columns = [{"name": i, "id": i} for i in list(event_table)]
    return event_table.to_dict("rows"), new_columns


# 한글 깨짐 현상 해결 못함.
# @app.callback(
#     Output("event-download", "data"), Input("event-save-button", "n_clicks"), State("calendar-table", "data")
# )
# def download_as_csv(n_clicks, table_data):
#     df = pd.DataFrame.from_dict(table_data)
#     if not n_clicks:
#         raise PreventUpdate
#     download_buffer = io.StringIO()
#     csv = df.to_csv(download_buffer ,encoding="utf-8-sig", index=False)
#     download_buffer.seek(0)
#     return dict(content=download_buffer.getvalue(), filename="google_calendar_table.csv")


app.layout = html.Div(
    [calendar_main_div],
    style={"display": "flex", "flex-direction": "row"},
)

if __name__ == "__main__":
    app.run_server(debug=True)
