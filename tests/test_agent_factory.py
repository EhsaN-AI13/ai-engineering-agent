from agent.agent import EhsaNAgent
from agent_factory import create_agent


def test_create_agent():
    agent = create_agent()

    assert isinstance(agent, EhsaNAgent)
    assert agent.name == "EhsaN"