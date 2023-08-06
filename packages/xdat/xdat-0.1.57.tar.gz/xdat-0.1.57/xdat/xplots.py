import datetime as dt
import pandas as pd
import seaborn as sns
import numpy as np
import arviz as az
import datashader as ds
import colorcet as cc
import datashader.transfer_functions as tf

from sklearn import metrics
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker
from ds_utils.metrics import plot_confusion_matrix as _plot_confusion_matrix, visualize_accuracy_grouped_by_probability
from scriptine import path

from . import xproblem, xpd, xsettings


def plot_feature_importances(folds, title=''):
    df = xproblem.calc_feature_importances(folds, flat=True)
    if df is None:
        return

    fis = df.groupby('feature_name')['feature_importance'].mean()
    df = xpd.x_sort_on_lookup(df, 'feature_name', fis, ascending=True)
    sns.catplot(data=df, y='feature_name', x='feature_importance')
    plt.xlim([0, None])
    if title:
        plt.title(title)

    plt.tight_layout()
    plt.show()

    return


def plot_roc_curve(y_true, y_score, title=''):
    auc = metrics.roc_auc_score(y_true, y_score)
    fper, tper, thresholds = metrics.roc_curve(y_true, y_score)
    plt.plot(fper, tper, color='orange', label='ROC')
    plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')

    title2 = f'ROC Curve (AUC={auc:.3f})'
    if title:
        title2 = f"{title}: {title2}"

    plt.title(title2)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_confusion_matrix(y_true, y_pred, labels=None, title=''):
    y_true = pd.Series(y_true)
    counts = sorted([(l, c) for l, c in y_true.value_counts().items()])
    counts_str = ", ".join([f"{l}={c}" for l, c in counts])

    labels = labels or sorted(y_true.unique())

    _plot_confusion_matrix(y_true, y_pred, labels=labels)

    title2 = f"Counts: {counts_str} (total={len(y_true)})"
    if title:
        title2 = f"{title}: {title2}"

    plt.title(title2)

    plt.tight_layout()
    plt.show()


def plot_model_scores(y_true, y_score, bins=25, title=''):
    """
    Useful of comparing model scores for the different targets
    """

    df = pd.DataFrame({'Target': y_true, 'Model Score': y_score})
    sns.histplot(data=df, x='Model Score', hue='Target', element="step", common_norm=False, stat='percent', bins=bins)

    title2 = 'Histogram of model scores'
    if title:
        title2 = f"{title}: {title2}"

    plt.title(title2)
    plt.tight_layout()
    plt.show()


def plot_score_comparison(scores: dict, key_label='Dataset', score_label='Model Score', bins=25, title=''):
    """
    Useful for comparing the scores of various datasets:
    > plot_score_comparison({'train': train_scores, 'test': test_scores, 'blind': blind_scores)
    """

    rows = []
    for k, scores in scores.items():
        for score in scores:
            rows.append({key_label: k, score_label: score})

    df = pd.DataFrame(rows)
    sns.histplot(data=df, x=score_label, hue=key_label, element="step", common_norm=False, stat='percent', bins=bins)

    title2 = f'Histogram of model scores per {key_label}'
    if title:
        title2 = f"{title}: {title2}"

    plt.title(title2)
    plt.tight_layout()
    plt.show()


def plot_model_scores_ratios(y_true, y_score, bins=25, ratio_of=1):
    df = pd.DataFrame({'target': y_true, 'score': y_score})
    s_min = y_score.min()
    s_max = y_score.max()
    s_range = s_max - s_min
    borders = np.linspace(s_min, s_max+s_range*.0001, bins+1)

    rows = []
    for s_start, s_end in zip(borders[:-1], borders[1:]):
        s_mid = (s_start + s_end) / 2
        df_g = df[(df.score >= s_start) & (df.score < s_end)]
        if len(df_g) == 0:
            continue

        r = (df_g.target == ratio_of).sum() / len(df_g)
        rows.append({'s_start': df_g.score.min(), 's_end': df_g.score.max(), 'ratio': r})

    df_rows = pd.DataFrame(rows)

    for row in df_rows.itertuples():
        plt.plot([row.s_start, row.s_end], [row.ratio, row.ratio], color='black')

    plt.title('Histogram of model scores')
    plt.tight_layout()
    plt.show()


def plot_corr_heatmap(df, title='Correlation Heatmap', fontsize=12, pad=12, cmap='BrBG', figsize=(15,15)):
    """
    Credits: https://medium.com/@szabo.bibor/how-to-create-a-seaborn-correlation-heatmap-in-python-834c0686b88e
    """

    plt.subplots(figsize=figsize)
    df_corr = df.corr()
    mask = np.triu(np.ones_like(df_corr, dtype=np.bool))

    hm = sns.heatmap(df_corr, vmin=-1, vmax=1, annot=True, cmap=cmap, mask=mask)
    hm.set_title(title, fontdict={'fontsize': fontsize}, pad=pad)
    plt.tight_layout()
    plt.show()


def plot_pie(vals=None, counts=None, title=''):
    if vals is not None:
        vals = pd.Series(vals)
        counts = vals.value_counts()

    assert counts is not None, "either vals or counts must be provided"

    plt.figure(figsize=(6, 6))
    plt.pie(counts.values, labels=counts.index.values, autopct='%1.1f%%', shadow=False, startangle=0)

    title2 = f"total count={counts.sum()}"
    if title:
        title2 = f"{title}: {title2}"
    plt.title(title2)

    plt.tight_layout()
    plt.show()


def plot_counts(df, on, sort_by_counts=True, title=''):
    counts = df[on].value_counts()
    counts = counts.sort_values(ascending=False)
    plt.clf()
    title2 = f"Counts on {on}"
    if title:
        title2 = f"{title}: {title2}"
    plt.title(title2)
    x = np.arange(len(counts)) if sort_by_counts else counts.index.values
    plt.scatter(x, counts.values, s=2)
    plt.ylabel('counts')
    if sort_by_counts:
        plt.xlabel(f"{on} sorted by counts")
        plt.tick_params(
            axis='x',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            bottom=False,  # ticks along the bottom edge are off
            top=False,  # ticks along the top edge are off
            labelbottom=False)  # labels along the bottom edge are off

    else:
        plt.xlabel(f"{on}")

    plt.tight_layout()
    plt.show()
    return


def big_scatter(df, x, y, colors='fire', title='', show=True, show_axis=True, figsize=(12, 12), plot_dim=(1000, 1000)):
    fig, axes = plt.subplots(figsize=figsize)
    # a = ds.Canvas().points(df, 'x', 'y')
    # tf.shade(a)
    # plt.plot([-15, 15], [-15, 15], color='blue')
    # plt.show()

    cvs = ds.Canvas(plot_width=plot_dim[0], plot_height=plot_dim[1])
    agg = cvs.points(df, x, y)

    if colors == 'fire':
        img = ds.tf.set_background(ds.tf.shade(agg, cmap=cc.fire), "black")
    elif colors == 'bw':
        img = ds.tf.set_background(ds.tf.shade(agg, cmap=cc.b_cyclic_grey_15_85_c0_s25), "black")
    else:
        raise ValueError(colors)

    img2 = img.to_pil()
    plt.imshow(img2, extent=(img.x.min(), img.x.max(), img.y.min(), img.y.max()))

    if not show_axis:
        plt.axis('off')

    plt.tight_layout()

    if title:
        plt.title(title)

    if show:
        plt.show()


def post_plot(title='', xlim=None, ylim=None, tight_layout=True, show=True):
    """
    Helper function to set various plot attributes...
    """

    if title:
        plt.title(title)

    if xlim:
        plt.xlim(xlim)

    if ylim:
        plt.ylim(ylim)

    if tight_layout:
        plt.tight_layout()

    if show:
        plt.show()


def plot_multi(df, kind='scatter', plot_func=None, x=None, y=None, plot_on=None, group_on=None, color_on=None, label_on=None, style_on=None, figsize=(10,6), alpha=1.0, hdi_probs=(0.1, 0.25, 0.5, 0.8, 0.999), color_dict=None, title='', x_axis_type=None, y_axis_type=None, legend_loc='best', xlim=None, ylim=None, save_to=None, clear_folder=False, add_date=True, **kwargs):
    """

    :param df: input dataframe
    :param kind: type of plot ('scatter', 'line', 'hdi')
    :param plot_func: alternative to *kind*, can provide a custom function that takes a subset of data & plots
    :param x: name of column for x-axis
    :param y: name of column for y-axis
    :param plot_on: column name that generates different plot for each unique value
    :param group_on: column name for different subgroup of data (usually not neaded if provide color_on, etc)
    :param color_on: column name for different colors
    :param label_on: column name for different labels
    :param style_on: column name for different styles
    :param figsize:
    :param alpha: transparency
    :param hdi_probs: used for kind == 'hdi'
    :param color_dict:
    :param title:
    :param x_axis_type: can set to int
    :param y_axis_type: can be set to int
    :param legend_loc:
    :param xlim:
    :param ylim:
    :param save_to: instead of displaying, can save fig to file
    :param clear_folder:
    :param add_date: adds a date to fig
    :param kwargs: additional params that get passed to plot_func
    :return:
    """
    color_dict = color_dict or dict()

    if save_to:
        save_to = path(save_to)
        save_to.ensure_dir()

        if clear_folder:
            save_to.rmtree()
            save_to.ensure_dir()

    def to_list(i):
        if not i:
            i = []

        if isinstance(i, str):
            i = [i]

        return i

    color_on = to_list(color_on)
    style_on = to_list(style_on)
    label_on = to_list(label_on)
    group_on = to_list(group_on)

    if not label_on:
        label_on = color_on + style_on

    if not color_on:
        color_on = label_on

    if label_on:
        df = df.sort_values(label_on)

    if not group_on:
        group_on = color_on + style_on + label_on

    color_list = list(mcolors.TABLEAU_COLORS.keys()) + list(mcolors.XKCD_COLORS)
    line_styles = [
     ('solid', 'solid'),      # Same as (0, ()) or '-'
     ('dotted', 'dotted'),    # Same as (0, (1, 1)) or ':'
     ('dashed', 'dashed'),    # Same as '--'
     ('dashdot', 'dashdot'),  # Same as '-.'
     ('loosely dashed',        (0, (5, 10))),
     ('densely dashed',        (0, (5, 1))),
     ('loosely dashdotted',    (0, (3, 10, 1, 10))),
     ('dashdotted',            (0, (3, 5, 1, 5))),
     ('densely dashdotted',    (0, (3, 1, 1, 1))),
     ('dashdotdotted',         (0, (3, 5, 1, 5, 1, 5))),
     ('loosely dashdotdotted', (0, (3, 10, 1, 10, 1, 10)))]
    line_styles = [ls[1] for ls in line_styles]
    scatter_markers = list(".v1sPp*+xd|_")
    style_list = line_styles if kind == 'line' else scatter_markers
    style_param = "ls" if kind == 'line' else 'marker'

    color_id = 0
    style_id = 0
    color_lookup = dict()
    style_lookup = dict()
    for df_p, _, plot_title in xpd.x_iter_groups(df, plot_on):
        labels = set()
        plt.clf()
        fig, ax = plt.subplots(figsize=figsize)
        for df_g, _, group_title in xpd.x_iter_groups(df_p, group_on):
            color = None
            label = None
            style = None

            if label_on:
                sa_label = df_g.iloc[0][label_on]
                label = ", ".join([f"{k}={v}" for k,v in sa_label.items()])

            if label in labels:
                label = None

            labels.add(label)

            if color_on:
                sa_color_val = df_g.iloc[0][color_on]
                color_val = ", ".join([f"{k}={v}" for k, v in sa_color_val.items()])
                if color_val not in color_lookup:
                    color_lookup[color_val] = color_list[color_id]
                    color_id += 1

                color = color_lookup[color_val]

            if style_on:
                sa_style_val = df_g.iloc[0][style_on]
                style_val = ", ".join([f"{k}={v}" for k, v in sa_style_val.items()])
                if style_val not in style_lookup:
                    style_lookup[style_val] = style_list[style_id]
                    style_id += 1

                style = style_lookup[style_val]

            params = dict()
            if color is not None:
                params['color'] = color

            if style is not None:
                params[style_param] = style

            if label is not None:
                params['label'] = label

            if alpha is not None:
                params['alpha'] = alpha

            params.update(kwargs)

            if plot_func:
                plot_func(df_g, **params)

            elif kind == 'scatter':
                params['s'] = params.get('s', 0.2)
                plt.scatter(x=df_g[x], y=df_g[y], **params)

            elif kind == 'line':
                if len(df_g) == 1:
                    params['marker'] = 'x'

                df_g = df_g.sort_values([x, y])
                plt.plot(df_g[x], df_g[y], **params)

            elif kind == 'hdi':
                hdi_probs = sorted(hdi_probs)
                alpha_step = alpha / len(hdi_probs)
                g_hdi = df_g.groupby(x)
                for hdi_prob in hdi_probs:
                    try:
                        df_hdi = g_hdi.apply(lambda dfx: pd.Series(az.hdi(dfx[y].to_numpy(), hdi_prob=hdi_prob), index=['low', 'high']))
                    except ValueError:
                        print('hi')
                        raise
                    df_hdi = df_hdi.reset_index()
                    params['label'] = label
                    params['alpha'] = alpha_step
                    if 'color' not in params:
                        params['color'] = 'blue'

                    plt.fill_between(df_hdi[x], df_hdi['low'], df_hdi['high'], linewidth=0, **params)
                    label = None

            else:
                raise ValueError(kind)

        if title and plot_title:
            plot_title = f"{title}: {plot_title}"

        elif title:
            plot_title = title

        if plot_title:
            plt.title(plot_title)

        if labels and legend_loc != 'off':
            plt.legend(loc=legend_loc)

        if x_axis_type == int:
            plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))

        if y_axis_type == int:
            plt.gca().yaxis.set_major_locator(mticker.MultipleLocator(1))

        if xlim:
            plt.xlim(xlim)

        if ylim:
            plt.ylim(ylim)

        if x:
            plt.xlabel(xsettings.x_get_desc(x))

        if y:
            plt.ylabel(xsettings.x_get_desc(y))

        if add_date:
            date_str = dt.date.today().isoformat()
            ax.annotate(date_str, xy=(0.9, -0.08), xycoords='axes fraction')

        plt.tight_layout()

        if save_to:
            plot_title = plot_title or "all"
            plt.savefig(save_to.joinpath(f"{plot_title}.png"), pad_inches=0)

        else:
            plt.show()
