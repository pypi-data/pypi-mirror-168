import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from classiq.interface.analyzer.result import GraphResult

from classiq.exceptions import ClassiqAnalyzerError


def _create_heatmap_graph(result: GraphResult, num_qubits: int) -> go.Figure:
    if result is None:
        raise ClassiqAnalyzerError("heatmap failed to create`")
    return (
        px.imshow(
            pd.read_json(result.details),
            labels=dict(
                x="cycles",
                y="qubit",
                color="connectivity strength",
            ),
            color_continuous_scale="sunset",
        )
        .update_xaxes(showticklabels=False)
        .update_yaxes(tickvals=list(range(num_qubits)))
    )
