from benchopt import safe_import_context

# Protect the import with `safe_import_context()`. This allows:
# - skipping import to speed up autocompletion in CLI.
# - getting requirements info when all dependencies are not installed.
with safe_import_context() as import_ctx:
    from benchmark_utils.base_solver import DASolver, FinalEstimator
    from skada.base import SelectSource
    from skada import make_da_pipeline

    from benchmark_utils.scorers import SupervisedScorer
    from benchmark_utils.base_solver import import_ctx as base_import_ctx
    if base_import_ctx.failed_import:
        exc, val, tb = base_import_ctx.import_error
        raise exc(val).with_traceback(tb)


# The benchmark solvers must be named `Solver` and
# inherit from `BaseSolver` for `benchopt` to work properly.
class Solver(DASolver):
    # Name to select the solver in the CLI and to display the results.
    name = 'NO_DA_SOURCE_ONLY'

    # List of parameters for the solver. The benchmark will consider
    # the cross product for each key in the dictionary.
    # All parameters 'p' defined here are available as 'self.p'.
    default_param_grid = {
        'finalestimator__estimator_name': ["LR", "SVC", "XGB"]
    }

    def get_estimator(self, **kwargs):
        self.criterions = {
            'supervised': SupervisedScorer(),
        }
        # The estimator passed should have a 'predict_proba' method.
        return make_da_pipeline(
            ('finalestimator', SelectSource(FinalEstimator())),
        )
