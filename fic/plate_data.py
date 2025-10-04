import pandas as pd

from fic.well import Well


class PlateData:
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)
        self.wells = self._parse_plate()

    def _parse_plate(self):
        wells = []
        for _, row in self.df.iterrows():
            row_label = row["Blank subtracted"]
            for col in range(1, 13):  # columns 1–12
                well_id = f"{row_label}{col}"
                value = float(row[str(col)])
                # classify type
                if col == 11:
                    well_type = "GrowthControl"
                elif col == 12:
                    well_type = "Blank"
                else:
                    well_type = "Combination"
                wells.append(Well(well_id, value, row_label, col, well_type))
        return wells

    def get_growth_controls(self):
        return [w for w in self.wells if w.type == "GrowthControl"]

    def get_combinations(self):
        return [w for w in self.wells if w.type == "Combination"]