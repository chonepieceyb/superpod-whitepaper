# 华为超节点产品分析

## 产品概述

华为是国内超节点领域的领军企业。从 2020 年昇腾 910 集群训练到 2024 年 CloudMatrix 384 发布，华为走出了一条"以规模换带宽、以自研协议构建护城河"的差异化路径。CloudMatrix 384 标称提供 **300 PFLOPs FP16 算力**，Scale-Up 域规模达到 384 颗 NPU，是当前公开可查的最大规模商用超节点之一。

## CloudMatrix 产品系列

### CloudMatrix 384（CM384）

CloudMatrix 384 是华为于 2024 年发布的旗舰超节点产品，采用昇腾 910C NPU 与自研 UB 灵衢互联协议：

| 参数 | CloudMatrix 384 | 对比 GB200 NVL72 |
|:-----|:----------------|:-----------------|
| **计算芯片** | 昇腾 910C × 384 | GB200 (双 Die) × 36 (72 GPU) |
| **FP16 算力** | ~300 PFLOPs (标称) | 180 PFLOPs |
| **HBM 配置** | HBM2e，单卡 64 GB | HBM3e，单卡 192 GB × 2 |
| **HBM 总容量** | 384 × 64 GB = 24.6 TB | 72 × 192 GB = 13.8 TB |
| **Scale-Up 互联** | UB 灵衢 + HCCS | NVLink + NVSwitch |
| **单 NPU Scale-Up 带宽** | ~400 GB/s | 1800 GB/s |
| **Scale-Up 域规模** | 384 NPU | 72 GPU |
| **Scale-Out 网络** | RoCE | IB/RoCE |
| **机柜形态** | 多柜互联（含光互联） | 单柜 72 卡 |

### 代际演进

| 产品 | 芯片 | Scale-Up 规模 | 互联协议 | 发布时间 |
|:-----|:-----|:-------------|:---------|:---------|
| Atlas 800（910A 集群） | 昇腾 910A | 8 卡/节点 | HCCS v1 | 2020 |
| Atlas 800T A2 | 昇腾 910B | 8 卡/节点 | HCCS v2 | 2023 |
| CloudMatrix 384 | 昇腾 910C | 384 NPU | UB 灵衢 1.0 | 2024 |
| CloudMatrix（下一代） | 昇腾 920 (预期) | 万卡级 | UB 灵衢 2.0 | 2025+ |

## 技术架构分析

### 昇腾 NPU 架构

华为昇腾系列 NPU 基于自研 Da Vinci 架构，核心计算单元为 AI Core（矩阵计算单元 Cube + 向量计算单元 Vector）。当前主力训练芯片为昇腾 910B/910C：

- **昇腾 910B**：7nm 工艺，320 TOPS INT8，HBM2e 64 GB，TDP 310W
- **昇腾 910C**：工艺升级版，FP16 算力提升至约 780 TFLOPS，HBM 容量/带宽提升
- **Da Vinci 3.0 架构**：增强 Cube Unit 算力密度，支持 FP8/FP16/BF16 混合精度

### 互联技术：HCCS → UB 灵衢

华为的超节点互联经历了从 HCCS 到 UB 灵衢的关键跃迁：

| 层级 | 技术方案 | 技术细节 |
|:-----|:---------|:---------|
| D2D 互联 | HCCS (Huawei Cache Coherent System) | 华为自研缓存一致性互联，单链路 56 GB/s，支持 MOESI 协议 |
| 节点内 Scale-Up | UB 灵衢 | 总线级互联，支持内存语义 + 消息语义，单跳 150–200 ns |
| 跨柜光互联 | UB 灵衢 + 光模块 | 支持 >200 m 距离，带宽衰减 <3% |
| Scale-Out | RoCE v2 | 基于以太网的 RDMA |

**UB 灵衢的核心设计理念**是"总线级互联"——与 NVLink 强调点对点高带宽不同，UB 灵衢更强调**全局一致性**与**全量池化**：所有 NPU 共享统一地址空间，任意 NPU 可等效访问任意远端显存，强调"无 NUMA 差异"的平坦架构。这种设计在 384 卡规模上实现了全域可达，但单链路带宽仍低于 NVLink。

### 软件生态

| 层次 | 华为方案 | 对标 NVIDIA |
|:-----|:---------|:-----------|
| 编程框架 | CANN (Compute Architecture for Neural Networks) | CUDA |
| AI 框架 | MindSpore / PyTorch (CANN 后端) | PyTorch / JAX |
| 通信库 | HCCL (Huawei Collective Communication Library) | NCCL |
| 推理引擎 | MindIE | TensorRT |
| 集群管理 | CloudMatrix Manager | Fabric Manager |

CANN 生态正在加速追赶：PyTorch 2.x 已提供昇腾后端适配，主流大模型（LLaMA、DeepSeek、ChatGLM 等）已完成昇腾适配。但在编译器自动优化、算子库覆盖度与社区活跃度上，与 CUDA 生态仍有 3–5 年差距。

## 与 NVIDIA 的系统级对比

| 维度 | NVIDIA GB200 NVL72 | 华为 CloudMatrix 384 |
|:-----|:-------------------|:--------------------|
| **芯片架构** | GPU (CUDA Core + Tensor Core) | NPU (Da Vinci AI Core) |
| **单卡算力 (FP16)** | 2.25 PFLOPS × 2 (双 Die) | ~0.78 PFLOPS |
| **互联协议** | NVLink 5 (私有) | UB 灵衢 (私有) |
| **交换芯片** | NVSwitch Gen4 (72 端口) | UB Switch (规格未公开) |
| **单卡互联带宽** | 1800 GB/s 双向 | ~400 GB/s |
| **Scale-Up 规模** | 72 GPU | 384 NPU |
| **系统总算力** | 180 PFLOPS (FP16) | ~300 PFLOPS (FP16，标称) |
| **HBM 总容量** | 13.8 TB | 24.6 TB |
| **软件栈** | CUDA / NCCL / TensorRT | CANN / HCCL / MindIE |
| **生态成熟度** | 成熟 (15+ 年) | 快速发展 (5+ 年) |

**核心差异分析**：NVIDIA 以**单卡极致性能 + 高带宽互联**取胜（72 张高性能 GPU，每张 1.8 TB/s 互联），华为以**大规模节点数 + 全域池化**取胜（384 张 NPU，强调无 NUMA 差异的统一地址空间）。两种路径反映了不同的工程哲学——前者追求"密度效率"，后者追求"规模效率"。

## 差异化战略

1. **规模为王**：384 → 万卡级的 Scale-Up 规模路线图，通过 NPU 数量补偿单卡性能差距
2. **全栈自主**：从芯片（昇腾）、互联（UB 灵衢）、交换（UB Switch）到软件（CANN）的完全自研，供应链风险可控
3. **协议开放**：UB 灵衢 2.0 规范开放（2025 年 9 月），试图构建国产生态联盟
4. **光互联先发**：跨柜光互联支持 >200 m，为下一代超大规模超节点（万卡级单域）提前布局
5. **云端一体**：华为云提供 CloudMatrix as a Service，降低客户硬件适配门槛

