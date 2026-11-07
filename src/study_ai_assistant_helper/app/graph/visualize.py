"""Generate a visual representation of the application graph."""

from study_ai_assistant_helper.app.graph.builder import create_graph

create_graph().get_graph().draw_mermaid_png(output_file_path='graph.png')
