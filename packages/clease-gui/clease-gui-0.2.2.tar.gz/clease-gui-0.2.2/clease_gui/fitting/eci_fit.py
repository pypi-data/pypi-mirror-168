import logging
import time
from datetime import timedelta
from IPython.display import display
import ipywidgets as widgets
import clease
from clease_gui.base_dashboard import BaseDashboard
from clease_gui.status_bar import update_statusbar
from clease_gui import register_logger, utils

from . import fitting_widgets

logger = logging.getLogger(__name__)
register_logger(logger)

__all__ = ["ECIFitDashboard"]


class ECIFitDashboard(BaseDashboard):
    def initialize(self):

        self.fitting_output = widgets.Output()

        self.fitting_algo_dropdown = widgets.Dropdown(
            options=[
                ("LASSO", fitting_widgets.LassoScheme(output=self.fitting_output)),
                (
                    "L2",
                    fitting_widgets.L2Scheme(output=self.fitting_output),
                ),
                # ('Genetic Algorithm', 'genetic_algorithm'),
            ],
            description="Fitting Algorithm:",
            **self.DEFAULT_STYLE_KWARGS,
        )
        self.fitting_algo_dropdown.value.display()

        def _on_fitting_change(change):
            if utils.is_value_change(change):
                change.new.display()

        self.fitting_algo_dropdown.observe(_on_fitting_change)

        self.scoring_output = widgets.Output()
        self.scoring_widget = fitting_widgets.ScoringSchemeWidget()

        self.db_select_out = widgets.Output()
        self.db_select_widget = fitting_widgets.DBSelectWidget()

        self.fit_eci_button = utils.make_clickable_button(
            self._on_fit_eci_click,
            description="Fit ECI",
            button_style="primary",
        )

    def display(self):
        # self.update_algo_widgets()
        self.scoring_widget.display_widgets(output=self.scoring_output)
        self.db_select_widget.display_widgets(output=self.db_select_out)
        display(
            self.fitting_algo_dropdown,
            self.fitting_output,
            self.scoring_output,
            self.db_select_out,
            self.fit_eci_button,
        )

    @property
    def fitting_algo_widget(self) -> fitting_widgets.RegressionScheme:
        return self.fitting_algo_dropdown.value

    def get_db_name(self):
        db_name = self.db_select_widget.get_db_name()
        if db_name is not None:
            cwd = self.app_data[self.KEYS.CWD]
            return cwd / db_name
        # No db name was specified, try getting it from settings
        return self.get_db_name()

    def _make_evaluator(self):
        settings = self.settings
        scoring_scheme_kwargs = self.scoring_widget.value

        evaluator = clease.Evaluate(
            settings,
            **scoring_scheme_kwargs,
        )
        return evaluator

    def fit_eci(self):
        start_time = time.perf_counter()
        # Get all parameters
        wdgt = self.fitting_algo_widget
        keys = list(wdgt.HYPERPARAMS)
        if keys != ["alpha"]:
            raise NotImplementedError("Not yet implemented yet. Got keys:", keys)

        alpha = wdgt.hyper_widget_dct["alpha"]
        is_opt = alpha.is_optimization

        evaluator = self._make_evaluator()
        scheme = wdgt.get_fitting_scheme()
        evaluator.set_fitting_scheme(fitting_scheme=scheme)
        if is_opt:
            logger.info("Optimizing alpha")
            min_val, max_val, step_val = alpha.get_min_max_step()
            spacing_type = alpha.get_spacing_type()

            scale = "log" if spacing_type == "logspace" else "linear"
            logger.debug("Scale: %s", scale)
            alphas, cv = evaluator.alpha_CV(
                alpha_min=min_val,
                alpha_max=max_val,
                num_alpha=step_val,
                scale=scale,
            )
            # Get optimial alpha
            ind = cv.argmin()
            alpha_val = alphas[ind]
            cv_min = cv[ind]
            logger.info("Optimized alpha: %.3e, cv score: %.3e", alpha_val, cv_min)
        else:
            alpha_val = alpha.get_float_value()
        logger.info("Running fit with alpha: %.3e", alpha_val)
        # Even if we did an optimization, we want to fit at the optimized
        evaluator.set_fitting_scheme(fitting_scheme=scheme, alpha=alpha_val)
        evaluator.fit()
        self.set_evaluator(evaluator)
        eci = evaluator.get_eci_dict()
        # Count the number of non-zero ECI's and log
        self.set_eci(eci)
        num_eci = sum(1 for val in eci.values() if abs(val) > 1e-5)
        logger.info("Number of non-zero ECI: %d", num_eci)

        dt = timedelta(seconds=time.perf_counter() - start_time)
        logger.info("Fitting complete in %s.", dt)

    def set_evaluator(self, evaluator):
        """The evaluator cannot be saved to file, so save it as private"""

        # Make a shallow copy, so that it doesn't suddenly change.
        self.app_data[self.KEYS.EVALUATE] = evaluator

    @update_statusbar
    def _on_fit_eci_click(self, b):
        with self.event_context(logger=logger) as cm:
            self.fit_eci()
        if not cm.success:
            logger.error("Failed to fit")

    def set_eci(self, value):
        self.app_data[self.KEYS.ECI] = value

    @property
    def eci(self):
        try:
            return self.app_data[self.KEYS.ECI]
        except KeyError:
            raise ValueError("No ECI's present. Run fit first, or load ECI from file.")
