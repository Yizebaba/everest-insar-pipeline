# 珠峰 / Everest 监控与异常分析系统 · 核心架构与多源演进规范

> **规范版本**：v4.0.0 (L0~L4 五层工业级架构)  
> **核心原则**：Detection ≠ Warning（检测到异常 ≠ 灾害预警），原始数据 ≠ 模型输入

---

## 一、完整系统架构总图

```text
                         珠峰 / Everest
                              │
                              │
              ┌───────────────┼────────────────┐
              │               │                │
              ▼               ▼                ▼
        Sentinel-1        Sentinel-2          DEM
        SAR数据            光学数据          地形数据
              │               │                │
              │               │                │
              │               ▼                │
              │          ┌───────────┐         │
              │          │  GlaViTU  │◄────────┘
              │          │ 冰川分割模型 │
              │          └─────┬─────┘
              │                │
              │                ▼
              │        Glacier Mask
              │        冰川范围/边界
              │                +
              │        Confidence
              │        分割置信度
              │
              ▼
        ┌───────────────┐
        │ CC-ResSiamNet │
        │ SAR位移/速度模型 │
        └───────┬───────┘
                │
                ▼
          Displacement
          像素位移
                │
                ▼
        ┌───────────────┐
        │     TICOI     │
        │ 时序融合/反演/插值 │
        └───────┬───────┘
                │
                ▼
      Glacier Velocity Time Series
             冰川速度时间序列
                │
                ├── 速度
                ├── 加速度
                ├── 趋势
                ├── 时间连续性
                └── 异常程度
                │
                ▼
       ┌────────────────────┐
       │ Velocity Anomaly   │
       │     速度异常检测    │
       └─────────┬──────────┘
                 │
        ┌────────┴─────────┐
        │                  │
        ▼                  ▼
 ┌──────────────┐    ┌────────────────┐
 │  AnyChange   │    │  InSAR + SAM   │
 │ 双时相变化检测 │    │ 形变区域提取    │
 └──────┬───────┘    └───────┬────────┘
        │                    │
        ▼                    ▼
 Surface Change         Deformation
 地表变化                地表形变
        │                    │
        └─────────┬──────────┘
                  │
                  ▼
        ┌──────────────────────┐
        │  多源遥感特征融合     │
        │ Remote Sensing       │
        │ Feature Fusion       │
        └──────────┬───────────┘
                   │
       ┌───────────┼────────────┐
       │           │            │
       ▼           ▼            ▼
Copernicus-FM   RobSense     Weather
多模态遥感       S1+S2融合     天气/气象
特征编码         特征编码       特征
       │           │            │
       └───────────┼────────────┘
                   │
                   ▼
               Seismic
                地震数据
                   │
                   ▼
        ┌──────────────────────┐
        │ Everest Anomaly      │
        │       Engine         │
        │ 珠峰多源异常分析引擎  │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ 持续性 Persistence    │
        │ 空间一致性 Spatial    │
        │ Consistency           │
        │ 多源交叉验证          │
        │ Cross-source         │
        │ Validation            │
        │ Confidence 置信度      │
        │ Uncertainty 不确定性  │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │   Anomaly / Event    │
        │   异常 / 潜在事件     │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ 人工确认 / Human      │
        │ Verification         │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │      Alert           │
        │      告警             │
        └──────────────────────┘
```

---

## 二、每个位置的明确职责与数据流向

### 【L0 数据层】

1. **Sentinel-1**
   - **类型**：SAR 遥感数据（穿透云雾、全天候全天时）。
   - **主要作用**：冰川位移/速度、SAR 变化检测、InSAR 形变、RTC 后向散射变化。
   - **特别纠正**：原始 Sentinel-1 数据 ≠ 模型输入。必须经过 SLC/SAR 影像对选取、RTC 辐射地形校正、精细配准后，才生成模型输入数据。
2. **Sentinel-2**
   - **类型**：光学多光谱数据。
   - **主要作用**：冰川范围、冰雪覆盖、冰湖演变、泥石流/崩塌地表痕迹。
   - **核心光学输入**：Blue、Green、Red、NIR、SWIR1、SWIR2。
3. **DEM（数字高程模型）**
   - **类型**：地形数据（Copernicus 30m DEM / GLO-30）。
   - **核心物理特征**：Elevation（高程）、Slope（坡度）、Aspect（坡向）、Curvature（曲率）、Relief（起伏度）。
   - **特别纠正**：DEM 绝不仅在系统末端使用：
     - **第一用途**：向 GlaViTU 输入 Elevation + Slope，直接作为冰川空间分割的基础特征；
     - **第二用途**：作为灾害物理特征与雷达几何畸变掩膜（过滤坡度 $>35^\circ$ 的假形变）。

---

### 【L1 遥感观测层】

4. **GlaViTU（冰川多模态分割基座）**
   - **发表顶会/期刊**：**IEEE IGARSS 2023**（arXiv:2401.15113）
   - **论文标题**：*Globally Scalable Glacier Mapping by Deep Learning Matches Expert Delineation Accuracy*
   - **核心架构**：混合 ResNet + Vision Transformer (ViT) + U-Net 架构。
   - **输入**：Sentinel-2 六波段（B2, B3, B4, B8, B11, B12） + DEM 高程 + DEM 坡度。
   - **输出**：`Glacier Mask`（冰川范围/边界） + `Confidence`（分割置信度）。
   - **回答问题**：“哪里是冰川？”（空间范围底座，非最终预警模型）。
   - **开源代码地址**：
     - 主仓：[https://github.com/Sarv8400/glaciermappingalgorithm](https://github.com/Sarv8400/glaciermappingalgorithm)
     - 论文复现仓：[https://github.com/konstantin-a-maslov/GlaViTU-IGARSS2023](https://github.com/konstantin-a-maslov/GlaViTU-IGARSS2023)
5. **CC-ResSiamNet（SAR 孪生残差位移模型）**
   - **研制方向**：雷达遥感与冰川流速 Offset Tracking 顶刊研究（Cross-Correlation Residual Siamese Network）
   - **输入**：不同时间的 SAR 影像对（经 RTC 与亚像素配准）。
   - **输出**：`Displacement / Offset`（像素级位移场）。
   - **回答问题**：“冰川表面移动了多少？”
   - **开源代码地址**：[https://github.com/udayDarbar/CC_ResSiamNet-26](https://github.com/udayDarbar/CC_ResSiamNet-26)
6. **AnyChange（双时相零样本遥感变化检测模型）**
   - **发表顶会**：**NeurIPS 2024 (全球人工智能顶级会议)**（arXiv:2402.01188）
   - **论文标题**：*Segment Any Change*
   - **核心架构**：基于 Meta SAM 打造的双时相潜在空间匹配（Bitemporal Latent Matching），无需标注即可零样本泛化。
   - **输入**：不同时间的遥感影像对（Sentinel-2 / Sentinel-1 / 高分影像）。
   - **输出**：`Surface Change`（地表变化区域多边形）。
   - **特别纠正**：不是速度异常的后处理，而是独立的遥感证据源，用于发现冰湖溃决、岩石崩塌、泥石流痕迹、新雪冰异常覆盖。
   - **开源代码地址**：[https://github.com/Z-Zheng/pytorch-change-models](https://github.com/Z-Zheng/pytorch-change-models)
7. **InSAR + SAM（形变提取与智能勾勒）**
   - **技术方案**：利用 InSAR 相干性骤降或解缠相位突变梯度作为 Prompt（提示框），驱动 SAM 自动勾勒闭合边界。
   - **流程**：`Sentinel-1` ➔ `InSAR 时间序列` ➔ `形变/速度图` ➔ `Deformation Prompt` ➔ `SAM` ➔ `Deformation Region`。
   - **输出**：`Deformation`（精准闭合的地表形变矢量区域）。
   - **回答问题**：“哪里出现了可观测的地表微小形变？”（与冰川大流速指标彻底解耦）。
   - **官方开源基座**：
     - SAM 官方基座：[https://github.com/facebookresearch/segment-anything](https://github.com/facebookresearch/segment-anything)
     - InSAR 时序解算基座：[https://github.com/insarlab/MintPy](https://github.com/insarlab/MintPy)

---

### 【L2 时序 / 物理层】

8. **TICOI（多时相时序融合与插值）**
   - **发表期刊**：**EGUsphere / Geoscientific Model Development (GMD 2024-2025)**（DOI: 10.5194/egusphere-2024-3409）
   - **论文标题**：*TICOI: an operational Python package to generate regularized glacier velocity time series*
   - **核心原理**：基于时间闭合环约束（Temporal Inversion with Closure of Observations），将离散多时相速度正则化平滑。
   - **定位**：通用时序反演闭合算法，不是单一算法的专用后处理。
   - **输入**：CC-ResSiamNet 位移、autoRIFT 速度、外部流速数据（NASA ITS_LIVE 等）。
   - **输出**：`Regular Glacier Velocity Time Series`（时间连续性规则化速度时间序列）。
   - **开源代码与安装**：
     - GitHub 主仓：[https://github.com/ticoi/ticoi](https://github.com/ticoi/ticoi)
     - Conda-forge 安装：`conda install -c conda-forge ticoi`
9. **Glacier Velocity Time Series（冰川动力学时序指标）**
   - 不仅是单一速度数字，全面度量：
     - **Velocity**（速度）
     - **Acceleration**（加速度）
     - **Direction Change**（流动方向变化）
     - **Spatial Gradient**（空间应变剪切梯度）
     - **Temporal Trend**（长期演变趋势）
     - **Persistence**（持续性）
     - **Historical Baseline**（多年历史同季节基线）
10. **Velocity Anomaly（速度异常检测层）**
    - 评估当前运动是否明显偏离历史基线（过去 30 天平均 ➔ 过去 7 天 ➔ 当前 ➔ 变化率/加速度）。
    - 警示：“速度异常” 不等于 “灾害发生”。

---

### 【L3 多模态特征层】

11. **多源遥感特征融合（Feature Fusion）**
    - 汇总 Glacier Mask、Confidence、Velocity、Acceleration、Surface Change、Deformation、SAR/光学/DEM 物理量，投影到统一特征空间。
12. **Copernicus-FM（欧空局哥白尼多模态遥感大模型）**
    - **发表成果**：德国宇航中心 (DLR) & 慕尼黑工大 (TUM) 打造（arXiv:2503.11849）
    - **论文标题**：*Towards a Unified Copernicus Foundation Model for Earth Vision*
    - **开源代码地址**：[https://github.com/zhu-xlab/Copernicus-FM](https://github.com/zhu-xlab/Copernicus-FM)
    - **定位**：统一对 S1 SAR、S2 多光谱、DEM 地形进行底层特征编码的高级 Feature Encoder，非最终灾害判断器。
13. **RobSense（复杂环境多模态鲁棒遥感感知大模型）**
    - **发表顶会**：**CVPR 2025 (计算机视觉顶级会议)**（DOI: 10.1109/cvpr52734.2025.00696）
    - **论文标题**：*RobSense: A Robust Multi-modal Foundation Model for Remote Sensing with Static, Temporal, and Incomplete Data Adaptability*
    - **定位**：专门应对恶劣云雾、雨雪遮挡、传感器缺失等不完整多模态遥感数据的鲁棒特征提取与跨模态对齐。
14. **Weather（精细化外部气象特征）**
    - 必须细化拆分为：`Temperature`（温度）、`Precipitation`（降水）、`Snow`（降雪）、`Wind`（风速）、`Gust`（阵风）、`Humidity`（湿度）、`Pressure`（气压）、`Freezing Level`（冻融高度/0度层）、`Snowline`（雪线）。
    - 重点驱动：**降水 + 温度 + 冻融 + 风 + 雪线**。
15. **Seismic（地震动特征）**
    - 特征化指标：`Earthquake Event`（事件）、`Magnitude`（震级）、`Depth`（震源深度）、`Distance`（震中距）、`Frequency`（余震频度）、`Event Density`（震群密度）。

---

### 【L4 Everest Anomaly Engine（珠峰多源异常分析引擎）】

16. **综合分析引擎核心**：严禁采用 “AI 跑出一个数 ➔ 盲目报警” 的做法，必须融合多维分析：
    - **空间分析（Spatial Analysis）**：热点分析（Hotspot）、聚类（Clustering）、边界接触度、地形临近度（Proximity）；
    - **时间分析（Temporal Analysis）**：持续性（Persistence，排除单次噪声）、加速度（Acceleration）、趋势演变、再现性；
    - **多源交叉验证（Cross-source Validation）**：S1 + S2 + DEM + Weather + Seismic 互相印证。
17. **Confidence（置信度）与 Uncertainty（不确定性）并列输出**：
    - 不确定性来源明确标定：云覆盖、雷达失相干、时间间隔脱节、多源证据冲突等。
18. **Anomaly / Event Candidate（候选事件生成）**：
    - 严守措辞边界：“检测到持续性冰川运动异常，存在进一步关注必要”，不直接定性灾害。
19. **Human Verification（人工复核与交互）**：
    - 向业务/科研专家完整展示前后卫星切片、InSAR 相位、速度曲线、气象与坡度分布。
20. **Alert（终极告警）**：
    - 人工确认后通过系统正式下发告警（微信服务号模板消息推送 / Windy 地图图层标注）。

---

## 三、五层工业级架构映射定义

| 层级 | 架构层名称 | 核心模块与技术栈 | 对应仓库/代码落地 |
| :--- | :--- | :--- | :--- |
| **L0** | **数据层 (Data)** | Sentinel-1, Sentinel-2, Copernicus DEM 30m, Weather, Seismic | CDSE STAC / NASA GIBS / USGS / ECMWF |
| **L1** | **遥感观测层 (Observation)** | GlaViTU (冰川分割), CC-ResSiamNet (SAR位移), AnyChange (变化检测), InSAR+SAM (形变勾勒) | AI 推理模型服务 / openEO UDP |
| **L2** | **时序/物理层 (Time-Series)** | TICOI (闭合平差融合), Velocity, Acceleration, Deformation, Persistence | `everest-insar-pipeline` / TICOI 库 |
| **L3** | **多模态特征层 (Features)** | Copernicus-FM, RobSense, SAR/光学/地形/气象/地震高级特征向量 | 特征工程库 / 多模态 Encoder |
| **L4** | **异常分析与决策层 (Engine)** | Everest Anomaly Engine, 空间聚类, 多源校验, 人工确认, 告警输出 | `D:\Zhufenjianche` / `Everest-realtime` / Windy |

---

## 四、十三条绝对保持的架构准则

1. `GlaViTU` = “哪里是冰川”（空间范围基础，非预警模型）；
2. `CC-ResSiamNet` = “冰川移动了多少”（像素偏移量量测）；
3. `TICOI` = “把多时相离散运动结果拟合成规则连续时间序列”；
4. `Velocity Anomaly` = “运动是否显著偏离自身历史状态”；
5. `AnyChange` = “哪里发生了独立地表与冰湖变化”；
6. `InSAR + SAM` = “哪里发生了毫米级地表形变并提取精准边界”；
7. `Copernicus-FM / RobSense` = “提取多模态遥感高级特征表示”；
8. `DEM` = “地形底座 + GlaViTU 输入特征 + 灾害物理特征 + 雷达几何掩膜”；
9. `Weather` = “降水、温度、冻融、风速、雪线等外部气象证据”；
10. `Seismic` = “震级、震源深度、震中距等外部地震动物理扰动”；
11. `Everest Anomaly Engine` = “时空一致性与多源证据综合研判”；
12. `Human Verification` = “人工确认层，防范模型假阳性”；
13. **最高法则**：
    $$\text{Detection} \neq \text{Warning}$$
    （检测到异常 $\neq$ 灾害预警。必须经持续性、空间一致性、多源验证、置信度评估及人工确认后，才准生成最终 Alert。）

---

## 五、顶会顶刊 AI 模型与权威云底座全量开源索引表

### 1. 顶会/顶刊 AI 模型与时序工具全量索引

| 模型/工具 | 发表期刊/会议 | 论文标题 / 文献索引 | 核心功能定位 | 官方开源仓库 / 包管理 |
| :--- | :--- | :--- | :--- | :--- |
| **GlaViTU** | **IEEE IGARSS 2023** | *Globally Scalable Glacier Mapping by Deep Learning Matches Expert Delineation Accuracy* (arXiv:2401.15113) | 混合 ResNet+ViT+U-Net 的冰川多模态分割基座 (S2 六波段 + DEM 高程坡度) | 🔗 [Sarv8400/glaciermappingalgorithm](https://github.com/Sarv8400/glaciermappingalgorithm)<br>🔗 [maslov/GlaViTU-IGARSS2023](https://github.com/konstantin-a-maslov/GlaViTU-IGARSS2023) |
| **CC-ResSiamNet** | **遥感顶刊专题** | *Cross-Correlation Residual Siamese Network for Glacier Surface Velocity Estimation* | 基于双分支残差孪生网络的 SAR 冰川表面亚像素级位移/速度特征匹配 | 🔗 [udayDarbar/CC_ResSiamNet-26](https://github.com/udayDarbar/CC_ResSiamNet-26) |
| **TICOI** | **EGUsphere / GMD 2025** | *TICOI: an operational Python package to generate regularized glacier velocity time series* (DOI: 10.5194/egusphere-2024-3409) | 基于时间闭合环约束（Closure of Observations）的多时相冰川流速正则化时序反演与插值 | 🔗 [ticoi/ticoi](https://github.com/ticoi/ticoi)<br>📦 `conda install -c conda-forge ticoi` |
| **AnyChange** | **NeurIPS 2024 (顶级AI大会)** | *Segment Any Change* (arXiv:2402.01188) | 基于 Meta SAM 的零样本双时相遥感变化检测基座模型（用于冰湖溃决、岩崩、泥石流地表突变识别） | 🔗 [Z-Zheng/pytorch-change-models](https://github.com/Z-Zheng/pytorch-change-models) |
| **InSAR + SAM** | **前沿遥感范式** | *Deformation extraction via InSAR gradient prompting Segment Anything Model* | 利用 InSAR 相干性骤降或解缠相位突变梯度作为 Prompt 提示驱动 SAM 自动勾勒毫米级形变区边界 | 🔗 [facebook/segment-anything](https://github.com/facebookresearch/segment-anything)<br>🔗 [insarlab/MintPy (InSAR解算基座)](https://github.com/insarlab/MintPy) |
| **Copernicus-FM** | **遥感大模型成果 (2025)** | *Towards a Unified Copernicus Foundation Model for Earth Vision* (arXiv:2503.11849) | 德国宇航中心(DLR)与慕尼黑工大打造的欧空局哥白尼统一多模态遥感大模型 Feature Encoder | 🔗 [zhu-xlab/Copernicus-FM](https://github.com/zhu-xlab/Copernicus-FM) |
| **RobSense** | **IEEE/CVF CVPR 2025** | *RobSense: A Robust Multi-modal Foundation Model for Remote Sensing with Static, Temporal, and Incomplete Data Adaptability* (DOI: 10.1109/cvpr52734.2025.00696) | 专为高山多云雾、遮挡等不完整多模态遥感数据设计的跨传感器鲁棒特征提取大模型 | 🔗 IEEE CVPR 官方 DOI 与公开数据集评测规范 |

### 2. 国际卫星云平台与官方数据源分发入口

| 数据源 / 平台 | 平台性质与核心能力 | 官方平台直达入口 | 接入方式 / API |
| :--- | :--- | :--- | :--- |
| **Sentinel-1** | 欧空局合成孔径雷达（C-band SAR，全天候穿透云层） | 🔗 [ESA Sentinel-1 官方任务入口](https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-1) | SLC 干涉对 / GRD 强度 |
| **Sentinel-2** | 欧空局多光谱光学卫星（10-60m 分辨率，13个波段） | 🔗 [ESA Sentinel-2 官方任务入口](https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-2) | L2A 地表反射率 / SCL 场景分类 |
| **CDSE** | 欧空局哥白尼数据空间生态系统（欧洲官方数据总底座） | 🔗 [https://dataspace.copernicus.eu/](https://dataspace.copernicus.eu/) | OData / STAC API、S3 直存与云端 JupyterHub 容器 |
| **Copernicus Browser** | CDSE 官方交互式遥感在线可视化浏览器（原 EO Browser） | 🔗 [https://browser.dataspace.copernicus.eu/](https://browser.dataspace.copernicus.eu/) | 在线交互检索、AOI 对比、真假彩色渲染 |
| **NASA Earthdata** | NASA 地球科学数据中心与统一认证通行证（Earthdata Login） | 🔗 [https://www.earthdata.nasa.gov/](https://www.earthdata.nasa.gov/) | 全球公开地球物理遥感产品与 ASF DAAC 接入 |
| **NASA Worldview** | NASA 官方全功能近实时全球卫星底图可视化大屏 | 🔗 [https://worldview.earthdata.nasa.gov/](https://worldview.earthdata.nasa.gov/) | 每日全球 MODIS/VIIRS 遥感、积雪、火点交互回溯 |
| **NASA GIBS** | NASA 全球影像浏览服务（全球标准切片瓦片流 API） | 🔗 [NASA GIBS 开发者规范文档](https://nasa-gibs.github.io/gibs-api-docs/) | WMTS 瓦片流（Windy 插件底图数据直接源于此） |
| **WEkEO** | 欧盟哥白尼 DIAS 四大官方云平台之一（海洋/海冰/大气/高山算力） | 🔗 [https://www.wekeo.eu/](https://www.wekeo.eu/) | 联合 EUMETSAT 与 ECMWF 搭建的统一数据访问 (HDA) 平台 |

