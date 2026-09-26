"""
Glacier State Database (SQLite Cloud-Native Engine)
Persistent State & Baseline Storage for Mount Everest Glaciers (L1 Mapping & L2 Motion).
Records:
- RGI 7.0 / GLIMS boundary geometry and historical area (km2)
- Multi-temporal terminus retreat & surface elevation changes
- Multi-sensor observations and automated status tags
"""
import os
import sqlite3
import json
import datetime
from typing import Dict, List, Optional

class GlacierStateDatabase:
    def __init__(self, db_path: str = "data/glacier_state.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_tables()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_tables(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # 冰川基础档案表 (Glacier Inventory)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS glacier_inventory (
                glacier_id TEXT PRIMARY KEY,
                rgi_id TEXT,
                name TEXT,
                center_lon REAL,
                center_lat REAL,
                baseline_area_km2 REAL,
                mean_elevation_m REAL,
                debris_fraction REAL,
                geometry_geojson TEXT,
                created_at TEXT
            )
            """)
            # 冰川动态状态与异常日志表 (Glacier Observations & State History)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS glacier_state_history (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                glacier_id TEXT,
                observation_date TEXT,
                velocity_m_yr REAL,
                velocity_z_score REAL,
                displacement_los_mm REAL,
                insar_coherence REAL,
                crevasse_count INTEGER,
                lake_risk_level TEXT,
                stability_status TEXT,
                engine_confidence REAL,
                payload_json TEXT,
                FOREIGN KEY (glacier_id) REFERENCES glacier_inventory (glacier_id)
            )
            """)
            conn.commit()

    def populate_rgi_baselines(self, rgi_catalog: Dict):
        """导入 RGI 7.0 珠峰权威冰川先验多边形与基准属性"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for rgi_id, data in rgi_catalog.items():
                center_lon = (data["primary_bbox"][0] + data["primary_bbox"][2]) / 2.0
                center_lat = (data["primary_bbox"][1] + data["primary_bbox"][3]) / 2.0
                cursor.execute("""
                INSERT OR REPLACE INTO glacier_inventory 
                (glacier_id, rgi_id, name, center_lon, center_lat, baseline_area_km2, mean_elevation_m, debris_fraction, geometry_geojson, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    data["glims_id"],
                    rgi_id,
                    data["name"],
                    center_lon,
                    center_lat,
                    data["area_km2"],
                    data["mean_elevation_m"],
                    data["debris_covered_fraction"],
                    json.dumps(data["primary_bbox"]),
                    datetime.datetime.utcnow().isoformat()
                ))
            conn.commit()

    def record_observation_state(self, glacier_id: str, obs_date: str, state_data: Dict):
        """记录每一次卫星过境的真实物理状态与反演特征"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO glacier_state_history 
            (glacier_id, observation_date, velocity_m_yr, velocity_z_score, displacement_los_mm, insar_coherence, crevasse_count, lake_risk_level, stability_status, engine_confidence, payload_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                glacier_id,
                obs_date,
                state_data.get("velocity_m_yr"),
                state_data.get("velocity_z_score"),
                state_data.get("displacement_los_mm"),
                state_data.get("insar_coherence"),
                state_data.get("crevasse_count", 0),
                state_data.get("lake_risk_level", "NORMAL"),
                state_data.get("stability_status", "STABLE"),
                state_data.get("confidence", 0.95),
                json.dumps(state_data)
            ))
            conn.commit()

    def get_latest_glacier_summary(self) -> List[Dict]:
        """导出当前最新的全冰川状态清单"""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            rows = cursor.execute("""
            SELECT i.glacier_id, i.name, i.baseline_area_km2, i.debris_fraction,
                   h.observation_date, h.velocity_m_yr, h.velocity_z_score, h.displacement_los_mm, h.stability_status
            FROM glacier_inventory i
            LEFT JOIN (
                SELECT glacier_id, MAX(observation_date) as max_date, velocity_m_yr, velocity_z_score, displacement_los_mm, stability_status
                FROM glacier_state_history
                GROUP BY glacier_id
            ) h ON i.glacier_id = h.glacier_id
            """).fetchall()
            return [dict(r) for r in rows]