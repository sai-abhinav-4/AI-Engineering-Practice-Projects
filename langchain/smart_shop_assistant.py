# smart_shop_assistant.py
# Block 12 — the PROJECT: give your agent a chat UI with Gradio.
# Run:  python smart_shop_assistant.py     then open the local link it prints.
import os
import sys
import gradio as gr

# Ensure script directory and parent directory are in sys.path
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from first_agent import agent


def chat(message, history):
    # Gradio fills in `message` (newest) and `history` (past turns) for you.
    # Pass `history` into your agent to give it memory across chat turns!
    return agent(message, history=history)


if __name__ == "__main__":
    gr.ChatInterface(
        fn=chat,
        title="🛍️ Smart Shop Assistant",
        description="Ask me the price of shoes, hat, bag, shorts or pants — I'll look it up.",
    ).launch(share=True)
