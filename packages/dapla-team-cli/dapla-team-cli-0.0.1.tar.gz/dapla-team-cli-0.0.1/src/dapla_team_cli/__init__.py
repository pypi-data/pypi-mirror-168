"""Dapla Team CLI."""

from questionary import Style


prompt_custom_style = Style(
    [
        ("separator", "fg:#cc5454"),
        ("qmark", "fg:#673ab7 bold"),
        ("question", ""),
        ("selected", "fg:#545454"),
        ("pointer", "fg:#673ab7 bold"),
        ("highlighted", "fg:#673ab7 bold"),
        ("answer", "fg:#5F517D bold"),
        ("text", "fg:#005500"),
        ("disabled", "fg:#858585 italic"),
    ]
)
