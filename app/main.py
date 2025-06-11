"""Application entry point for running the Gradio interface."""

from .interface import create_interface


def main() -> None:
    demo = create_interface()
    demo.launch()


if __name__ == "__main__":
    main()
