from model.analyze_model import AnalyzeModel
from model.analyze_state_model import state_model
from model.conduction_solver import ConductionSolver


class ConductionAnalysesController:
    def solve_preview(self, data):
        solver = ConductionSolver()
        results = solver.solve_conduction(data)
        return results, solver.errors

    def solve_analyses(self, params, analyze_id):
        solver = ConductionSolver()
        data = params.get("data", params)
        answers = solver.solve_conduction(data)
        if not answers:
            return {"errors": solver.errors, "status": -1}

        self._save_results(data, answers, analyze_id)
        return {"results": answers, "status": 0}

    def _save_results(self, user_inputs, results, analyze_id):
        analyze = state_model.get_analyze(analyze_id)
        AnalyzeModel().save_analyze(analyze_id, analyze, user_inputs, results)