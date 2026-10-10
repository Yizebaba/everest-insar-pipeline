OTT PARSIVEL2 DATA METADATA 
all details about the sensor are available in: 
https://mail.google.com/mail/u/0/#inbox/FMfcgzQgMVZLKksWnxZcxVrTghcFVvKn

Instrument Name:       OTT Parsivel² Laser Present Weather Sensor (Optical Disdrometer)
Manufacturer:          OTT HydroMet GmbH
Measurement Principle: Laser-optical extinction method (650 nm laser band)
Measurement Grid:      32 size classes (0.2 to 8 mm for liquid; up to 25 mm for solid)
                       32 velocity classes (0.2 to 20 m/s)
Precipitation Types:   Drizzle, Drizzle with Rain, Rain, Sleet, Snow, Snow Grains, Soft Hail, Hail


intensity: Precipitation intensity (unit : mm/h)--  The real-time rate of precipitation (rain rate) based on the falling hydrometeor sizes and quantities detected

p_tot: Cumulative Total Precipitation Amount (unit : mm)-- Cumulative accumulation of equivalent liquid precipitation  recorded since the start of measurement or the last reset. Might not be useful since Parisvel2 was only powered one for three minutes each hour due to power constraints. (* might not be useful since Parisvel2 was only powered one for three minutes each hour due to power constraints)

synop: Precipitation code according to WMO Table 4680


radar(unit : dBz): Equivalent Radar Reflectivity -- Computed radar reflectivity factor (Z) derived from 		the  measured particle size distribution. Typically ranges 
                       from -9.99 to 99.99 dBZ

visib(unit m): Visibility in Precipitation -- Meteorological Optical Range (MOR) calculated 				specifically during precipitation events, ranging up to 20,000 meters.

interval: Sampling Interval (unit: Second) -- The length of time over which the current row of data was 
                       integrated and averaged (typically 10, 30, or 60 seconds).

signal: Signal Quality / Status -- Error, diagnostic, or laser attenuation status codes 
                       indicating whether the optical window is clean, distorted, 
                       or if an instrumental fault is detected.


particles: Total Particle Count -- The absolute total number of valid hydrometeor particles 
                       detected passing through the laser beam during the 
                       sampling interval.

