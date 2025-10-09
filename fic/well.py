class Well:
    def __init__(self, well_id, absorbance, row, col, well_type="Combination", drug2_only=False):
        self.well_id = well_id
        self.absorbance = absorbance
        self.row = row
        self.col = col
        self.type = well_type
        self.drug2_only = drug2_only
        self.drug1_conc = None
        self.drug2_conc = None