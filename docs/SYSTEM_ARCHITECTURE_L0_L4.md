# 珠峰 / Everest 监控与异常分析系统 · 核心架构与多源演进规范 (v5.0 终极版)

> **系统版本**：v5.0.0 (全源异构多模态物理约束架构)  
> **最高准则**：Detection ≠ Warning（检测到异常 ≠ 灾害预警，未经物理约束与人工复核绝不报警）

---

## 一、完整系统架构总图

```text
                              Everest                                
                                │
        =================================================
        │                       │                       │
        ▼                       ▼                       ▼

   Sentinel-1              Sentinel-2                DEM
   SAR                     Optical                   Terrain

        │                       │                       │
        │                       │                       │
        ▼                       ▼                       ▼

 SAR Feature             Optical Feature          Terrain Feature
 - Backscatter           - RGB                    - Elevation
 - Coherence             - NIR                    - Slope
 - Phase                 - SWIR                   - Aspect
 - Texture               - NDVI/NDSI              - Curvature
                         - Snow Index             - Glacier Basin

        │                       │                       │
        │                       │                       │
        =========================                       │
                    │                                   │
                    ▼                                   │
        =================================               │
        │                              │                │
        ▼                              ▼                │
 Glacier Motion                  Glacier Mapping        │
 冰川运动                         冰川范围              │
        │                              │                │
        ▼                              ▼                │
 ITS_LIVE                         GlaViTU               │
 autoRIFT                         GlacierNet            │
 CC-ResSiamNet                    DeepLab/U-Net         │
        │                              │                │
        ▼                              ▼                │
 Glacier Velocity                 Glacier Mask          │
 Time Series                      Glacier Boundary      │
        │                              │                │
        ▼                              │                │
 Velocity Anomaly                  Glacier Change       │
 Detection                         Detection            │
        │                              │                │
        │                              │                │
        =================================                │
                         │                              │
                         ▼                              ▼
              Glacier State Database  <-----------------
              冰川状态数据库

============================================================

              Sentinel-1 SAR变化模块
                    │
                    ▼
                  InSAR
                    │
                    ▼
             Deformation Map
                    │
                    ▼
          Deformation Detection
                    │
                    ▼
        ┌─────────────────────┐
        │  Glacier Stability  │
        │  冰川稳定性分析      │
        └─────────────────────┘

============================================================

              Sentinel-2变化模块
                    │
                    ▼
              AnyChange
              ChangeFormer
              SAMGeo
                    │
                    ▼
              Surface Change
                    │
        -------------------------
        │                       │
        ▼                       ▼
  Crevasse Detection       Ice Surface Change
  冰裂缝检测               冰面变化
                    │
                    ▼
             Glacier Hazard Feature

============================================================

             Sentinel-2 + SAR
                    │
                    ▼
            Lake Detection
                    │
                    ▼
              GLOF Module
                    │
                    ▼
          Glacier Lake Risk

============================================================

             Sentinel-2 + SAR + DEM
                    │
                    ▼
          Avalanche / Icefall Module
                    │
                    ▼
        Snow/Ice Collapse Feature

============================================================

                 DEM Terrain Layer
                     │
       --------------------------------
       │              │               │
       ▼              ▼               ▼
    Slope        Elevation       Aspect
       │              │               │
       --------------------------------
                     │
                     ▼
          Physical Constraint Layer
          物理约束层
          (判断: 陡坡/冰川末端/高风险区/冰崩物理条件)

============================================================

                 外部环境数据
        Weather                 Seismic
          │                       │
          ▼                       ▼
 Temperature              Earthquake Event
 Snow                     Vibration
 Rain                     Magnitude
 Wind                     Distance

============================================================
                      │
                      ▼
        Remote Sensing Foundation Model
        遥感基础大模型层
        - Copernicus-FM
        - RobSense
        - Prithvi (NASA/IBM)
                      │
                      ▼
              Multi-modal Feature Fusion
              多模态特征融合
                      │
                      ▼
              Everest Anomaly Engine
              珠峰多源异常分析引擎
                      │
                      ▼
        =================================
        Persistence 持续性
        Spatial Consistency 空间一致性
        Cross Validation 多源验证
        Physics Constraint 物理约束
        Confidence 置信度
        Uncertainty 不确定性
        =================================
                      │
                      ▼
              Event Candidate 潜在事件
                      │
                      ▼
              Human Review 人工复核
                      │
                      ▼
                  Alert 最终告警
```

---

## 二、各大模块技术标准与物理职责说明

### 1. 数据与基础特征层 (L0 Data & Features)
- **Sentinel-1 SAR Feature**：提取 Gamma0 后向散射强度 (Backscatter)、干涉相干性 (Coherence)、差分相位 (Phase) 与纹理特征 (Texture)。
- **Sentinel-2 Optical Feature**：提取真彩色 (RGB)、近红外 (NIR)、短波红外 (SWIR)、NDVI植被/水体指数、NDSI积雪冰川指数。
- **DEM Terrain Feature**：提取高程 (Elevation)、坡度 (Slope)、坡向 (Aspect)、剖面曲率 (Curvature) 与冰川流域盆地 (Glacier Basin)。

### 2. 冰川状态数据库 (Glacier State Database)
- **冰川运动 (Glacier Motion)**：利用 NASA ITS_LIVE、autoRIFT 及 CC-ResSiamNet 输出规则化冰川流速时间序列，对比历史基线检测速度异常。
- **冰川范围制图 (Glacier Mapping)**：利用 GlaViTU、GlacierNet 等前沿网络输出 Glacier Mask 与边界，监测消融后退变化。
- **数据库作用**：作为珠峰冰川的长期档案库，沉淀时空基线。

### 3. 五大平行专项灾害观测管道
1. **S1 InSAR 形变管道**：通过相位差分与相干性反演，输出 `Deformation Map`，评估冰川地表整体稳定性 (`Glacier Stability`)。
2. **S2 地表变化管道 (AnyChange/ChangeFormer/SAMGeo)**：双时相检测冰面破裂、冰裂缝群扩张 (`Crevasse Detection`) 与崩滑痕迹。
3. **S2 + SAR 冰湖溃决管道 (GLOF Module)**：水体指数结合雷达穿透，动态监测冰湖水面暴涨、冰坝溃决风险 (`Glacier Lake Risk`)。
4. **S2 + SAR + DEM 雪崩/冰崩管道 (Avalanche/Icefall Module)**：多源结合捕捉雪崩、高位冰崩堆积体与崩塌前兆。
5. **DEM 物理约束层 (Physical Constraint Layer)**：
   - 审查是否处于崩塌临界坡度（$30^\circ \sim 50^\circ$）；
   - 审查是否在冰川终碛垄与末端活跃消融区；
   - 审查是否满足重力驱动的物理条件，强力过滤虚假误报。

### 4. 外部物理环境与基座大模型
- **外部环境驱动**：引入温度（冻融0度层）、降雨、降雪、风速及地震动（震级、震源深度、震中距）作为外部能量触发源。
- **遥感大模型表征**：
  - **Copernicus-FM**：欧空局哥白尼多模态特征编码大模型；
  - **RobSense**：针对云雾遮挡的鲁棒对齐大模型；
  - **Prithvi**：NASA 与 IBM 联合打造的 100M 地球科学基础时空模型。

### 5. Everest Anomaly Engine (综合判定决策引擎)
严格执行六大判定准则：
- **持续性 (Persistence)**：多周期连续存在，剔除单景随机噪声；
- **空间一致性 (Spatial Consistency)**：异常聚集于同一坡面或冰川运动通道；
- **多源验证 (Cross Validation)**：雷达形变 + 光学变化 + 气象触发多方印证；
- **物理约束 (Physics Constraint)**：地形坡度与重力条件必须物理成立；
- **置信度 (Confidence) 与 不确定性 (Uncertainty)** 并列输出；
- **人机协同 (Human Review)**：终极告警前必须经专家在可视化大屏/Windy界面人工确认。

---

## 三、顶会顶刊开源模型与权威服务全量索引

| 模型/工具 | 发表期刊/会议 | 核心功能 | 官方开源代码 / 访问入口 |
| :--- | :--- | :--- | :--- |
| **GlaViTU** | **IEEE IGARSS 2023** | 冰川多模态分割基座 (S2+DEM) | [Sarv8400/glaciermappingalgorithm](https://github.com/Sarv8400/glaciermappingalgorithm) |
| **CC-ResSiamNet** | **遥感顶刊专题** | SAR 冰川表面亚像素位移匹配 | [udayDarbar/CC_ResSiamNet-26](https://github.com/udayDarbar/CC_ResSiamNet-26) |
| **TICOI** | **EGUsphere / GMD 2025** | 时间闭合环时序速度正则化融合 | [ticoi/ticoi](https://github.com/ticoi/ticoi) |
| **AnyChange** | **NeurIPS 2024** | 零样本双时相遥感地表突变检测 | [Z-Zheng/pytorch-change-models](https://github.com/Z-Zheng/pytorch-change-models) |
| **InSAR + SAM** | **前沿遥感范式** | 相位/相干性梯度 Prompt 驱动 SAM | [facebook/segment-anything](https://github.com/facebookresearch/segment-anything) + [MintPy](https://github.com/insarlab/MintPy) |
| **Prithvi** | **NASA / IBM 2023** | 地球科学遥感时空基础大模型 | [NASA-IMPACT/hls-foundation-os](https://github.com/NASA-IMPACT/hls-foundation-os) |
| **Copernicus-FM** | **DLR / TUM 2025** | 哥白尼多模态统一遥感基座 | [zhu-xlab/Copernicus-FM](https://github.com/zhu-xlab/Copernicus-FM) |
| **RobSense** | **IEEE/CVF CVPR 2025** | 恶劣高山遮挡多模态鲁棒大模型 | 官方 DOI: 10.1109/cvpr52734.2025.00696 |
| **ITS_LIVE** | **NASA MEaSUREs** | 全球现成冰川流速与历史基准 | [https://nsidc.org/data/measures/its_live](https://nsidc.org/data/measures/its_live) |
