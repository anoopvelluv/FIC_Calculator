class FICCalculator:
    def __init__(self, plate_data, mic_drug1, mic_drug2, drug1_concs, drug2_concs):
        """
        drug1_concs: dict mapping (col) -> Drug1 concentration
        drug2_concs: dict mapping (row) -> Drug2 concentration
        """
        self.plate = plate_data
        self.mic_drug1 = mic_drug1
        self.mic_drug2 = mic_drug2
        self.drug1_concs = drug1_concs
        self.drug2_concs = drug2_concs
        self.cutoff = self._calculate_cutoff()
        print(f"Cutoff - {self.cutoff }")
        self._assign_concentrations()

    def _calculate_cutoff(self):
        controls = self.plate.get_growth_controls()
        mean_growth = sum(w.absorbance for w in controls) / len(controls)
        return mean_growth * 0.1

    def _assign_concentrations(self):
        for w in self.plate.get_combinations():
            if w.col in self.drug1_concs:
                w.drug1_conc = self.drug1_concs[w.col]
            if w.row in self.drug2_concs:
                w.drug2_conc = self.drug2_concs[w.row]

    def calculate_fic(self, well):
        if well.drug1_conc is None or well.drug2_conc is None:
            return None
        FIC1 = well.drug1_conc / self.mic_drug1
        FIC2 = well.drug2_conc / self.mic_drug2

        print("-")
        print(f"For Well {well.row}-{well.col} ")
        print(f"FIC1 = {well.drug1_conc} / {self.mic_drug1} = {FIC1}")
        print(f"FIC2 = {well.drug2_conc} / {self.mic_drug2} = {FIC2}")
        print(f"Total {FIC1 + FIC2}")
        print("-")

        return FIC1 + FIC2

    def find_min_fic(self):
        candidate_wells = [w for w in self.plate.get_combinations() if w.absorbance <= self.cutoff]
        print(f"Absorbance values <= cutoff : {[w.absorbance for w in candidate_wells]}")

        candidate_wells = [w for w in candidate_wells if self.calculate_fic(w) is not None]

        if not candidate_wells:
            return None, None

        min_well = min(candidate_wells, key=lambda w: self.calculate_fic(w))
        print(f"Minimum Well Value(absorbance) : {min_well.absorbance}")

        min_fic = self.calculate_fic(min_well)
        return min_well, min_fic

    @staticmethod
    def interpret_fic(fic_value):
        if fic_value is None:
            return "No valid wells found"
        if fic_value <= 0.5:
            return "Synergy"
        elif fic_value <= 1.0:
            return "Additive"
        elif fic_value <= 4.0:
            return "Indifferent"
        else:
            return "Antagonism"