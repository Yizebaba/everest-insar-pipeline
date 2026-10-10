README FILE FOR MT. EVEREST SOUTH COL AWS (27.9719 N, 86.9295 E, 7945 M ASL)

VARIABLES*
TIMESTAMP: Calendar date and time in Universal Time Coordinated (UTC).
T_HMP: Mean hourly temperature (∞C) from Vaisala HMP 155A-L5-PT sensor installed in a naturally ventilated 
METSPEC 14-plate solar radiation shield.
T_109: Mean hourly temperature (∞C) from CS109 sensor in a METSPEC 6-plate solar radiation shield.
RH: Mean hourly relative humidity (%) from Vaisala HMP 155A-L5-PT sensor installed in a naturally ventilated 
METSPEC 14-plate solar radiation shield. Calculated with respect to ice when T_HMP < 0 ∞C.
WS_MAX: Maximum 5-sec wind speed (m s-1) from RM Young 05108-45 wind sensor #1 at 2.0 m above ground 
level through 9 May 2022. An Arklay Richards C5C stainless steel 3-cup anemometer replaced the RM Young 
05108-45 on 9 May 2022.
WS_AVG: Mean hourly wind speed (m s-1) from RM Young 05108-45 wind sensor #1 at 2.0 m above ground level through 
9 May 2022. An Arklay Richards C5C stainless steel 3-cup anemometer replaced the RM Young 05108-45 on 9 May 2022.
WDIR: Mean hourly wind direction (degrees) from RM Young 05108-45 wind sensor #1 at 2.0 m above ground 
level calculated using the Wind Vector CRBasic instruction through 9 May 2022. An Arklay Richards D5 wind vane 
replaced the RM Young 05108-45 on 9 May 2022 but orientation not known. 
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
2. Highly positive bias on T_109 values during daytime, likely due to insufficient ventilation of METSPEC 6-plate 
solar radiation shield resulting in artificial heating of sensor.
3. Negative bias on WS_MAX, WS_AVG, WS_MAX_2, WS_AVG_2 at times during the monsoon season due to 
rime ice accretion on the propellers.
4. WDIR_2 offset by 180 degrees due to apparent internal wiring error through 10 MAY 2021.
5. Erroneous data from wind sensor 1 (WS_AVG, WS_MAX, WDIR) beginning 15 DECEMBER 2019 due to sensor and/or mount 
damage/failure.
6. No data from wind sensor 2 (WS_AVG_2, WS_MAX_2, WDIR_2) beginning 5 JANUARY 2020 due to either sensor or cable 
failure.
7. No data from 1 SEPTEMBER 2020 through 7 OCTOBER 2020 due to low battery voltage presumably caused by burial of solar 
panels by deep snow. Intermittent data from 7 OCTOBER 2020 through 11 OCTOBER 2020 as snow began to ablate.
8. Tenzing Gyalzen Sherpa and Lakhpa Sherpa replaced 155A-L5-PT sensor on 10 MAY 2021 but the new sensor has had some 
erroneous data that have been removed and converted to -999.
9. Tenzing Gyalzen Sherpa and Lakhpa Sherpa replaced the battery pack on 10 MAY 2021.
10. Tenzing Gyalzen Sherpa and Lakhpa Sherpa replaced the 05108-45 wind sensors on 10 MAY 2021 but a factory wiring
error resulted in no wind data through 9 MAY 2022.
11. Erroneous data from T_HMP and RH from 18 JULY 2021 to 9 MAY 2022 due to either sensor or cable failure.
12. No data from 22 JULY 2021 through 9 MAY 2022 due to low battery voltage and failure presumably caused by burial of solar 
panels by deep snow.
13. No data from 14 DECEMBER 2022 to 14 MAY 2023 due to faulty connector and/or cable between battery and datalogger
enclosures. 
14. No data from wind sensor 1 or 2 from 14 MAY 2023 due to inaccurate internal wiring diagram from Campbell Scientific.
Experimental wind data from Mount Washington Observatory pitot available by request.
15. No data from LW_IN or LW_OUT from 14 MAY 2023 due to inaccurate cable connector diagram from Campbell Scientific.
16. Baker Perry and Tenzing Gyalzen Sherpa installed a new 24 Ahr lithium-ion battery on 14 May 2023.
17. Baker Perry and Rajesh Thapa Magar replaced the battery on 11 May 2024
18. Arbindra Khadka downloded the AWS and added the SD card on 18 May 2025

EMPTY CELL DENOTES MISSING VALUES



REFERENCE FOR WEATHER DATA
This AWS was installed as part of the National Geographic and Rolex Perpetual Planet Expedition to Mt. Everest in 
April-May 2019. Please use the following citation for these data; Matthews, T., and Coauthors,  Going to Extremes: 
Installing the Worldís Highest Weather Stations on Mount Everest. Bulletin of the American Meteorological Society, 101(11), 
E1870-E1890. DOI: https://doi.org/10.1175/BAMS-D-19-0198.1.

WEATHER DATA USE DISCLAIMER
Please note that the weather data have not been adjusted for quality assurance and represent information transmitted 
by remote automatic weather stations. The user assumes the entire risk related to any use of these data.  The 
National Geographic Society makes these data publicly available and disclaims all warranties whether express or implied 
including any implied warranties of merchantability or fitness of these data for weather  forecasting or any other 
purpose, and further disclaims all warranties with respect to the accuracy, reliability, and/or continuing availability 
of these data.  In no event will National Geographic Society be liable for damages of any kind or lost profits concerning 
any use or misuse of these data. Additionally, these data may not be used in a manner that implies any endorsement or 
affiliation with National Geographic.  
