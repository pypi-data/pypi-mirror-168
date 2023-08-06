from datetime import datetime

import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import Dash, Input, Output, dcc, html
from dash.exceptions import PreventUpdate
from plotly import graph_objects as go
from plotly.subplots import make_subplots

from bacorakel.controller import list_all_ports
from bacorakel.state import state

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.SUPERHERO, dbc_css],
)

server = app.server


def build_banner():
    """Build the banner content."""
    return dbc.Container(html.H2("BACorakel"))


def build_content():
    """Build the main app content."""
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Row(html.Label("Empty keg weight")),
                            dbc.Row(
                                dcc.Slider(
                                    id="empty-keg-weight",
                                    min=0,
                                    max=20,
                                    step=0.5,
                                    value=state.keg_weight_empty,
                                    marks={i: i for i in range(21)},
                                    tooltip={
                                        "placement": "top",
                                        "always_visible": True,
                                    },
                                )
                            ),
                            dbc.Row(html.Label("Keg capacity")),
                            dbc.Row(
                                dcc.Slider(
                                    id="keg-capacity",
                                    min=20.5,
                                    max=50,
                                    step=0.5,
                                    value=state.keg_capacity,
                                    marks={20.5: "20.5L", 30: "30L", 50: "50L"},
                                    tooltip={
                                        "placement": "top",
                                        "always_visible": True,
                                    },
                                )
                            ),
                            dbc.Row(html.Label("Scales device")),
                            dbc.Row(
                                dcc.Dropdown(
                                    id="scales-device",
                                    options=[],
                                    value=state.scales.device,
                                )
                            ),
                            dbc.Row(html.Label("Arduino device")),
                            dbc.Row(
                                dcc.Dropdown(
                                    id="arduino-device",
                                    options=[],
                                    value=state.arduino.device,
                                )
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            dbc.Row(
                                daq.Tank(
                                    id="keg-percentage",
                                    min=0,
                                    max=100,
                                    value=state.keg_fraction * 100,
                                    showCurrentValue=True,
                                    units="%",
                                    label="Keg percentage remaining",
                                    scale=dict(interval=10),
                                    width=250,
                                )
                            ),
                        ]
                    ),
                ]
            ),
            dbc.Row(className="p-5", children=[build_graph()]),
            dcc.Interval(id="trigger", interval=1000, n_intervals=0),
            html.Div(id="sentinel", style=dict(display="none")),
        ],
    )


def build_graph():
    return dcc.Graph(
        config=dict(staticPlot=False, editable=False, displayModeBar=False),
        id="graph-history",
        figure=get_history_figure(),
    )


def get_history_figure() -> go.Figure:
    data = state.history.data
    times = [datetime.fromtimestamp(m.time) for m in data]
    weights = [m.weight - state.keg_weight_empty for m in data]
    rates = [-m.rate for m in data]
    now = datetime.now()
    horizon = datetime.fromtimestamp(
        max(now.timestamp() - 300, data[0].time if len(data) else 0)
    )
    x_range = [horizon, now]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.update_layout(
        dict(
            uirevision=True,
            margin=dict(l=0, r=0, t=4, b=4, pad=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0.05)",
            xaxis=dict(range=x_range, title="Time"),
            yaxis=dict(
                title="Contents [L]",
                range=[
                    0,
                    60,
                ],
                nticks=7,
            ),
            yaxis2=dict(
                title="Rate [L/s]",
                range=[0.0, 0.6],
                nticks=7,
                showgrid=False,
            ),
            template="plotly_dark",
        )
    )
    fig.add_trace(go.Scatter(name="Contents", x=times, y=weights, mode="lines"))
    fig.add_trace(
        go.Scatter(name="Rate", x=times, y=rates, mode="lines"),
        secondary_y=True,
    )
    return fig


app.layout = html.Div(
    className="dbc p-5", children=[dbc.Row(build_banner()), dbc.Row(build_content())]
)


@app.callback(
    [
        Output("keg-percentage", "value"),
        Output("graph-history", "figure"),
        Output("scales-device", "options"),
        Output("arduino-device", "options"),
    ],
    [Input("trigger", "n_intervals")],
)
def reload_state(trigger):
    # Stop when we get to zero.
    if not trigger or int(trigger) < 1:
        raise PreventUpdate

    keg_percentage = round(state.keg_fraction * 100, 0)
    history_figure = get_history_figure()
    ports = [p.device for p in list_all_ports()]

    return (keg_percentage, history_figure, ports, ports)


@app.callback(
    [Output("sentinel", "children")],
    [
        Input("empty-keg-weight", "value"),
        Input("keg-capacity", "value"),
        Input("scales-device", "value"),
        Input("arduino-device", "value"),
    ],
)
def update_settings(weight_empty, keg_capacity, scales_device, arduino_device):
    state.keg_weight_empty = weight_empty
    state.keg_capacity = keg_capacity
    state.scales.device = scales_device
    state.arduino.device = arduino_device
    state.save(state.state_file)
    raise PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=True)
