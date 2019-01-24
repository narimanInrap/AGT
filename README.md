AGT
===

Electrical resistivity processing module (Geoscan Research RM15/RM85) contains:
	Import
	Processing: 
		Median filtering
		Georeferencing
Magnetic data processing module (Sensys MXPDA - GNSS) contains:
	Import
	Processing:
		Decimation(raw - median moving window)
		Median removal
		Trend removal
		Stationary point removal
Magnetic data processing module (Sensys MXPDA/Grad601 - grid survey) contains:
	Import
	Processing:	
		Median removal
		Trend removal
		Georeferencing
Electromagnetic data processing module (Geonics EM31) contains:
	Import
	Processing:
		Apparent conductivity calculation
Electromagnetic data processing module (Geophex GEM2, GSSI EMP400) contains:
	Importing
	Processing:
		Spatial GNSS/GEM2/EMP400 shift
		Median filtering by profile (in-phase, out-of-phase)
		Moving window filter
		Geophysical parameter calculation:
			Calibration
			Electrical conductivity and magnetic susceptibility computation

Coming soon:	
	RM15/RM85 Download module
	Advanced processing module 

Please consult the help file for more details.