from gettext import gettext as _

class AnalyzeModel:
    def __init__(self):
        self.analyze_options = {
            "new_fin_analyze": {
                "label": _("\uf2c8 FIN"), 
                "button": _("FIN ANALYZE"), 
                "tag": "fin"
                }, 
            "new_conduction_analyze": {
                "label": _("\uf029 CONDUCTION"), 
                "button": _("CONDUCTION ANALYZE"), 
                "tag": "conduction"
                },
            "new_cconvection_analyze": {
                "label": _("\uf773 CONVECTION"), 
                "button": _("CONVECTION ANALYZE"), 
                "tag": "convection"
                }
        }

    def get_analyze_options(self):
        return self.analyze_options