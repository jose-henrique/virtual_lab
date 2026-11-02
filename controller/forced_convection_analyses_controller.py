from model.analyze_model import AnalyzeModel
from model.analyze_state_model import state_model
from model.forced_convection_solver import ForcedConvectionSolver


class ForcedConvectionAnalysesController:
    def solve_preview(self, data):
        solver = ForcedConvectionSolver()
        results = solver.solve(data)
        return results, solver.errors

    def solve_analyses(self, params, analyze_id):
        solver = ForcedConvectionSolver()
        data = params.get("data", params)
        results = solver.solve(data)
        if not results:
            return {"errors": solver.errors, "status": -1}

        analyze = state_model.get_analyze(analyze_id)
        AnalyzeModel().save_analyze(analyze_id, analyze, {"data": data}, results)
        return {"results": results, "status": 0}