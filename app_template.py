from dash import Dash, html, dcc, dash_table
import pandas as pd
from dash.exceptions import PreventUpdate
from dash_extensions import Download
from dash.dependencies import Input, Output, State
import io

app = Dash(__name__)

from collections import OrderedDict

data = OrderedDict(
    [
        ("Date", ["2015-01-01", "2015-10-24", "2016-05-10", "2017-01-10", "2018-05-10", "2018-08-15"]),
        ("Region", ["Montreal", "Toronto", "New York City", "Miami", "San Francisco", "London"]),
        ("Temperature", [1, -20, 3.512, 4, 10423, -441.2]),
        ("Humidity", [10, 20, 30, 40, 50, 60]),
        ("Pressure", [2, 10924, 3912, -10, 3591.2, 15]),
    ]
)

df = pd.DataFrame(OrderedDict([(name, col_data * 10) for (name, col_data) in data.items()]))


table = dash_table.DataTable(
    id="table_id",
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict("rows"),
    row_selectable="single",
    fixed_rows={"headers": True, "data": 0},
    fixed_columns={"headers": True, "data": 0},
    page_size=10,
    virtualization=True,
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
)

table_div = html.Div(
    [
        html.H1("Table"),
        Download(id="download"),
        html.Button("Save", id="save-button"),
        html.Div("Press button to save data at your desktop", id="output-1"),
        table,
    ]
)


@app.callback(Output("download", "data"), Input("save-button", "n_clicks"), State("table_id", "data"))
def download_as_csv(n_clicks, table_data):
    df = pd.DataFrame.from_dict(table_data)
    if not n_clicks:
        raise PreventUpdate
    download_buffer = io.StringIO()
    df.to_csv(download_buffer, index=False)
    download_buffer.seek(0)
    return dict(content=download_buffer.getvalue(), filename="some_filename.csv")


app.layout = html.Div(
    [
        html.Div(
            children=[
                html.Label("Dropdown"),
                dcc.Dropdown(["New York City", "Montréal", "San Francisco"], "Montréal"),
                html.Br(),
                html.Label("Multi-Select Dropdown"),
                dcc.Dropdown(
                    ["New York City", "Montréal", "San Francisco"], ["Montréal", "San Francisco"], multi=True
                ),
                html.Br(),
                html.Label("Radio Items"),
                dcc.RadioItems(["New York City", "Montréal", "San Francisco"], "Montréal"),
            ],
            style={"padding": 10, "flex": 1},
        ),
        html.Div(
            children=[
                html.Label("Checkboxes"),
                dcc.Checklist(["New York City", "Montréal", "San Francisco"], ["Montréal", "San Francisco"]),
                html.Br(),
                html.Label("Text Input"),
                dcc.Input(value="MTL", type="text"),
                html.Br(),
                html.Label("Slider"),
                dcc.Slider(
                    min=0,
                    max=9,
                    marks={i: f"Label {i}" if i == 1 else str(i) for i in range(1, 6)},
                    value=5,
                ),
                table_div,
            ],
            style={"padding": 10, "flex": 1},
        ),
    ],
    style={"display": "flex", "flex-direction": "row"},
)

if __name__ == "__main__":
    app.run_server(debug=True)
