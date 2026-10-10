README FILE FOR MT. EVEREST CAMP II AWS (27.9810 N, 86.9023 E, 6464 M ASL)

VARIABLES*
TIMESTAMP: Calendar date and time in Universal Time Coordinated (UTC).
T_HMP: Sample hourly temperature (C) from Vaisala HMP 155A-L5-PT sensor installed in a naturally ventilated 
METSPEC 14-plate solar radiation shield.
T_109: Sample hourly temperature (C) from CS109 sensor in a METSPEC 6-plate solar radiation shield.
RH: Mean hourly relative humidity (%) from Vaisala HMP 155A-L5-PT sensor installed in a naturally ventilated 
METSPEC 14-plate solar radiation shield. Calculated with respect to ice when T_HMP < 0 C.
WS_MAX: Maximum 60-sec wind speed (m s-1) from RM Young 05108-45 wind sensor at 2.0 m above ground 
level.
WS_AVG: Mean hourly wind speed (m s-1) from RM Young 05108-45 wind sensor at 2.0 m above ground level.
WDIR: Mean hourly wind direction (degrees) from RM Young 05108-45 wind sensor at 2.0 m above ground level 
calculated using the Wind Vector CRBasic instruction.
SW_IN_AVG: Maximum incoming short-wave radiation (W m-2) from Apogee SN-500-SS radiation sensor.
SW_OUT_AVG: Mean hourly outgoing short-wave radiation (W m-2) from Apogee SN-500-SS radiation sensor.
LW_IN_AVG: Mean hourly incoming long-wave radiation (W m-2) from Apogee SN-500-SS radiation sensor.
LW_OUT_AVG: Mean hourly outgoing long-wave radiation (W m-2) from Apogee SN-500-SS radiation sensor.
PRESS: Mean hourly barometric pressure (hPa) from Vaisala PTB210 air pressure sensor with special low pressure
characterization.
RHi: Mean hourly relative humidity with respect to ice (%) calculated using the measure Temperature and relative humidity (Buck, 1981, 1996)

EMPTY ROWS DENOTES MISSING VALUES



KNOWN ISSUES WITH AWS DATA (THROUGH 01 June 2025)
1. Positive bias on T_HMP values during periods of calm wind and high solar radiation presumably due to limited 
ventilation of METSPEC 14-plate solar radiation shield.
2. Highly positive bias on T_109 values during daytime, likely due to insufficient ventilation of METSPEC 6-plate 
solar radiation shield resulting in artificial heating of sensor.
3. Some radiation measurements are suspect and we have set values to -999 or empty rows when above/below the following thresholds: 
SW_IN_thresh_upper=1400
SW_IN_thresh_lower=0
SW_OUT_thresh_lower=0
SW_OUT_thresh_upper=1200
LW_IN_AVG_thresh_upper=400
LW_IN_AVG_lower=60
LW_OUT_thresh_lower=100
LW_OUT_thresh_upper=600
4. Erroneous T_HMP values noted from 28 December 2020 through 31 December 2020 following high wind event and values  have been set to -999.
5. Erroneous T_HMP values continued at times from 28 December 2020 presumably due to HMP 155A-L5-PT sensor being dislodged from METSPEC 14-plate solar radiation shield. Values left for user to decide how to address.
6. Tenzing Gyalzen and Lakpa Sherpa replaced the HMP 155A-L5-PT sensor with an improved bracket to keep sensor from vibrating loose from the radiation shield on 8 May 2021. 

REFERENCE FOR WEATHER DATA
This AWS was installed as part of the National Geographic and Rolex Perpetual Planet Expedition to Mt. Everest in April-May 2019. Please use the following citation for these data; Matthews, T., and Coauthors,  Going to Extremes:  Installing the World's Highest Weather Stations on Mount Everest. Bulletin of the American Meteorological Society, 101(11), 
E1870-E1890. DOI: https://doi.org/10.1175/BAMS-D-19-0198.1.

WEATHER DATA USE DISCLAIMER
Please note that the weather data have not been adjusted for quality assurance and represent information transmitted by remote automatic weather stations. The user assumes the entire risk related to any use of these data. The 
National Geographic Society makes these data publicly available  as is  and disclaims all warranties whether 
express or implied including any implied warranties of merchantability or fitness of these data for weather 
forecasting or any other purpose, and further disclaims all warranties with respect to the accuracy, reliability, and/or continuing availability of these data.  In no event will National Geographic Society be liable for damages of any kind or lost profits concerning any use or misuse of these data. Additionally, these data may not be used in a manner that implies any endorsement or affiliation with National Geographic.   
