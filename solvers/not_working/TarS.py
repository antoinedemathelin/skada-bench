from benchopt import safe_import_context

# Protect the import with `safe_import_context()`. This allows:
# - skipping import to speed up autocompletion in CLI.
# - getting requirements info when all dependencies are not installed.
with safe_import_context() as import_ctx:
    from skada import MMDTarSReweightAdapter, make_da_pipeline
    from benchmark_utils.base_solver import DASolver
    from xgboost import XGBClassifier


# The benchmark solvers must be named `Solver` and
# inherit from `BaseSolver` for `benchopt` to work properly.
class Solver(DASolver):

    # Name to select the solver in the CLI and to display the results.
    name = 'TarS'

    # List of parameters for the solver. The benchmark will consider
    # the cross product for each key in the dictionary.
    # All parameters 'p' defined here are available as 'self.p'.
    param_grid = {
        'mmdtarsreweightadapter__gamma': [0.1, 1, 10],
        'mmdtarsreweightadapter__reg': [1e-10, 1e-8, 1e-6],
        'mmdtarsreweightadapter__tol': [1e-6, 1e-4],
        'mmdtarsreweightadapter__max_iter': [1000],
    }

    def get_estimator(self):
        # The estimator passed should have a 'predict_proba' method.
        return make_da_pipeline(
            MMDTarSReweightAdapter(gamma=0.1),
            XGBClassifier()
            .set_fit_request(sample_weight=True)
            .set_score_request(sample_weight=True),
        )