# Validation against the codes

[`walidacja_pl.md`](walidacja_pl.md) – the validation document (in Polish): for every kind of object of the program
an example calculated by hand strictly to the code and compared with the result of KAYENN – snow (PN-EN 1991-1-3),
wind on buildings and other structures, the site, the structural factor and friction (PN-EN 1991-1-4), imposed loads
(PN-EN 1991-1-1), all with the Polish National Annexes and corrigenda.

The hand calculations are independent scripts – the formulas written out from the codes, no function or table of
the program is used on the hand side:

| Script | Part | Result file |
|---|---|---|
| `val_snow.py` | snow, examples S1–S8 | `snow_out.json` |
| `val_wind.py` | wind on buildings, W1–W12 | `wind_out.json` |
| `val_struct.py` | other structures B1–B12, site / cₛcd / friction T1–T4 | `struct_out.json` |
| `val_use.py` | imposed loads U1–U6 (the program form, offscreen) | `use_out.json` |

Run from this folder, e.g. `python val_wind.py` (`QT_QPA_PLATFORM=offscreen` for `val_use.py`). Every comparison is
printed with the hand value and the program value; the acceptance limit is 0.5 % (or 0.0015 absolute).
