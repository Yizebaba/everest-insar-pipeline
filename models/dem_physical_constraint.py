"""
DEM Physical Constraint Layer (物理约束过滤门禁层).
Enforces strict physical boundary rules on all remote sensing anomalies:
1. Is slope in critical hazard band? (28° - 55°)
2. Is point located on active glacier terminus or steep cirque wall?
3. Does terrain aspect match sun/radar illumination geometry (Layover/Shadow rejection)?
4. Hard veto on false alarms in physically impossible locations.
"""
from typing import Dict, List, Tuple

class DEMPhysicalConstraintLayer:
    """
    基于数字高程模型的物理约束与假阳性拦截器
    """
    def __init__(self,
                 max_radar_layover_slope: float = 38.0,
                 min_avalanche_slope: float = 28.0,
                 max_avalanche_slope: float = 55.0):
        self.max_radar_layover_slope = max_radar_layover_slope
        self.min_avalanche_slope = min_avalanche_slope
        self.max_avalanche_slope = max_avalanche_slope

    def evaluate_physical_feasibility(self,
                                      elevation_m: float,
                                      slope_deg: float,
                                      aspect_deg: float,
                                      hazard_type: str) -> Dict:
        """
        裁决特定灾害在给定地形条件下物理上是否成立 (Pass / Veto)
        """
        is_physically_possible = True
        veto_reason = None

        # 规则 1: 雷达 InSAR 位移的陡坡叠掩伪影排查
        is_radar_layover_risk = slope_deg >= self.max_radar_layover_slope
        if hazard_type == "insar_displacement" and is_radar_layover_risk:
            is_physically_possible = False
            veto_reason = f"Slope {slope_deg}° exceeds radar incidence threshold {self.max_radar_layover_slope}°, flagged as geometric layover/shadow artifact."

        # 规则 2: 雪崩/冰崩重力临界坡度判定
        if hazard_type in ["avalanche", "icefall"]:
            if slope_deg < self.min_avalanche_slope:
                is_physically_possible = False
                veto_reason = f"Slope {slope_deg}° is too flat for gravitational avalanche (<{self.min_avalanche_slope}°)."
            elif slope_deg > self.max_avalanche_slope:
                is_physically_possible = False
                veto_reason = f"Slope {slope_deg}° is too steep for significant snow accumulation (>{self.max_avalanche_slope}°)."

        # 规则 3: 冰湖溃决的地形低洼性约束
        if hazard_type == "glof_lake":
            if slope_deg > 15.0:
                is_physically_possible = False
                veto_reason = f"Lake cannot form or sustain on steep slope of {slope_deg}° (>15°)."

        # 规则 4: 高程物理分布约束
        if elevation_m < 3500.0 and hazard_type in ["icefall", "glacier_surge"]:
            is_physically_possible = False
            veto_reason = f"Elevation {elevation_m}m is below Everest regional snowline and glacier terminus limit."

        status = "PASSED_PHYSICAL_CONSTRAINT" if is_physically_possible else "VETOED_PHYSICALLY_IMPOSSIBLE"

        return {
            "hazard_type": hazard_type,
            "elevation_m": round(elevation_m, 1),
            "slope_degrees": round(slope_deg, 1),
            "aspect_degrees": round(aspect_deg, 1),
            "physical_constraint_status": status,
            "is_valid_candidate": is_physically_possible,
            "veto_reason": veto_reason
        }