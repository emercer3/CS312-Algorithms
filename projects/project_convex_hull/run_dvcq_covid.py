"""Run the DVCQ convex-hull algorithm on the COVID timeseries CSV
and plot the hull of infected countries for three different dates.

Usage: run with `python run_dvcq_covid.py` in the project root.
"""
from datetime import datetime
import csv
import matplotlib.pyplot as plt

from convex_hull import compute_hull_dvcq
from plotting import plot_points, draw_hull, title, show_plot


CSV_PATH = "Covid_19_Countrywise_timeseries.csv"


def load_by_date(csv_path):
    """Return dict mapping date -> set of (lon, lat) tuples for rows with Confirmed>0."""
    by_date = {}
    with open(csv_path, newline='') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            date_str = row.get('ObservationDate')
            if not date_str:
                continue
            try:
                date_obj = datetime.strptime(date_str.strip(), "%m/%d/%Y")
            except Exception:
                # skip malformed dates
                continue

            try:
                confirmed = int(row.get('Confirmed') or 0)
            except Exception:
                confirmed = 0

            if confirmed <= 0:
                continue

            try:
                lat = float(row.get('latitude'))
                lon = float(row.get('longitude'))
            except Exception:
                continue

            key = date_obj.date()
            by_date.setdefault(key, set()).add((lon, lat))

    return by_date


def pick_three_dates(dates):
    """Pick three dates: earliest, middle, latest (if available)."""
    dates = sorted(dates)
    if not dates:
        return []
    if len(dates) == 1:
        return [dates[0]] * 3
    if len(dates) == 2:
        return [dates[0], dates[0], dates[1]]

    mid_index = len(dates) // 2
    return [dates[0], dates[mid_index], dates[-1]]


def run_and_plot():
    by_date = load_by_date(CSV_PATH)
    dates = list(by_date.keys())
    sel_dates = pick_three_dates(dates)

    if not sel_dates:
        print("No data found in CSV or no infected rows.")
        return

    fig, axes = plt.subplots(1, len(sel_dates), figsize=(5 * len(sel_dates), 5))
    if len(sel_dates) == 1:
        axes = [axes]

    for ax, d in zip(axes, sel_dates):
        pts = sorted(by_date.get(d, []))
        pts_list = list(pts)

        ax.set_aspect('equal', adjustable='datalim')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')

        if not pts_list:
            ax.set_title(f"{d}: no infected locations")
            continue

        # plot raw points
        xx, yy = zip(*pts_list)
        ax.scatter(xx, yy, c='k', s=10)

        # compute hull (expects list of (x,y))
        hull = compute_hull_dvcq(pts_list)

        if hull and len(hull) >= 2:
            # draw hull on the axes
            hx, hy = zip(*hull)
            hx = [*hx, hull[0][0]]
            hy = [*hy, hull[0][1]]
            ax.plot(hx, hy, c='r')
            ax.scatter(hx[:-1], hy[:-1], facecolors='none', edgecolors='r', s=80)

        ax.set_title(f"{d} — points: {len(pts_list)} hull: {len(hull)}")

    fig.suptitle('DVCQ convex hull of infected-country locations at 3 dates')
    plt.tight_layout()

    out_fname = 'dvcq_covid_hulls.svg'
    plt.savefig(out_fname, format='svg')
    print(f'Saved plot to {out_fname}')


if __name__ == '__main__':
    run_and_plot()
