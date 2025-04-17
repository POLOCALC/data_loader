# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: polocalc
#     language: python
#     name: python3
# ---

# %%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import sys
sys.path.append("../")
from get_payload_data import read_inclino_file, read_log_time

# %matplotlib widget

color_angles = {"yaw":"cornflowerblue", "pitch":"darkorange", "roll":"forestgreen"}


# %% [markdown]
# # Notebook to have a quick look on inclinometer data (Kernel-100)

# %% [markdown]
# ## Plot raw (yaw, pitch, roll) data

# %%
inclino_path = "/home/tsouverin/polocalc/data_loader/quick_look/20250416_115757/sensors_data/Kernel-100_20250416_115757.bin"
logfile = "/home/tsouverin/polocalc/data_loader/quick_look/20250416_115757/file.log"
inclino_data = read_inclino_file(inclino_path, logfile)

# %%
timestamps = inclino_data["datetime"] if "datetime" in inclino_data.keys() else inclino_data["timestamp"]
time_label = "Datetime" if "datetime" in inclino_data.keys() else "timestamps [s]"

fig, axs = plt.subplots(3, 1, figsize=(10, 7), sharex=True)
axs[0].plot(timestamps, inclino_data["pitch"], color=color_angles["pitch"], label="Pitch")
axs[0].set_ylabel("Pitch [deg]")
axs[0].grid(color="gray")
axs[0].legend()
axs[1].plot(timestamps, inclino_data["roll"], color=color_angles["roll"], label="Roll")
axs[1].set_ylabel("Roll [deg]")
axs[1].grid(color="gray")
axs[1].legend()
axs[2].plot(timestamps, inclino_data["yaw"], color=color_angles["yaw"], label="Yaw")
axs[2].set_ylabel("Yaw [deg]")
axs[2].set_xlabel(time_label)
axs[2].grid(color="gray")
axs[2].legend()

plt.tight_layout()
plt.show()

# %% [markdown]
# ## Plot temperature

# %%
plt.figure()
plt.plot(timestamps, inclino_data["Temper"])
plt.show()

# %%
