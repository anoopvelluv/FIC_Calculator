from fic.fic_calculator import FICCalculator
from fic.plate_data import PlateData

if __name__ == "__main__":
    plate = PlateData("data/plate_data.csv")

    # MIC values (from single drug MIC test)
    mic_drug1 = 0.125
    mic_drug2 = 0.5

    # Define concentration layout (column = drug1, row = drug2)
    drug1_concs = {1: 0, 2: 0.5, 3: 0.25, 4: 0.125, 5: 0.063, 6: 0.031, 7: 0.016, 8: 0.0078, 9: 0.0039, 10: 0.0019}
    drug2_concs = {"A": 2.0, "B": 1.0, "C": 0.5, "D": 0.25, "E": 0.125, "F": 0.063, "G": 0.031, "H": 0.016}

    calc = FICCalculator(plate, mic_drug1, mic_drug2, drug1_concs, drug2_concs)

    well, fic_val = calc.find_min_fic()
    if well:
        print(f"Best well: {well.well_id} (Row {well.row}, Col {well.col}), "
              f"D1={well.drug1_conc}, D2={well.drug2_conc}, Abs={well.absorbance:.4f}")
        print(f"FIC_min = {fic_val:.4f} → {calc.interpret_fic(fic_val)}")
    else:
        print("No wells met the 90% inhibition cutoff.")


    drug2_mic_value = calc.find_min_mic_drug_2()
    print(f"Drug 2 MIC Value : {drug2_mic_value}")
