"""This dashboard is for the plots"""
import logging
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import ipywidgets as widgets

import clease.plot_post_process
from clease_gui import register_logger
from clease_gui.base_dashboard import BaseDashboard

__all__ = ["FitPlotDashboard"]

logger = logging.getLogger(__name__)
register_logger(logger)


class FitPlotDashboard(BaseDashboard):
    def initialize(self):

        tabs = []
        titles = []

        plt.ioff()

        def add_tab(output, title):
            tabs.append(output)
            titles.append(title)

        self.fit_out = widgets.Output()
        add_tab(self.fit_out, "Fit")

        self.residual_out = widgets.Output()
        add_tab(self.residual_out, "Residuals")

        self.eci_out = widgets.Output()
        add_tab(self.eci_out, "ECI")

        self.cv_out = widgets.Output()
        add_tab(self.cv_out, "CV")

        # Convex hull can take a long time to plot for large systems
        # Add a switch so we can disable plotting convex hulls manually, if we want.
        self.enable_hull_switch = widgets.Checkbox(
            value=False,
            description="Enable?",
        )
        convex_hull_tab_out = widgets.Output()
        self.convex_hull_out = widgets.Output()
        with convex_hull_tab_out:
            clear_output()
            display(self.enable_hull_switch)
            display(self.convex_hull_out)
        add_tab(convex_hull_tab_out, "Convex Hull")

        self.plot_btn = self.make_event_button(
            self._on_make_plot_click,
            description="Update Plots",
            button_style="primary",
        )

        self.tabs = widgets.Tab(children=tabs)
        for ii, title in enumerate(titles):
            self.tabs.set_title(ii, title)

        # Keep track of open figures, so we can close them again
        # if we overwrite them.
        self._figures = {}

    def display(self):
        display(self.plot_btn, self.tabs)

    @property
    def evaluator(self):
        try:
            return self.app_data[self.KEYS.EVALUATE]
        except KeyError:
            raise KeyError("No fit has been performed yet.") from None

    def _close_figure(self, name: str) -> None:
        """Close a figure object with a certain name
        if it exists"""
        if name in self._figures:
            logger.debug("Closing figure: %s", name)
            fig = self._figures[name]
            plt.close(fig=fig)
            # We no longer need to store this
            self._figures.pop(name)

    def _register_figure(self, name: str, fig) -> None:
        """Register a figure object with a name.
        Will close the old figure if it exists"""
        self._close_figure(name)
        self._figures[name] = fig

    def _make_convex_hull(self):
        evaluator = self.evaluator

        if not self.enable_hull_switch.value:
            return
        fig = clease.plot_post_process.plot_convex_hull(evaluator)
        btn = self._make_save_figure_button(fig, "convex_hull.png")

        with self.convex_hull_out:
            clear_output(wait=True)
            display(fig, btn)
        self._register_figure("convex_hull", fig)

    def _make_residual_plot(self):
        evaluator = self.evaluator
        fig = clease.plot_post_process.plot_fit_residual(evaluator)
        btn = self._make_save_figure_button(fig, "fit_residual.png")

        with self.residual_out:
            clear_output(wait=True)
            display(fig, btn)
        self._register_figure("residual", fig)

    def _make_cv_plot(self):
        evaluate = self.evaluator
        try:
            fig = clease.plot_post_process.plot_cv(evaluate)
            btn = self._make_save_figure_button(fig, "fit_cv.png")
        except ValueError:
            # No CV scores
            fig = None
            btn = None

        with self.cv_out:
            clear_output(wait=True)
            if fig is not None:
                display(fig, btn)
                self._register_figure("cv_score", fig)
            else:
                print("No CV values, requires alpha optimization")

    def _make_fit_plot(self):
        evaluate = self.evaluator
        fig = clease.plot_post_process.plot_fit(evaluate)
        btn = self._make_save_figure_button(fig, "fit_plot.png")

        with self.fit_out:
            clear_output(wait=True)
            display(fig, btn)
        self._register_figure("fit_plot", fig)

    def _make_eci_plot(self):
        evaluate = self.evaluator
        fig = clease.plot_post_process.plot_eci(evaluate)
        btn = self._make_save_figure_button(fig, "fit_eci.png")

        with self.eci_out:
            clear_output(wait=True)
            display(fig, btn)
        self._register_figure("eci_plot", fig)

    def _make_save_figure_button(self, fig, default_filename):
        button = widgets.Button(description="Save Figure")
        filename_widget = widgets.Text(description="Filename:", value=default_filename)

        def _on_click(b):
            cwd = self.app_data[self.KEYS.CWD]
            filename = filename_widget.value
            pa = cwd / filename
            fig.savefig(
                filename,
                dpi=400,
                bbox_inches="tight",
                facecolor="white",
                transparent=False,
            )
            logger.info("Saved figure to file: %s", str(pa))

        button.on_click(_on_click)
        box = widgets.HBox(children=[button, filename_widget])
        return box

    def _on_make_plot_click(self):
        logger.info("Updating all fit plots.")
        self._make_fit_plot()
        self._make_residual_plot()
        self._make_eci_plot()
        self._make_cv_plot()
        self._make_convex_hull()
        logger.info("Plotting completed.")

    @property
    def fit_results(self):
        return self.app_data.get("fit_results", None)
