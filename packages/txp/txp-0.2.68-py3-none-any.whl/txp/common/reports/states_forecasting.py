import logging
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from PIL import Image
from typing import List, Dict, Union
from txp.common.config import settings
import txp.common.reports.section as sections
from prophet import Prophet
import pytz
import datetime
log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class StatesForecasting(sections.Plot2dSection):
    _color_map = {
        'OPTIMAL': '#3D62F6',
        'GOOD': '#79CF24',
        'OPERATIVE': '#F6F03D',
        'UNDEFINED': '#808080',
        'CRITICAL': '#F64F3D'
    }

    def __init__(
            self,
            tenant_id,
            section_id,
            start_datetime: str,
            end_datetime: str,
            axes_names: List[str],
            lines,
            **kwargs
    ):
        super(StatesForecasting, self).__init__(
            tenant_id, section_id, start_datetime, end_datetime,
            axes_names, lines, **kwargs
        )

    @classmethod
    def required_inputs(cls) -> List[sections.SectionInputEnum]:
        return [sections.SectionInputEnum.STATES]

    @classmethod
    def compute(cls, inputs: Dict[sections.SectionInputEnum, pd.DataFrame], section_event_payload: Dict) -> Dict:
        # Converts Data timestamp to datetime objects
        states_data = inputs[sections.SectionInputEnum.STATES]

        if not states_data.size:
            log.info(f"Not received states to compute {cls.__name__}")
            return {}

        states_data['observation_timestamp'] = (
            pd.to_datetime(states_data['observation_timestamp'], utc=True)
            .dt.tz_convert("America/Mexico_City")
        )

        # Groups by hrs
        conditions_by_hrs = cls._transform_conditions_to_hours(states_data)
        forecasting_data = cls.getting_forecasting_data(conditions_by_hrs)

        lines: List[cls.Plot2DLine] = []
        for state in cls._color_map.keys():
            if state in conditions_by_hrs:
                forecasting_x_axis = forecasting_data["ds"].to_list()
                forecasting_y_axis = forecasting_data[f"forecasting_{state}"].to_list()

                str_x_axis = conditions_by_hrs['observation_timestamp'].astype(str)
                x_axis = str_x_axis.to_list()
                y_axis = conditions_by_hrs[state].to_list()

                lines.append(
                    cls.Plot2DLine(
                        x_axis, y_axis, state
                    )
                )
                lines.append(
                    cls.Plot2DLine(
                        forecasting_x_axis, forecasting_y_axis, f"forecasting_{state}"
                    )
                )


        section: StatesForecasting = cls(
            section_event_payload['tenant_id'],
            section_event_payload['section_id'],
            section_event_payload['start_datetime'],
            section_event_payload['end_datetime'],
            ['Fecha', 'Pronóstico'],
            lines
        )

        return section.get_table_registry(
            **{
                'section': section,
            }
        )

    def get_dynamic_plot(self) -> Union[go.Figure]:
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Datos previos", "Pronóstico"))

        for line in self.lines:
            if 'forecasting' in line.name:
                state = line.name.replace('forecasting_', '')
                fig.add_trace(
                        go.Scatter(
                            x=line.x_values,
                            y=line.y_values,
                            mode='lines',
                            line=dict(color=self._color_map[state]),
                            showlegend=False,
                        ),
                        row=1,
                        col=2,
                    )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=line.x_values,
                        y=line.y_values,
                        mode="lines",
                        line=dict(color=self._color_map[line.name]),
                        name=line.name
                    ),
                    row=1,
                    col=1,
                )

        fig.update_layout(
            xaxis_title=self.axes_names[0],
            yaxis_title=self.axes_names[1],
            margin=dict(l=0, t=0, r=0, b=0))

        return fig


    @classmethod
    def get_image_plot(cls, **kwargs) -> Image:
        section = kwargs['section']
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Datos previos", "Pronóstico"))

        for line in section.lines:
            if 'forecasting' in line.name:
                state = line.name.replace('forecasting_', '')
                fig.add_trace(
                    go.Scatter(
                        x=line.x_values,
                        y=line.y_values,
                        mode='lines',
                        line=dict(color=section._color_map[state]),
                        showlegend=False,
                    ),
                    row=1,
                    col=2,
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=line.x_values,
                        y=line.y_values,
                        mode="lines",
                        line=dict(color=section._color_map[line.name]),
                        name=line.name
                    ),
                    row=1,
                    col=1,
                )

        fig.update_layout(
            xaxis_title=section.axes_names[0],
            yaxis_title=section.axes_names[1],
            margin=dict(l=0, t=0, r=0, b=0))

        img = cls._convert_plotly_to_pil(fig)

        return img


    @classmethod
    def _transform_conditions_to_hours(cls, conditions_df: pd.DataFrame) -> pd.DataFrame:
        by_hour = []
        for hour in range(0, 23):
            subset = conditions_df[
                conditions_df.observation_timestamp.dt.hour == hour
            ]
            states_by_hour = subset.condition.value_counts()
            states_dict = states_by_hour.to_dict()
            states_dict['observation_timestamp'] = subset['observation_timestamp'].median()
            by_hour.append(states_dict)

        states_by_hour = pd.DataFrame(
            by_hour).dropna(
            axis=0, how="all", inplace=False).reset_index().fillna(0)
        data = states_by_hour.sort_values(by="observation_timestamp")
        return data

    @classmethod
    def prophet_method(cls, previous_data, values_column):
        """Use prophet to get forecasting data."""
        periods = len(previous_data.index)
        previous_data.rename(
            columns={values_column: "y", "observation_timestamp": "ds"}, inplace=True
        )
        previous_data["ds"] = (previous_data['ds'] + pd.Timedelta(days=1)).dt.tz_localize(None)
        m = Prophet(changepoint_prior_scale=0.01).fit(previous_data)
        future = m.make_future_dataframe(periods=periods, freq="H")
        forecast = m.predict(future)
        return [forecast["yhat"], forecast["ds"]]

    @classmethod
    def getting_forecasting_data(cls, grouped_by_hour: pd.DataFrame) -> pd.DataFrame:
        """Get forecasting data."""
        forecast_df = pd.DataFrame()
        forecast_df["observation_timestamp"] = grouped_by_hour['observation_timestamp']

        for column_name in cls._color_map.keys():
            if column_name in grouped_by_hour.columns:
                forecast_by_condition = grouped_by_hour.loc[
                                        :, [column_name, "observation_timestamp"]
                                        ]

                if forecast_by_condition.size < 4:  # size returns num rows times num cols
                    log.info(f"Could not compute forecast for colum_name, because less than 2 rows")
                    continue

                forecasting_values = cls.prophet_method(forecast_by_condition, column_name)
                forecast_df[f"forecasting_{column_name}"] = forecasting_values[0]
                forecast_df["ds"] = forecasting_values[1]

                data = forecast_df.sort_values(by="ds")
                data['ds'] = data['ds'].astype(str)

        return data
