import pandas as pd
import numpy as np
from pycirclize import Circos
from pycirclize.utils import ColorCycler

import random

def create_awesome_visualization(df):
    
    np.random.seed(0)
    ColorCycler.set_cmap("tab10")
    df = df.select_dtypes(include=['number'])
    old_sectors = df.to_dict(orient='records')
    sectors = {}
    for sec_dict in old_sectors:
        for k,v in sec_dict.items():
            sectors[k]=sectors.get(k,0)+v
    # print(sectors)
    L = ["red","blue","green"]
    sector_colors = {k:random.choices(L, k=1)[0] for k,v in sectors.items()}
    circos = Circos(sectors, space=10, start=90, end=360, endspace=False)

    for sector in circos.sectors:
        # Outer Track
        outer_track = sector.add_track((95, 100))
        outer_track.text(sector.name, color="white")
        outer_track.axis(fc=sector_colors[sector.name])
        outer_track.xticks_by_interval(interval=10, label_orientation="vertical")
        # Rectangle Track
        rect_track = sector.add_track((90, 95))
        rect_size = 10
        for i in range(int(rect_track.size / rect_size)):
            x1, x2 = i * rect_size, i * rect_size + rect_size
            rect_track.rect(x1, x2, ec="black", lw=0.5, color=ColorCycler())
            rect_track.text(str(i + 1), (x1 + x2) / 2, size=8, color="white")
        # Generate random x, y plot data
        x = np.arange(1, int(sector.size), 2)
        y = np.random.randint(0, 10, len(x))
        # Line Track
        line_track = sector.add_track((80, 90), r_pad_ratio=0.1)
        line_track.axis()
        line_track.line(x, y, color="blue")
        # Scatter Track
        scatter_track = sector.add_track((70, 80), r_pad_ratio=0.1)
        scatter_track.axis()
        scatter_track.bar(x, y, width=0.8, color="orange")
        # Bar Track
        bar_track = sector.add_track((60, 70), r_pad_ratio=0.1)
        bar_track.axis()
        bar_track.scatter(x, y, color="green", s=3)
        # Fill Track
        fill_track = sector.add_track((50, 60), r_pad_ratio=0.1)
        fill_track.axis()
        fill_track.fill_between(x, y, y2=0, fc="red", ec="black", lw=0.5, alpha=0.5)
        # Line + Bar + Scatter Track
        line_bar_scatter_track = sector.add_track((40, 50), r_pad_ratio=0.1)
        line_bar_scatter_track.axis()
        line_bar_scatter_track.line(x, y, color="blue")
        line_bar_scatter_track.bar(x, y, width=0.8, color="orange")
        line_bar_scatter_track.scatter(x, y, color="green", s=3)

    # Plot text description
    text_common_kws = dict(ha="left", va="center", size=8)
    circos.text(" 01. Outer Track", r=97.5, color="black", **text_common_kws)
    circos.text(" 02. Rectangle Track", r=92.5, color="grey", **text_common_kws)
    circos.text(" 03. Line Track", r=85, color="blue", **text_common_kws)
    circos.text(" 04. Bar Track", r=75, color="orange", **text_common_kws)
    circos.text(" 05. Scatter Track", r=65, color="green", **text_common_kws)
    circos.text(" 06. Fill between Track", r=55, color="red", **text_common_kws)
    circos.text(" 07. Line + Bar + Scatter Track", r=45, color="purple", **text_common_kws)

    fig = circos.plotfig()
    return fig

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
