# ========================================
# gradio_app.py
# ========================================

import gradio as gr
from theme_classifier.theme_classifier import ThemeClassifier
import pandas as pd

def get_themes(theme_list_str, subtitles_path, save_path):
    # Split theme list
    theme_list = [t.strip() for t in theme_list_str.split(',')]

    # Create classifier
    theme_classifier = ThemeClassifier(theme_list)
    output_df = theme_classifier.get_themes(subtitles_path, save_path)

    # Remove 'dialogue'
    theme_list = [theme for theme in theme_list if theme != 'dialogue']

    # Keep only requested themes
    output_df = output_df[theme_list]

    # Aggregate scores
    output_df = output_df.sum().reset_index()
    output_df.columns = ['Theme', 'Score']

    # ✅ IMPORTANT: return the **DataFrame**, NOT the component!
    return output_df

def main():
    with gr.Blocks() as iface:
        gr.Markdown("# Theme Classification (Zero Shot Classifier)")

        with gr.Row():
            theme_list = gr.Textbox(label="Themes (comma separated)")
            subtitles_path = gr.Textbox(label="Subtitles or Script Path")
            save_path = gr.Textbox(label="Save Path")
            get_themes_button = gr.Button("Get Themes")

        # ✅ Correct: declare output as BarPlot, but don’t return it yourself!
        plot = gr.BarPlot(
            x="Theme",
            y="Score",
            title="Series Themes",
            tooltip=["Theme", "Score"],
            vertical=False,
            width=500,
            height=400,
        )

        # ✅ Connect handler
        get_themes_button.click(
            get_themes,
            inputs=[theme_list, subtitles_path, save_path],
            outputs=plot
        )

    iface.launch(share=True)

if __name__ == '__main__':
    main()
