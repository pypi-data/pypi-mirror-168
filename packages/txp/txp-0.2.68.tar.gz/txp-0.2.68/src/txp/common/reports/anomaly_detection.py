import logging
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from PIL import Image
from typing import List, Dict, Union
from txp.common.config import settings
import txp.common.reports.section as sections
from sklearn.ensemble import IsolationForest
log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class AnomalyDetectionStates(sections.Plot2dSection):
    _color_map = {
        'OPTIMAL': "rgb(61, 98, 246)",
        'GOOD': "rgb(121, 207, 36)",
        'OPERATIVE': "rgb(246, 240, 61)",
        'UNDEFINED': "rgb(246, 79, 61)",
        'CRITICAL': "rgb(246, 79, 61)",
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
        super(AnomalyDetectionStates, self).__init__(
            tenant_id, section_id, start_datetime, end_datetime,
            axes_names, lines, **kwargs
        )

    @classmethod
    def required_inputs(cls) -> List[sections.SectionInputEnum]:
        return [sections.SectionInputEnum.STATES]

    @classmethod
    def compute(cls, inputs: Dict[sections.SectionInputEnum, pd.DataFrame], section_event_payload: Dict) -> Dict:
        states_data = inputs[sections.SectionInputEnum.STATES]
        states_data['observation_timestamp'] = (
            pd.to_datetime(states_data['observation_timestamp'], utc=True)
            .dt.tz_convert("America/Mexico_City")
        )
        conditions_by_hrs = cls._transform_conditions_to_hours(states_data)
        anomaly_data = cls._get_anomaly_detection_data(conditions_by_hrs)
        anomaly_detection = cls._anomaly_detection(anomaly_data)

        lines: List[cls.Plot2DLine] = []
        for state in cls._color_map.keys():
            if state in anomaly_detection:
                line_x_axis = anomaly_detection[state].index.astype(str).to_list()
                line_y_axis = anomaly_detection[state][state].to_list()

                marker_x_axis = anomaly_detection[state].index.astype(str).to_list()
                marker_y_axis = anomaly_detection[state]["Outlier"].to_list()

                lines.append(
                    cls.Plot2DLine(
                        line_x_axis, line_y_axis, f'line_{state}'
                    )
                )
                lines.append(
                    cls.Plot2DLine(
                        marker_x_axis, marker_y_axis, f'marker_{state}'
                    )
                )

        section: AnomalyDetectionStates = cls(
            section_event_payload['tenant_id'],
            section_event_payload['section_id'],
            section_event_payload['start_datetime'],
            section_event_payload['end_datetime'],
            ['Fecha', 'Ocurrencia de estados'],
            lines
        )

        return section.get_table_registry(
            **{
                'section': section,
            }
        )


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
    def _get_anomaly_detection_data(cls, hours_data: pd.DataFrame) -> Dict:
        data_by_hour = hours_data.set_index('observation_timestamp')
        anomaly_mapping_dict = {}
        for column in cls._color_map.keys():
            if column in data_by_hour.columns:
                test = pd.DataFrame()
                test[column] = data_by_hour[column]
                anomaly_mapping_dict.update({column: test})
        droped_nan_anomaly_mapping = {}
        for column in cls._color_map.keys():
            if column in anomaly_mapping_dict:
                data = anomaly_mapping_dict[column].dropna(subset=[column])
                droped_nan_anomaly_mapping.update({column: data})
        return droped_nan_anomaly_mapping

    @classmethod
    def _anomaly_detection(cls, droped_nan_anomaly_mapping: Dict):
        """
        Building dict for each data setting and getting anomaly detection
        """
        for column in cls._color_map.keys():
            if column in droped_nan_anomaly_mapping:
                if droped_nan_anomaly_mapping[column].empty:
                    print("empty")
                else:
                    # initializing Isolation Forest
                    clf = IsolationForest(max_samples="auto", contamination=0.01)

                    # training
                    clf.fit(droped_nan_anomaly_mapping[column])

                    # finding anomalies
                    droped_nan_anomaly_mapping[column]["Anomaly"] = clf.predict(
                        droped_nan_anomaly_mapping[column]
                    )

        for name, df in droped_nan_anomaly_mapping.items():
            df["Outlier"] = df.apply(
                    lambda x: x[name] if x["Anomaly"] == -1 else 0, axis=1
                )

        return droped_nan_anomaly_mapping

    @classmethod
    def get_image_plot(cls, **kwargs) -> Image:
        section = kwargs['section']
        fig = make_subplots(rows=1, cols=1)
        for line in section.lines:
            if 'line' in line.name:
                state = line.name.replace('line_', '')
                fig.add_trace(
                    go.Scatter(
                        x=line.x_values,
                        y=line.y_values,
                        mode="lines",
                        line=dict(color=section._color_map[state]),
                    ),
                    row=1,
                    col=1,
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=line.x_values,
                        y=line.y_values,
                        name="Anomalies",
                        mode="markers",
                        marker=dict(color="red", size=10, line=dict(color="red", width=1)),
                    )
                )
        fig.update_layout(margin=dict(l=0, r=100, t=0, b=0), showlegend=False)
        fig.update_layout(
            xaxis_title=section.axes_names[0],
            yaxis_title=section.axes_names[1],
            margin=dict(l=0, t=0, r=0, b=0))

        img = cls._convert_plotly_to_pil(fig)

        return img

    def get_dynamic_plot(self) -> Union[go.Figure]:
        fig = make_subplots(rows=1, cols=1)

        for line in self.lines:
            if 'line' in line.name:
                state = line.name.replace('line_', '')
                fig.add_trace(
                    go.Scatter(
                        x=line.x_values,
                        y=line.y_values,
                        mode="lines",
                        line=dict(color=self._color_map[state]),
                    ),
                    row=1,
                    col=1,
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=line.x_values,
                        y=line.y_values,
                        name="Anomalies",
                        mode="markers",
                        marker=dict(color="red", size=10, line=dict(color="red", width=1)),
                    )
                )
        fig.update_layout(margin=dict(l=0, r=100, t=0, b=0), showlegend=False)
        fig.update_layout(
            xaxis_title=self.axes_names[0],
            yaxis_title=self.axes_names[1],
            margin=dict(l=0, t=0, r=0, b=0))

        return fig
