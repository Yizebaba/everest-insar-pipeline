README FILE FOR MT. EVEREST BALCONY AWS (27.9826°N, 86.9292°E, 8430 M ASL)

VARIABLES*
TIMESTAMP: Calendar date and time in Universal Time Coordinated (UTC).
T_HMP: Mean hourly temperature (°C) from Vaisala HMP 155A-L5-PT sensor installed in a naturally ventilated 
METSPEC 14-plate solar radiation shield.
T_109: Mean hourly temperature (°C) from CS109 sensor in a METSPEC 6-plate solar radiation shield.
RH: Mean hourly relative humidity (%) from Vaisala HMP 155A-L5-PT sensor installed in a naturally ventilated 
METSPEC 14-plate solar radiation shield.
WS_MAX: Maximum 5-sec wind speed (m s-1) from RM Young 05108-45 wind sensor #1 at 2.0 m above ground 
level.
WS_AVG: Mean hourly wind speed (m s-1) from RM Young 05108-45 wind sensor #1 at 2.0 m above ground level.
WD: Mean hourly wind direction (degrees) from RM Young 05108-45 wind sensor #1 at 2.0 m above ground 
level calculated using the Wind Vector CRBasic instruction.
WS_2_MAX: Maximum 5-sec wind speed (m s-1) from RM Young 05108-45 wind sensor #2 at 2.0 m above 
ground level.
WS_AVG_2: Mean hourly wind speed (m s-1) from RM Young 05108-45 wind sensor #2 at 2.0 m above ground 
level.
WD_2: Mean hourly wind direction (degrees) from RM Young 05108-45 wind sensor #2 at 2.0 m above ground 
level calculated using the Wind Vector CRBasic instruction.
PRESS: Mean hourly barometric pressure (hPa) from Vaisala PTB210 air pressure sensor with special low pressure 
characterization.
RHi: Mean hourly relative humidity with respect to ice (%) calculated using the measure Temperature and relative humidity (Buck, 1981, 1996)
EMPTY ROWS DENOTES MISSING VALUES


KNOWN ISSUES WITH AWS DATA (THROUGH 30 JUNE 2021)

1. Positive bias on T_HMP values during periods of calm wind and high solar radiation presumably due to limited 
ventilation of METSPEC 14-plate solar radiation shield.
2. Highly positive bias on T_109 values during daytime, likely due to insufficient ventilation of METSPEC 6-plate 
solar radiation shield resulting in artificial heating of sensor.
3. RH calculated with respect to water as opposed to ice resulting in negative bias at saturation (with respect to ice) 
during colder conditions.
4. Negative bias on WS_MAX, WS, WS_MAX_2, WS_2 at times during the monsoon season, likely 
due to rime ice accretion on the propellers.
5. Discrepancy noted between WDIR and WDIR_2, particularly beginning 1 NOVEMBER 2019.
6. No data from HMP155A-L5-PT sensor (T_HMP, RH) beginning 21 DECEMBER 2019 due to either sensor or cable failure.
7. No data from wind sensor 2 (WS_2, WS_MAX_2, WD_2) beginning 2 JANUARY 2020 due to either sensor or cable failure.
8. Last satellite data transmission at 0500 UTC 20 JANUARY 2020.
9. Tenzing Sherpa and Lakpa Sherpa made the first maintenance visit on 12 MAY 2021 and found the Balcony AWS toppled due to
anchor failure. They recovered the datalogger with new data through 10 FEBRUARY 2020 which are appended to the data file. 
Anchors likely failed on 20 JANUARY 2020.

REFERENCE FOR WEATHER DATA
This AWS was installed as part of the National Geographic and Rolex Perpetual Planet Expedition to Mt. Everest in 
April-May 2019. Please use the following citation for these data; Matthews, T., and Coauthors,  Going to Extremes: 
Installing the World’s Highest Weather Stations on Mount Everest. Bulletin of the American Meteorological Society, 101(11), 
E1870-E1890. DOI: https://doi.org/10.1175/BAMS-D-19-0198.1.

WEATHER DATA USE DISCLAIMER
Please note that the weather data have not been adjusted for quality assurance and represent information transmitted 
by remote automatic weather stations. The user assumes the entire risk related to any use of these data.  The 
National Geographic Society makes these data publicly available “as is” and disclaims all warranties whether 
express or implied including any implied warranties of merchantability or fitness of these data for weather 
forecasting or any other purpose, and further disclaims all warranties with respect to the accuracy, reliability, and/or 
continuing availability of these data.  In no event will National Geographic Society be liable for damages of any 
kind or lost profits concerning any use or misuse of these data. Additionally, these data may not be used in a manner 
that implies any endorsement or affiliation with National Geographic.   
