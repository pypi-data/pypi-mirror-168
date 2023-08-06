import logging
from IPython.display import display
import ipywidgets as widgets

import ase
from ase.optimize import BFGS
from ase.constraints import UnitCellFilter
from ase.calculators.emt import EMT
import clease

from clease_gui import register_logger, utils
from clease_gui.status_bar import update_statusbar
from clease_gui.base_dashboard import BaseDashboard

logger = logging.getLogger(__name__)
register_logger(logger)


class EMTDashboard(BaseDashboard):
    def initialize(self):

        self.calc_button = utils.make_clickable_button(
            self._on_calc_click,
            description="Calculate with EMT",
            button_style="primary",
        )

        self.optimize_cell_widget = widgets.Checkbox(
            description="Optimize cell?",
            value=True,
            **self.DEFAULT_STYLE_KWARGS,
        )

        self.fmax_widget = widgets.BoundedFloatText(
            value=0.02,
            min=1e-4,
            max=999,
            description="Max Force:",
            **self.DEFAULT_STYLE_KWARGS,
        )

        def _on_update_optimize(change):
            if utils.is_value_change(change):
                self._update_widgets()

        self.optimize_cell_widget.observe(_on_update_optimize)
        self._update_widgets()

    def _update_widgets(self):
        # disable fmax if we don't optimize
        fmax_disabled = not self.do_optimize
        self.fmax_widget.disabled = fmax_disabled

    @property
    def fmax(self):
        return self.fmax_widget.value

    @property
    def do_optimize(self):
        return self.optimize_cell_widget.value

    @update_statusbar
    def _on_calc_click(self, b):
        with self.event_context(logger=logger) as cm:
            self.calculate()
        if not cm.success:
            logger.warning("Failed to calculate.")

    @property
    def mode(self):
        if self.do_optimize:
            return "Optimization"
        return "Static"

    def calculate(self):
        settings = self.app_data.get(self.KEYS.SETTINGS, None)
        if settings is None:
            raise RuntimeError("Need to know the settings to calculate")
        db_name = str(self.get_db_name())
        con = ase.db.connect(settings.db_name)
        num_calculated = 0

        mode = self.mode
        for row in con.select(converged=False):
            logger.info("Calculating row id: %d. Mode: %s", row.id, mode)
            atoms = row.toatoms()
            self._calculate_atoms(atoms)
            custom_kvp = row.key_value_pairs.copy()
            for key in ("struct_type", "name", "converged", "started", "queued"):
                # These keys are set in CLEASE, pop them out
                # pop converged just because we leave that as an "initial" attribute
                custom_kvp.pop(key, None)

            clease.tools.update_db(
                uid_initial=row.id,
                final_struct=atoms,
                db_name=db_name,
                custom_kvp_final=custom_kvp,
            )
            num_calculated += 1
        if num_calculated == 0:
            logger.info("No calculations were performed.")
        else:
            logger.info(f"Completed {num_calculated} calculations.")

    def _calculate_atoms(self, atoms):
        calc = EMT()
        atoms.calc = calc
        if self.do_optimize:
            ucf = UnitCellFilter(atoms)
            opt = BFGS(ucf, logfile=None)
            fmax = self.fmax
            opt.run(fmax=fmax)
        else:
            atoms.get_potential_energy()

    def display(self):
        box = widgets.HBox(children=[self.optimize_cell_widget, self.fmax_widget])
        display(box, self.calc_button)
