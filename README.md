# delimclean
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Last commit](https://img.shields.io/github/last-commit/almtronics/delimclean)

A simple CLI tool for cleaning delimited files by skipping rows, keeping selected columns, renaming output columns and writing cleaned CSV files to an output folder.
## Features

- Clean a single file or an entire folder
- Skip a fixed number of rows at the top of a file
- Keep selected columns by column numbers
- Rename output columns
- Support tab, comma, semicolon, or a custom single character separator
- Write cleaned CSV files to a separate output folder

## Installation

```bash
py -m pip install -e .
```

## Arguments
- `path` - Input file or folder
- `--skiprows` - Number of rows to skip at the top of the file
- `--keepcols` - Column numbers to keep, starting from 1
- `--sep` - Separator: `tab`, `comma`, `semicolon` or a custom single character like `|`
- `--pattern` - File pattern when input is a folder, for example *.tx
- `--suffix` - Suffix added to each output filename
- `--names` - Optional output column names
- `--no-header` - Treat the input file as having no header row
- `--outdir` - Output folder for cleaned files
- `--version` - Show the installed version

## Example Usage
With an input file like this:

```text
Terahertz Time-Domain Spectroscopy Measurement Use Y for E(t). Amplitude will give you noise floor and peak amplitude. Random phase indicates signal was too weak (or noisy) to measure properly Lock-In Parameters:
f_Chopper(Hz)	Period of Modulation (s)	Time Constant (s)	Waiting Time(s)	Slope (dB/s)	Sensitivity (V)	Input Couple	Ground Reserve
325.157E+0	3.075E-3	30 ms	150	24	100 mV/nA	I (1e6)	Ground	DC	Normal
Scan Parameters:
Start Position (mm)	Stop Position (mm)	Step Size (mm)	Number of Points in Scan	Scan Speed (mm/s)	Scan Distance (mm)	Max Frequency (THz)	Frequency resolution (THz)
40.120E+0	57.120E+0	10.000E-3	1701	0.000000	17.000000	7.500000	0.008824
Position  (mm)	Time (ps)	Amplitude (pA)	Phase (Degrees)	X (pA)	Y (pA)	E(t) (pA)
40.120000	267.466667	247.384000	85.422400	19.743525	246.594884	19.743525
40.130000	267.533333	254.660000	86.984900	13.394896	254.307476	13.394896
40.140000	267.600000	258.298000	84.867700	23.106252	257.262430	23.106252
40.150000	267.666667	258.298000	85.594200	19.842442	257.534724	19.842442
40.160000	267.733333	254.660000	88.508300	6.629344	254.573697	6.629344
40.170000	267.800000	258.298000	86.328600	16.539900	257.767897	16.539900
40.180000	267.866667	265.574000	86.414600	16.607989	265.054191	16.607989
40.190000	267.933333	251.022000	86.281700	16.279036	250.493588	16.279036
40.200000	268.000000	254.660000	86.328600	16.306943	254.137363	16.306943
40.210000	268.066667	265.574000	85.703600	19.895761	264.827695	19.895761
40.220000	268.133333	254.660000	84.797400	23.092001	253.610873	23.092001
40.230000	268.200000	261.936000	84.930200	23.147096	260.911249	23.147096
40.240000	268.266667	261.936000	86.328600	16.772856	261.398430	16.772856
```

To skip the metadata rows, keep only three useful columns, rename them and put the results in an output directory:

```bash
delimclean "DATA PATH" --skiprows 6 --keepcols 2 5 6 --sep tab --names time real imag --outdir cleaned
```

This would produce output like:

```csv
time,real,imag
267.466667,19.743525,246.594884
267.533333,13.394896,254.307476
267.600000,23.106252,257.262430
267.666667,19.842442,257.534724
267.733333,6.6293440,254.573697
267.800000,16.539900,257.767897
267.866667,16.607989,265.054191
267.933333,16.279036,250.493588
268.000000,16.306943,254.137363
268.066667,19.895761,264.827695
268.133333,23.092001,253.610873
268.200000,23.147096,260.911249
268.266667,16.772856,261.398430
```

## License

MIT — see [LICENSE](LICENSE).