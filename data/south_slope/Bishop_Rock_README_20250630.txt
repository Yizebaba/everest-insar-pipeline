README FILE FOR MT. EVEREST BISHOP ROCK AWS (27.9735 N, 86.9308 E, 8810 M ASL)

VARIABLES
TIMESTAMP: Calendar date and time in Universal Time Coordinated (UTC).
T_HMP: Mean hourly temperature (C) from Vaisala HMP 155A-L5-PT sensor installed in a naturally ventilated 
METSPEC 14-plate solar radiation shield.
RH: Mean hourly relative humidity (%) from Vaisala HMP 155A-L5-PT sensor installed in a naturally ventilated 
METSPEC 14-plate solar radiation shield. Calculated with respect to ice when T_HMP < 0 C.
T_HMP_2: Mean hourly temperature (C) from Vaisala HMP 155A-L5-PT sensor installed in a naturally ventilated 
METSPEC 14-plate solar radiation shield.
RH_2: Mean hourly relative humidity (%) from Vaisala HMP 155A-L5-PT sensor installed in a naturally ventilated 
METSPEC 14-plate solar radiation shield. Calculated with respect to ice when T_HMP < 0 C.
WS_MAX: Maximum 5-sec wind speed (m s-1) from Arklay Richards C5C stainless steel 3-cup anemometer installed at 
2.0 m above ground level.
WS_AVG: Mean hourly wind speed (m s-1) from Arklay Richards C5C stainless steel 3-cup anemometer installed at 
2.0 m above ground level.
WDIR: Mean hourly wind direction (degrees) from Arklay Richards D5 wind vane but orientation not known. 
WS_MAX_2: Maximum 5-sec wind speed (m s-1) from RM Young 05108-45 wind sensor #2 at 2.0 m above ground 
level.
WS_AVG_2: Mean hourly wind speed (m s-1) from RM Young 05108-45 wind sensor #2 at 2.0 m above ground 
level.
WDIR_2: Mean hourly wind direction (degrees) from RM Young 05108-45 wind sensor #2 at 2.0 m above ground 
level calculated using the Wind Vector CRBasic instruction.
SW_IN_AVG: Mean hourly incoming short-wave radiation (W m-2) from Hukseflux NR01 radiation sensor.
SW_OUT_AVG: Mean hourly outgoing short-wave radiation (W m-2) from Hukseflux NR01 radiation sensor.
LW_IN_AVG: Mean hourly incoming long-wave radiation (W m-2) from Hukseflux NR01 radiation sensor.
LW_OUT_AVG: Mean hourly outgoing long-wave radiation (W m-2) from Hukseflux NR01 radiation sensor.
PRESS: Mean hourly barometric pressure (hPa) from Vaisala PTB210 air pressure sensor with special low pressure 
characterization.
RHi: Mean hourly relative humidity with respect to ice (%) calculated using the measure Temperature and relative humidity (Buck, 1981, 1996)

KNOWN ISSUES WITH AWS DATA (THROUGH 30 JUNE 2025)
1. Positive bias on T_HMP values during periods of calm wind and high solar radiation presumably due to limited 
ventilation of METSPEC 14-plate solar radiation shield.
2. Negative bias on WS_MAX, WS_AVG, WS_MAX_2, WS_AVG_2 at times during the monsoon season due to rime ice 
accretion on the propellers.
3. WDIR not oriented to true north and offset unknown.
4. No data between 8 JULY 2022 and 15 May 2023 due to failure of power cable connecting battery enclosure with 
datalogger enclosure.
5. Arklay Richards C5C stainless steel 3-cup anemometer destroyed between October 2022 and April 2023 and hence no 
WS_MAX, WS_AVG, or WDIR since 15 May 2023.
6. There is very short period of daytime data in Dec 2022 and Jan 2023. 

EMPTY ROWS DENOTES MISSING VALUES



REFERENCE FOR WEATHER DATA
This AWS was installed as part of the National Geographic and Rolex Perpetual Planet Return to Everest Expedition in
April-May 2022. Please use the following citation for these data; Matthews, T., and Coauthors,  Going to Extremes: 
Weather observations reach the summit of Mount Everest. Bulletin of the American Meteorological Society, 2022: 103: 
E2827-E2835, https://doi.org/10.1175/BAMS-D-22-0120.1 

WEATHER DATA USE DISCLAIMER
Please note that the weather data have not been adjusted for quality assurance and represent information transmitted 
by remote automatic weather stations. The user assumes the entire risk related to any use of these data.  The 
National Geographic Society makes these data publicly available and disclaims all warranties whether express or implied 
including any implied warranties of merchantability or fitness of these data for weather  forecasting or any other 
purpose, and further disclaims all warranties with respect to the accuracy, reliability, and/or continuing availability 
of these data.  In no event will National Geographic Society be liable for damages of any kind or lost profits concerning 
any use or misuse of these data. Additionally, these data may not be used in a manner that implies any endorsement or 
affiliation with National Geographic.  
