"""
Milestone 5: Gradio web interface for the Off-Campus Housing Guide.

Run with:
    python app.py

Then open http://localhost:7860 in your browser.
"""

import gradio as gr
from query import ask


def handle_query(question: str):
    """
    Called on every button click or Enter press.
    Returns (answer_text, sources_text) for the two output boxes.
    """
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question)
    answer = result["answer"]

    # Format sources as a readable list
    sources = "\n".join(f"• {s}" for s in result["sources"])

    return answer, sources


# ---------------------------------------------------------------------------
# Gradio UI
# ---------------------------------------------------------------------------

example_questions = [
    "What should I look for when inspecting an apartment before signing a lease?",
    "What utilities are typically not included in rent for student apartments?",
    "How do I get my security deposit back after moving out?",
    "What are red flags when touring an apartment?",
    "How much of my income should I budget for rent as a student?",
]

with gr.Blocks(title="Off-Campus Housing Guide") as demo:
    gr.Markdown(
        """
        # 🏠 Off-Campus Housing Guide
        ### An unofficial student guide to renting your first apartment

        Ask any question about off-campus housing — leases, deposits, utilities,
        landlord issues, budgeting, and more. Answers are grounded in student reviews
        and housing guides; sources are shown for every response.
        """
    )

    with gr.Row():
        with gr.Column(scale=3):
            question_box = gr.Textbox(
                label="Your question",
                placeholder="e.g. What should I check before signing a lease?",
                lines=2,
            )
            ask_btn = gr.Button("Ask", variant="primary")

        with gr.Column(scale=1):
            gr.Markdown("**Example questions:**")
            for ex in example_questions:
                gr.Button(ex, size="sm").click(
                    fn=lambda q=ex: q,
                    outputs=question_box,
                )

    with gr.Row():
        answer_box = gr.Textbox(
            label="Answer",
            lines=10,
            interactive=False,
        )

    with gr.Row():
        sources_box = gr.Textbox(
            label="Retrieved from",
            lines=4,
            interactive=False,
        )

    # Wire up the button click and Enter key
    ask_btn.click(
        fn=handle_query,
        inputs=question_box,
        outputs=[answer_box, sources_box],
    )
    question_box.submit(
        fn=handle_query,
        inputs=question_box,
        outputs=[answer_box, sources_box],
    )

    gr.Markdown(
        """
        ---
        *Answers are generated only from collected student housing documents.
        For questions outside that scope, the system will say so rather than guess.*
        """
    )

if __name__ == "__main__":
    demo.launch()
