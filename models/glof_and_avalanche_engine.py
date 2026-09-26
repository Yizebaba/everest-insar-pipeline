"""
GLOF (Glacial Lake Outburst Flood) & Avalanche / Icefall Physical Mechanics Engine.
Complies with:
- Sentinel-2 NDWI / MNDWI Lake Surface Area Monitoring
- Sentinel-1 SAR Backscatter Loss (Wet snow / Dam seepage detection)
- Avalanche & Icefall Gravitational Potential Energy & Critical Slope Mechanics
"""
import math
from typing import Dict, List, Tuple

class GlacierLakeRiskEngine:
    """
    冰湖溃决风险评估引擎 (S2 光学水体 + S1 雷达渗流观测)
    """
    def __init__(self, critical_expansion_ratio: float = 1.15):
        self.critical_expansion_ratio = critical_expansion_ratio

    def evaluate_lake_expansion_and_breach_risk(self,
                                                lake_name: str,
                                                current_area_km2: float,
                                                baseline_area_km2: float,
                                                dam_sar_coherence: float,
                                                upstream_snowmelt_intensity: float) -> Dict:
        """
        评估冰湖面积扩张率与母坝稳定性
        """
        expansion_ratio = current_area_km2 / (baseline_area_km2 + 1e-6)
        
        # 风险规则:
        # 1. 面积急速扩张 (>15%)
        # 2. 冰碛坝相干性骤降 (<0.35 意味着坝体管涌渗漏或滑动)
        # 3. 上游强融温/积雪消融
        is_dam_seeping = dam_sar_coherence < 0.35
        is_expanding = expansion_ratio >= self.critical_expansion_ratio
        
        risk_score = 0.0
        if is_expanding: risk_score += 0.45
        if is_dam_seeping: risk_score += 0.35
        if upstream_snowmelt_intensity > 0.5: risk_score += 0.20

        level = "CRITICAL_BURST_HAZARD" if risk_score >= 0.7 else ("WATCH_EXPANSION" if risk_score >= 0.4 else "STABLE_NORMAL")

        return {
            "lake_name": lake_name,
            "current_area_km2": round(current_area_km2, 3),
            "baseline_area_km2": round(baseline_area_km2, 3),
            "expansion_ratio": round(expansion_ratio, 3),
            "dam_stability_coherence": round(dam_sar_coherence, 3),
            "glof_risk_score": round(risk_score, 2),
            "glof_risk_level": level,
            "recommended_action": "ISSUE_DOWNSTREAM_ALERT" if risk_score >= 0.7 else "CONTINUOUS_REMOTE_MONITORING"
        }

class AvalancheIcefallEngine:
    """
    雪崩与高位冰崩动力学判定引擎 (S2 + SAR + DEM 地形约束)
    """
    def __init__(self):
        pass

    def evaluate_avalanche_icefall_potential(self,
                                            slope_deg: float,
                                            elevation_drop_m: float,
                                            snow_water_equiv_mm: float,
                                            sar_wet_snow_detected: bool,
                                            recent_earthquake_detected: bool) -> Dict:
        """
        物理重力学与临界滑脱面破裂判定
        """
        # 物理临界条件:
        # 1. 临界坡度必须在 28° ~ 55° (过平不滑，过陡不积雪)
        # 2. 存在湿雪层重力加载 或 地震动剪切触发
        is_critical_slope = 28.0 <= slope_deg <= 55.0
        
        instability_index = 0.0
        if is_critical_slope:
            instability_index += 0.40
            if sar_wet_snow_detected: instability_index += 0.30
            if snow_water_equiv_mm > 50.0: instability_index += 0.15
            if recent_earthquake_detected: instability_index += 0.25

        can_collapse = is_critical_slope and (instability_index >= 0.60)
        
        # 潜在崩塌体积与动能级别
        hazard_class = "HIGH_POTENTIAL_AVALANCHE_ZONE" if can_collapse else ("MONITORED_ACCUMULATION" if is_critical_slope else "PHYSICALLY_STABLE_TERRAIN")

        return {
            "slope_degrees": round(slope_deg, 1),
            "is_critical_avalanche_slope": bool(is_critical_slope),
            "gravitational_instability_index": round(min(1.0, instability_index), 2),
            "avalanche_icefall_trigger_condition": bool(can_collapse),
            "hazard_classification": hazard_class
        }