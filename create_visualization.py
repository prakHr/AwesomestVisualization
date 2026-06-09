import pandas as pd
import numpy as np
from pycirclize import Circos

import random
import pandas as pd
import numpy as np
from pycirclize import Circos
from pycirclize.utils import ColorCycler


def create_awesome_visualization(df):
    # Keep only numeric columns
    df = df.select_dtypes(include=["number"])

    if df.empty:
        raise ValueError("DataFrame contains no numeric columns")

    # Sector sizes = column sums
    sectors = df.sum(axis=0).to_dict()

    ColorCycler.set_cmap("tab20")

    sector_names = list(sectors.keys())
    sector_colors = {
        sector: ColorCycler(i)
        for i, sector in enumerate(sector_names)
    }

    circos = Circos(
        sectors,
        space=max(2, 360 / (len(sectors) * 8)),
        start=90,
        end=360,
        endspace=False,
    )

    max_value = df.max().max()

    for sector in circos.sectors:
        col_name = sector.name

        # Values from dataframe column
        values = df[col_name].dropna().values

        if len(values) == 0:
            continue

        x = np.arange(len(values))

        # -------------------------
        # Outer Track
        # -------------------------
        outer_track = sector.add_track((95, 100))
        outer_track.axis(fc=sector_colors[col_name])
        outer_track.text(col_name, color="white")

        tick_interval = max(1, len(values) // 5)
        outer_track.xticks_by_interval(
            tick_interval,
            label_orientation="vertical"
        )

        # -------------------------
        # Rectangle Track
        # -------------------------
        rect_track = sector.add_track((90, 95))

        rect_size = max(1, int(sector.size / max(5, len(values))))

        for i in range(len(values)):
            x1 = i * rect_size
            x2 = min((i + 1) * rect_size, sector.size)

            rect_track.rect(
                x1,
                x2,
                ec="black",
                lw=0.5,
                color=ColorCycler(i)
            )

            rect_track.text(
                str(i + 1),
                (x1 + x2) / 2,
                size=6,
                color="white"
            )

        # -------------------------
        # Line Track
        # -------------------------
        line_track = sector.add_track((80, 90), r_pad_ratio=0.1)
        line_track.axis()

        line_track.line(
            x,
            values,
            color="blue"
        )

        # -------------------------
        # Bar Track
        # -------------------------
        bar_track = sector.add_track((70, 80), r_pad_ratio=0.1)
        bar_track.axis()

        bar_track.bar(
            x,
            values,
            width=0.8,
            color="orange"
        )

        # -------------------------
        # Scatter Track
        # -------------------------
        scatter_track = sector.add_track((60, 70), r_pad_ratio=0.1)
        scatter_track.axis()

        scatter_track.scatter(
            x,
            values,
            color="green",
            s=10
        )

        # -------------------------
        # Fill Track
        # -------------------------
        fill_track = sector.add_track((50, 60), r_pad_ratio=0.1)
        fill_track.axis()

        fill_track.fill_between(
            x,
            values,
            y2=0,
            fc="red",
            ec="black",
            lw=0.5,
            alpha=0.5,
        )

        # -------------------------
        # Combined Track
        # -------------------------
        combo_track = sector.add_track((40, 50), r_pad_ratio=0.1)
        combo_track.axis()

        combo_track.line(x, values, color="blue")
        combo_track.bar(x, values, width=0.8, color="orange")
        combo_track.scatter(x, values, color="green", s=10)

    # Dynamic legend labels
    legend_items = [
        ("Outer Track", 97.5, "black"),
        ("Rectangle Track", 92.5, "grey"),
        ("Line Track", 85, "blue"),
        ("Bar Track", 75, "orange"),
        ("Scatter Track", 65, "green"),
        ("Fill Track", 55, "red"),
        ("Combined Track", 45, "purple"),
    ]

    for label, radius, color in legend_items:
        circos.text(
            f" {label}",
            r=radius,
            color=color,
            ha="left",
            va="center",
            size=8,
        )

    return circos.plotfig()

def save_figure(fig, output_file_path):
    fig.savefig(output_file_path, dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    row_names = ["F1", "F2", "F3"]
    col_names = ["T1", "T2", "T3", "T4", "T5", "T6"]

    matrix_data = [
        [10, 16, 7, 7, 10, 8],
        [4, 9, 10, 12, 12, 7],
        [17, 13, 7, 4, 20, 4],
    ]

    df = pd.DataFrame(
        matrix_data,
        index=row_names,
        columns=col_names
    )

    fig = create_awesome_visualization(df)
    save_figure(fig, "output.png")
