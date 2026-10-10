README FILE FOR PHORTSE AWS (27.8456 N, 86.7472 E, 3810 M ASL)

VARIABLES*
TIMESTAMP: Calendar date and time in Universal Time Coordinated (UTC).
T_HMP: Sample hourly temperature (C) from Vaisala HMP 155A-L5-PT sensor installed in a naturally ventilated 
METSPEC 14-plate solar radiation shield.
RH: Mean hourly relative humidity (%) from Vaisala HMP 155A-L5-PT sensor installed in a naturally ventilated 
METSPEC 14-plate solar radiation shield. Calculated with respect to ice when T_HMP < 0 C.
PRECIP: Hourly precipitation total (mm) from OTT Pluvio2 1500 weighing precipitation gauge inside a Belfort 
double alter shield.
WS_MAX: Maximum hourly 3-sec wind speed (m s-1) from RM Young 05108-45 wind sensor at 2.3 m above 
ground level.
WS_AVG: Mean hourly wind speed (m s-1) from RM Young 05108-45 wind sensor at 2.3 m above ground level.
WDIR: Mean hourly wind direction (degrees) from RM Young 05108-45 wind sensor at 2.3 m above ground level 
calculated using the Wind Vector CRBasic instruction.
SW_IN_AVG: Maximum incoming short-wave radiation (W m-2) from Hukseflux SR30 radiation sensor.
SW_OUT_AVG: Mean hourly outgoing short-wave radiation (W m-2) from Hukseflux SR30 radiation sensor.
LW_IN_AVG: Mean hourly incoming long-wave radiation (W m-2) from Hukseflux IR20 radiation sensor.
LW_OUT_AVG: Mean hourly outgoing long-wave radiation (W m-2) from Hukseflux IR20 radiation sensor.
PRESS: Mean hourly barometric pressure (hPa) from Vaisala PTB110 air pressure sensor.
SR50A: Distance (m) from CS SR50A ultrasonic snow depth sensor to top of ground/snow/vegetation surface. 
Considerable noise is evident during non-winter months likely due to grass/vegetation/insects.

EMPTY CELL DENOTES MISSING VALUES



KNOWN ISSUES WITH AWS DATA (THROUGH 01 June 2025)
1. Positive bias on T_HMP values during periods of calm wind and high solar radiation presumably due to limited 
ventilation of METSPEC 14-plate solar radiation shield.
2. SR50A snow depth suspect from approximately 1 October 2021 to 10 April 2022 due to vegetation growth underneath
sensor. 

REFERENCE FOR WEATHER DATA
This AWS was installed as part of the National Geographic and Rolex Perpetual Planet Expedition to Mt. Everest in 
April-May 2019. Please use the following citation for these data; Matthews, T., and Coauthors,  Going to Extremes: 
Installing the World's Highest Weather Stations on Mount Everest. Bulletin of the American Meteorological Society, 
101(11), E1870-E1890. DOI: https://doi.org/10.1175/BAMS-D-19-0198.1.

WEATHER DATA USE DISCLAIMER
Please note that the weather data have not been adjusted for quality assurance and represent information transmitted 
by remote automatic weather stations. The user assumes the entire risk related to any use of these data.  The 
National Geographic Society makes these data publicly available  as is  and disclaims all warranties whether 
express or implied including any implied warranties of merchantability or fitness of these data for weather 
forecasting or any other purpose, and further disclaims all warranties with respect to the accuracy, reliability, and/or 
continuing availability of these data.  In no event will National Geographic Society be liable for damages of any 
kind or lost profits concerning any use or misuse of these data. Additionally, these data may not be used in a manner 
that implies any endorsement or affiliation with National Geographic.   

