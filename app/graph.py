from langgraph.graph import StateGraph, END

from app.state import ResearchState
from app.nodes.planner import planner_node
from app.nodes.fundamentals import fundamentals_node
from app.nodes.leadership import leadership_node
from app.nodes.aum import aum_node
from app.nodes.outlook_strategy import outlook_strategy_node
from app.nodes.culture_careers import culture_careers_node
from app.nodes.curation import curation_node
from app.nodes.section_writer import section_writer_node
from app.nodes.qa_final import qa_final_node


def build_graph():
    graph = StateGraph(ResearchState)

    # Nodes
    graph.add_node("planner", planner_node)
    graph.add_node("fundamentals", fundamentals_node)
    graph.add_node("leadership", leadership_node)
    graph.add_node("aum", aum_node)
    graph.add_node("outlook_strategy", outlook_strategy_node)
    graph.add_node("culture_careers", culture_careers_node)
    graph.add_node("curation", curation_node)
    graph.add_node("section_writer", section_writer_node)
    graph.add_node("qa_final", qa_final_node)

    # Entry
    graph.set_entry_point("planner")

    # Planner → topic agents
    graph.add_edge("planner", "fundamentals")
    graph.add_edge("planner", "leadership")
    graph.add_edge("planner", "aum")
    graph.add_edge("planner", "outlook_strategy")
    graph.add_edge("planner", "culture_careers")

    # Topic agents → curation
    graph.add_edge("fundamentals", "curation")
    graph.add_edge("leadership", "curation")
    graph.add_edge("aum", "curation")
    graph.add_edge("outlook_strategy", "curation")
    graph.add_edge("culture_careers", "curation")

    # Tail
    graph.add_edge("curation", "section_writer")
    graph.add_edge("section_writer", "qa_final")
    graph.add_edge("qa_final", END)

    return graph.compile()
