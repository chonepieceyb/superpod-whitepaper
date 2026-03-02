# 超长序列技术

超长序列（Long-Context）技术正在把模型的有效上下文窗口从数千 token 推向数十万乃至百万级，这对超节点的内存容量、带宽层次与通信拓扑提出了全新的约束。Attention 机制的计算量与 KV Cache 的内存占用随序列长度超线性增长，使得"序列长度"成为与"模型参数量"并列的第二个规模轴，深刻改变了并行策略与硬件配比的设计空间。

面向超节点架构，超长序列技术的影响需要从以下维度考察：

- **内存与带宽的双重约束**：百万级 token 的 KV Cache 可轻松消耗数百 GB 显存，迫使系统在 HBM 容量、分层缓存（HBM → DDR → SSD）以及跨节点内存池化之间做取舍。同时，Attention 计算的带宽需求使得 HBM 带宽成为更严苛的瓶颈——这要求超节点在 HBM 代际选型（HBM3 → HBM3E → HBM4）与互联带宽之间保持匹配。
- **加速策略与并行切分**：分块注意力（FlashAttention/Ring Attention）、滑窗注意力、稀疏注意力等技术各自在"计算量 vs 精度 vs 通信量"上做出不同权衡。序列并行（Sequence Parallelism）与 Context Parallelism 需要跨卡/跨节点传输 KV 分片，直接依赖 Scale-Up 域的带宽与延迟特性。
- **KV Cache 管理与调度**：PagedAttention 等分页管理技术解决了 KV Cache 的碎片化问题，但引入了更复杂的内存分配/回收/迁移语义。在超长序列场景下，KV Cache 的放置策略（本地 vs 远端、常驻 vs 可换出）与请求调度（Prefill/Decode 分离、投机解码）深度耦合，需要系统软件提供更细粒度的控制面。

待补充：

- [ ] 代表性长序列模型的硬件配比需求分析。
- [ ] Ring Attention 与 Context Parallelism 在不同拓扑下的通信开销对比。
- [ ] KV Cache 分层管理的工程实践与性能数据。
