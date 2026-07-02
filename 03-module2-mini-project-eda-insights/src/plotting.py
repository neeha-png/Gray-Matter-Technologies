"""Small shared plotting helpers so every "finding" chart in the notebook
looks consistent and doesn't repeat the same styling code five times."""
import pathlib

import matplotlib.pyplot as plt

ASSETS_DIR = pathlib.Path(__file__).resolve().parent.parent / "assets"
ASSETS_DIR.mkdir(exist_ok=True)


def approval_rate_bar(rates, title, xlabel, filename, palette=None):
    """Bar chart of an approval rate (0-1) per category, saved for the deck."""
    fig, ax = plt.subplots(figsize=(5.5, 4))
    rates.plot(kind="bar", ax=ax, color=palette or "#4C72B0")
    ax.set_ylabel("Approval rate")
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    ax.set_ylim(0, 1)
    for i, v in enumerate(rates):
        ax.text(i, v + 0.02, f"{v:.0%}", ha="center")
    plt.xticks(rotation=0)
    plt.tight_layout()
    save(fig, filename)
    return fig


def save(fig, filename):
    path = ASSETS_DIR / filename
    fig.savefig(path, dpi=130)
    print(f"Saved chart -> {path}")
