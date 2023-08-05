# from PyThat import MeasurementTree
from h5to_nc import MeasurementTree
import h5to_nc
import xarray as xr
import matplotlib.pyplot as plt

# Define path to .h5 file
# paths = [r'D:\Pycharm\PyThat\examples\floquet_just_spectrum_analyzer_large_incomplete.h5',
#         r"D:\Pycharm\PyThat\examples\Spot_characterization_Thorlabs_R1DS2N_slit_hi_res.h5",
#         r'D:\Pycharm\PyThat\examples\Spot_characterization_on_Thorlabs_R1DS2N_across_slit_hi_res.h5',
#         r"D:\Pycharm\PyThat\examples\100mm_scan_radius - Kopie.h5",
#         r'D:\Pycharm\PyThat\examples\M486 Dispersion 40 mT.h5']
# path = r'D:\Pycharm\PyThat\examples\M486 Dispersion 40 mT.h5'
# path = r'D:\Pycharm\PyThat\examples\Spot_characterization_on_Thorlabs_R1DS2N_across_slit_hi_res.h5'
# path = r'D:\Pycharm\PyThat\examples\single.h5'
# path = r'D:\Pycharm\PyThat\examples\floquet_just_spectrum_analyzer_large_incomplete.h5'
# path = r'D:\Pycharm\PyThat\examples\repetitions.h5'
# path = r"C:\Users\Matthias\Desktop\along_antenna_heating_over_slm_2_spots_abwechselnd_laser.h5"
path = r"C:\Users\Matthias\Desktop\floquet_bls_angle_rotation_3.h5"

# index = (2, 1)
# index = (3,0)
# Optional: If the index is known beforehand, it can be specified here. Otherwise the user will be asked to choose.
# index = (2, 1)

# Create measurement_tree object. Path argument should point towards thatec h5 file.
# out = []
# for path in paths:
#     measurement_tree = MeasurementTree(path, index=True, override=True)
#     out.append(measurement_tree)
#     print()
#     print(f'self.logs: {measurement_tree.logs}')
#     print(f'self.devices: {measurement_tree.devices}')
#     print(f'self.labbook: {measurement_tree.labbook}')
#     print(f'self.tree_string:\n{measurement_tree.tree_string}')

# for i in out:
#     # print(i.dataset)
#     vars = i.dataset.data_vars
#     print(vars)
#     i.dataset[list(vars)[]].plot()
#     plt.show()


data = MeasurementTree(path, index=True, override=False)
d = data.dataset
print('Here1!')
print(d)
d = h5to_nc.consolidate_dims(d, 'Frequency', "Frequency")
d = h5to_nc.consolidate_dims(d, 'Frequency', "Frequency_1")
print('Here2!')
print(d)
# print(data.tree_string)
# print(data.definition)
# print(data.labbook)
# print(data.logs)
for i in data.dataset.values():
    for j in i.coords.values():
        print(f"Name: {j.name}, Units: {j.attrs['units']}")
exit()


# Take variable name from printout
interesting = "2,1: Acquire spectrum"

data = MeasurementTree(path).dataset['2,1: Acquire spectrum']

# Select and plot data
data[interesting].sel(dict(Frequency=slice(5, 15, None))).plot(col='Set Field')
plt.show()

data = data.rename({interesting: "The interesting stuff", "Winkel": "Angle"})
print(data)
data["The interesting stuff"].sel(dict(Frequency=slice(5, 15, None))).plot(col='Set Field')
plt.show()

