# 大学生创新创业训练计划项目申请书

## 一、 项目名称
**基于双线性注意力的药物智能预测系统**

## 二、 立项依据

### 1. 研究背景：现代药物研发的瓶颈与人工智能的破局

在21世纪的生命科学领域，新药研发被公认为一项极具挑战性的系统工程。根据塔夫茨药物开发研究中心（Tufts CSDD）的最新报告显示，开发一款成功上市的新药，平均周期长达 10-15 年，研发投入成本已飙升至 26 亿美元以上。这其中，药物发现阶段（Drug Discovery）作为源头，其效率直接决定了整个研发管线的成败。

传统的小分子药物研发遵循“锁-钥模型”（Lock and Key Model），即寻找能够与特定蛋白质靶点（Target）特异性结合的小分子配体（Ligand）。为了筛选出高活性的先导化合物，制药企业往往需要对数以百万计的化合物库进行高通量筛选（High-Throughput Screening, HTS）。然而，基于湿实验（Wet-lab）的 HTS 技术面临着三大难以逾越的障碍：
*   **成本高昂**：所需的试剂、耗材以及维护精密仪器设备的费用极其惊人。
*   **周期漫长**：完成一轮完整的化合物库筛选往往耗时数月，严重制约了研发迭代速度。
*   **假阳性率**：体外实验受环境因素干扰大，往往存在一定的误差。

在此背景下，计算机辅助药物设计（Computer-Aided Drug Design, CADD）技术应运而生。早期的 CADD 主要依赖于基于物理力学的分子对接（Molecular Docking）和基于数理统计的定量构效关系（QSAR）。虽然这些方法在一定程度上加速了筛选进程，但它们高度依赖于高质量的三维晶体结构数据（Crystal Structure）或需要大量人工设计的特征工程（Feature Engineering），泛化能力有限。

近年来，随着以深度学习（Deep Learning, DL）为代表的人工智能技术的爆发式增长，AI for Science（AI4S）范式正在重塑医药行业。深度神经网络凭借其强大的非线性特征提取能力，能够直接从原始的分子序列数据（如 SMILES 字符串）中自动学习出隐含的理化规律，为解决药物-靶点亲和力（Drug-Target Affinity, DTA）预测这一核心科学问题提供了全新的思路。本课题正是立足于这一前沿交叉领域，试图通过算法创新解决现有模型存在的精度不足与解释性差等痛点。

### 2. 研究意义：从“试错法”向“精准预测”的范式转变

本项目的实施具有重要的科学意义与实际应用价值，具体体现在以下三个维度：

**(1) 理论层面：探索生物分子间相互作用的深度表征机制**
目前的 DTA 预测研究多停留在对分子全局特征的简单映射上，往往忽略了局部子结构（Substructure）与蛋白模体（Motif）之间的关键相互作用。本项目引入**双线性注意力网络（Bilinear Attention Network, BAN）**，旨在从数学层面构建一种能够模拟生物化学中“原子-残基”二阶交互的计算模型。这种尝试不仅有助于提升预测精度，更为理解生物分子间的分子识别机制提供了新的计算视角，即通过注意力权重的分布来反推潜在的结合位点。

**(2) 技术层面：构建“筛选-安评”一体化的智能计算框架**
药物研发不仅要关注“有效性”（Efficacy），更要关注“安全性”（Safety）。临床上，大量的候选药物因不可预见的药物-药物相互作用（Drug-Drug Interaction, DDI）导致严重毒副作用而惨遭淘汰。本项目创新性地将 DTA 预测与 DDI 预警整合在同一个基于孪生网络（Siamese Network）的深度学习框架下，实现了模型权重的共享与多任务协同优化。这种一体化的设计思路，相当于在药物筛选的早期就引入了安全评估机制，能有效降低后续临床试验的失败风险。

**(3) 应用层面：推动国产化、本地化药物研发软件的自主可控**
当前主流的药物预测工具（如 SwissTargetPrediction, Schrödinger 等）多为国外商业软件或云端 SaaS 服务，存在价格昂贵、数据隐私无法保障等问题。在我国生物医药产业蓬勃发展、数据安全日益受到重视的今天，开发一款拥有自主知识产权、支持全本地化部署（On-Premise Deployment）、且具备良好交互体验的智能筛选软件，对于保障我国原创新药研发的数据安全、降低中小药企和科研院所的研发门槛具有重要的战略意义。

### 3. 国内外研究现状及分析

**(1) 基于机器学习的传统方法**
早期的研究主要基于传统的机器学习算法。例如，KronRLS 算法利用正则化最小二乘法结合相似性核函数进行预测；SimBoost 则利用梯度提升树（GBDT）提取特征。这些方法严重依赖于人工定义的分子指纹（如 ECFP4, MACCS）和蛋白质描述符（如 PseAAC），存在特征工程繁琐、难以捕捉深层非线性关系的问题。

**(2) 基于深度学习的序列模型**
2018 年，Öztürk 等人提出的 **DeepDTA** 模型标志着该领域进入深度学习时代。DeepDTA 将药物 SMILES 序列和蛋白氨基酸序列分别视为“文本”，利用一维卷积神经网络（1D-CNN）提取特征，并简单拼接后输入全连接层。随后，**GraphDTA** 将药物分子建模为图结构（Graph），利用图卷积网络（GCN）提取拓扑特征。然而，这些模型普遍采用简单的特征融合方式（Concatenation），无法有效建模药物与靶点之间的细粒度交互。

**(3) 注意力机制的引入**
为了解决交互建模问题，近年来的研究开始引入注意力机制（Attention Mechanism）。例如，AttentionDTA 在 CNN 基础上加入了单向注意力；TransformerDTA 则引入了功能强大的 Transformer 架构。虽然精度有所提升，但现有的注意力模型大多计算复杂度极高（O(N^2)），难以在普通硬件上进行大规模高通量筛选。且大多数模型缺乏对 DDI 任务的兼容性，无法满足多维度的筛选需求。

**(4) 综合评述与本项目切入点**
综上所述，当前领域虽已取得长足进步，但仍存在**“高精度与低算力不可兼得”**、**“有效性与安全性评估割裂”**、**“预测结果缺乏可解释性”**三大痛点。本项目拟通过轻量级双线性注意力机制解决算力与精度的平衡问题，通过多任务学习框架解决功能割裂问题，通过集成大语言模型（LLM）解决解释性问题，具有鲜明的创新性与可行性。

### 4. 参考文献
[1] Öztürk H, Özgür A, Ozkirimli E. DeepDTA: deep drug–target binding affinity prediction[J]. Bioinformatics, 2018, 34(17): i821-i829.
[2] Nguyen T, Le H, Quinn T P, et al. GraphDTA: predicting drug–target binding affinity with graph neural networks[J]. Bioinformatics, 2021, 37(8): 1140-1147.
[3] **Kim J H, Jun J, Zhang B T. Bilinear attention networks[C]. Advances in Neural Information Processing Systems (NeurIPS), 2018: 1564-1574.**
[4] Jaeger S, Fulle S, Turk S. Mol2vec: unsupervised machine learning embeddings with chemical substructures[J]. Journal of Chemical Information and Modeling, 2018, 58(1): 27-35.
[5] Asgari E, Mofrad M R K. Continuous distributed representation of biological sequences for deep proteomics[J]. PLoS One, 2015, 10(11): e0141287. (ProtVec 原文)
[6] Ryu J Y, Kim H U, Lee S Y. Deep learning improves prediction of drug–drug and drug–food interactions[J]. Proceedings of the National Academy of Sciences (PNAS), 2018, 115(18): E4304-E4311. (DeepDDI)
[7] **Yang Z, Zhong W, Zhao L, et al. ExDDI: Explaining Drug-Drug Interactions[C]. Proceedings of the 30th ACM International Conference on Information & Knowledge Management (CIKM), 2021: 2361-2370.**
[8] Vaswani A, Shazeer N, Parmar N, et al. Attention is all you need[C]. Advances in Neural Information Processing Systems (NIPS), 2017: 5998-6008.
[9] Huang K, Xiao C, Glass L M, et al. MolTrans: Molecular Interaction Transformer for drug–target interaction prediction[J]. Bioinformatics, 2021, 37(6): 830-836.
[10] Chen L, Tan X, Wang D, et al. TransformerCPI: improving compound–protein interaction prediction by sequence-based deep learning with self-attention mechanism[J]. Bioinformatics, 2020, 36(16): 4406-4414.
[11] Zitnik M, Agrawal M, Leskovec J. Modeling polypharmacy side effects with graph convolutional networks[J]. Bioinformatics, 2018, 34(13): i457-i466. (Decagon)
[12] He T, Heidemeyer M, Ban F, et al. SimBoost: a read-across approach for predicting drug–target binding affinities using gradient boosting machines[J]. Journal of Cheminformatics, 2017, 9(1): 1-14.
[13] Öztürk H, Ozkirimli E, Özgür A. WideDTA: prediction of drug-target binding affinity[J]. Bioinformatics, 2019, 35(15): 2656–2665.
[14] Shin B, Park S, Kang K, et al. Self-attention based molecule representation for predicting drug-target interaction[J]. PLoS Computational Biology, 2019, 15(5): e1007023.
[15] Pahikkala T, Airola A, Pietilä S, et al. Toward more realistic drug-target interaction predictions[J]. Briefings in Bioinformatics, 2015, 16(2): 325-337.
[16] Jin W, Barzilay R, Jaakkola T. Junction Tree Variational Autoencoder for Molecular Graph Generation[C]. International Conference on Machine Learning (ICML), 2018: 2323-2332.
[17] Zeng X, Zhu S, Lu W, et al. Target identification among known drugs by deep learning[J]. Journal of Chemical Information and Modeling, 2020, 60(3): 1785-1793.
[18] Lin X, Kwan D, Li X. Deep learning for drug-drug interaction prediction: A survey[J]. Current Bioinformatics, 2022, 17(5): 406-417.

---

## 三、 项目研究内容

### 1. 总体架构设计
本项目拟构建一个分层耦合的智能系统架构，自底向上分为**数据层、算法层、交互层**三个层级。
*   **数据层**：负责多源异构数据的采集、清洗、标准化存储与高效检索。
*   **算法层 (Core Engine)**：包含基于 GLU-CNN 的特征提取器、双线性注意力交互模块以及 DTA/DDI 双任务预测头。
*   **交互层 (User Interface)**：基于 GUI 图形界面的可视化操作平台，集成 RDKit 分子渲染与 LLM 文本生成模块。

### 2. 核心算法模块详解

#### (1) 基于 Mol2Vec 与 ProtVec 的分布式表征学习
为了让计算机“读懂”化学分子，我们需要将离散的符号序列转化为连续的稠密向量。
*   **药物嵌入**：本项目采用源自自然语言处理（NLP）Word2Vec 思想的 **Mol2Vec** 算法。我们将药物分子的 SMILES 字符串通过 Morgan 指纹算法打散成一系列子结构片段（Substructures），视作“单词”，将整个分子视作“句子”。在大规模化合物库上进行无监督预训练，使得化学性质相似的子结构在向量空间中距离更近。
*   **蛋白嵌入**：同理，对于蛋白质序列，我们采用 **3-mer** 切分策略，将氨基酸序列转化为 n-gram 词袋，利用 ProtVec 预训练模型生成高维特征矩阵。

#### (2) 基于门控线性单元（GLU）的深度卷积特征提取
在获得初始嵌入后，我们设计了深层的一维卷积神经网络（1D-CNN）来提取上下文特征。为了解决深层网络梯度消失及信息筛选效率低的问题，本项目创新性地引入了 **门控线性单元（Gated Linear Unit, GLU）** 作为激活机制。
GLU 的数学表达式为：
$$
 H_{out} = (X * W) \otimes \sigma(X * V) 
$$
其中，X 为输入，
$$
\sigma
$$
 为 Sigmoid 函数，
$$
\otimes
$$
 表示逐元素乘法。这种机制允许网络自动学习一个“门控”（Gate），类似于 LSTM 中的遗忘门，能够自适应地选择保留关键的生化特征（如疏水性、极性），并抑制无关的背景噪声，从而显著提升特征表达的纯度。

#### (3) 低秩双线性注意力机制（Low-Rank Bilinear Attention）
这是本项目的核心。传统的注意力机制通常直接计算 Dot-Product，而双线性注意力旨在捕捉两个模态之间的复杂二阶交互。设药物特征矩阵为 
$$
X \in R^{L_d \times D}
$$
，蛋白特征矩阵为 
$$
Y \in R^{L_p \times D}
$$
。我们定义双线性注意力图 A 为：
$$
A = Softmax((X^T U) \cdot (V^T Y))
$$
其中 U, V 为可学习的投影矩阵。为了减少参数量，防止过拟合，我们采用低秩近似（Low-Rank Approximation）的思想对权重矩阵进行分解。该模块能够模拟药物配体原子与蛋白受体残基之间的成对势能函数，从而在缺乏 3D 结构信息的情况下，隐式地学习到空间结合位点的分布信息。

#### (4) DDI 预测的孪生网络架构
针对药物-药物相互作用（DDI）任务，我们复用上述的药物特征提取器（Weight Sharing），构建孪生网络结构。系统将输入的两个药物分子 Pair (DrugA, DrugB) 分别通过同一个 Encoder 映射到同一特征空间，然后计算两者的双线性注意力交互。如果两者存在强烈的特征冲突（例如注意力权重异常集中于代谢酶结合位点），则判定为存在 DDI 风险。这种多任务学习（Multi-Task Learning, MTL）策略不仅节省了计算资源，还能通过不同任务间的正则化效应提升模型的泛化能力。

### 3. 软件系统功能设计与实现路径

**(1) 数据管理子系统**
*   **功能**：实现对 CSV, TSV, SDF, FASTA 等多种生物信息学格式文件的解析与导入。
*   **实现**：基于 Pandas 进行数据清洗，剔除无效 SMILES 和非标准氨基酸序列；利用 SQLite 构建本地关系型数据库，设计合理的表结构（Schema）存储分子 ID、序列信息及实验真值。

**(2) 3D 可视化子系统**
*   **功能**：支持药物分子的 2D 平面结构展示与 3D 空间构象渲染，支持旋转、缩放、原子着色等交互操作。
*   **实现**：集成 **RDKit** 计算化学库生成分子的 2D 坐标；利用 **AllChem.EmbedMolecule** 算法基于距离几何法生成 3D 构象；通过 Tkinter Canvas 或嵌入的 Matplotlib 窗口进行图形渲染。

**(3) 智能报告生成子系统**
* **功能**：当预测完成时，除了输出
  $$
  pK_d
  $$
   数值或 DDI 概率外，还能生成一段解释性文本。
*   **实现**：利用 **LangChain** 框架构建 Prompt Template（提示词模板），将提取到的药物关键子结构名称（如“苯环”、“羟基”）和预测结果填入模板，调用（本地部署或 API 接入的）大语言模型，生成诸如“由于该分子含有高反应活性的亲电基团，预测其与靶点半胱氨酸残基结合紧密...”的自然语言描述。

---

## 四、 项目主要创新点

**1. 理论方法的微创新：GLU-CNN 与 双线性注意力的有机融合**
本项目并未止步于简单的卷积神经网络应用，而是深入神经网络内部结构，将自然语言处理领域的门控机制（GLU）与计算机视觉领域的双线性注意力（BAN）进行跨界融合。相比 DeepDTA 等基线模型，这种融合架构显著增强了模型对生物序列局部与全局特征的捕获能力，在理论层面具有一定的先进性。

**2. 系统架构的集成创新：多任务联合学习框架**
打破了现有软件功能单一的局限。通过巧妙设计的孪生网络架构这种“一模多用”的设计思路，不仅大幅降低了模型部署的存储空间需求，更体现了“系统生物学”中整体性分析的科学理念。

**3. 交互模式的应用创新：GenAI 驱动的可解释性增强**
创新性地引入生成式人工智能（GenAI）技术解决科学计算的“黑盒”问题。大多数同类大创项目仅停留在数值输出层面，而本项目率先尝试利用 LLM 技术将冷冰冰的数据转化为科研人员易于理解的自然语言报告，显著提升了软件的用户体验与辅助决策价值。

**4. 部署与安全理念创新：全栈本地化 (Local-First)**
顺应数据安全与隐私保护的时代潮流，项目坚持“数据不出域”的原则。所有的核心计算流程——包括特征提取、模型推理、数据库读写——均设计为在本地计算终端完成。这种设计为那些对数据高度敏感的制药企业和实验室提供了一个安全可靠的解决方案，具有极高的推广潜力。

---

## 五、 项目预期成果

1.  **实物成果：智能药物筛选软件系统 (V1.0)**
    *   提交完整的 Windows 平台安装包（.exe），无需配置复杂的 Python 环境即可一键运行。
    *   软件具备完善的图形用户界面（GUI），包含数据中心、模型训练、预测分析、3D 可视化、报告生成五大功能模块。
    *   软件运行稳定，响应迅速，界面美观，交互逻辑符合科研人员操作习惯。

2.  **技术文档与源码**
    *   提交不少于 5000 行的规范化 Python 源代码，代码注释率超过 30%，遵循 PEP8 编码规范。
    *   提供完整的《用户操作手册》、《软件架构设计文档》及《API 接口文档》。

3.  **学术与科研产出**
    *   **学术论文**：撰写并投稿 1 篇应用型学术论文（推荐投稿至 *Journal of Chemical Information and Modeling* 或生物信息学相关 IEEE 会议），详细阐述双线性注意力网络在药物筛选中的应用效果。
    *   **高质量数据集**：整理清洗出一套包含肺癌 EGFR 靶点相关的高质量数据集，包含结构化清洗后的药物分子 15,000+ 个，相互作用条目 50,000+ 条。

4.  **模型资产**
    *   输出经过充分训练与调优的深度学习模型权重文件（.pth格式），模型在 Davis 测试集上的 CI 指数（一致性指数）达到 0.88 以上，MSE 误差低于 0.25，在同类轻量级模型中处于领先水平。

---

## 六、 进度安排

**第一阶段：需求分析与数据准备（第 1-2 月）**
*   细化软件功能需求，绘制 UML 用例图与流程图。
*   从 Davis, Kiba, DrugBank 等数据库下载原始数据。
*   编写 Python 脚本（使用 RDKit 和 Pandas）对数据进行清洗、去重、标准化处理，构建 Mol2Vec 语料库。

**第二阶段：核心算法研发与模型训练（第 3-5 月）**
*   搭建 PyTorch 深度学习开发环境。
*   编写 LLMDTA.py 和 `LLMDDI.py`，实现 GLU-CNN 编码器和 BANLayer 注意力层。
*   在高性能服务器上进行模型训练，利用网格搜索（Grid Search）策略优化超参数（如学习率、Batch Size、注意力头数）。
*   记录训练日志，绘制 Loss 曲线，验证模型收敛性。

**第三阶段：软件系统开发与集成（第 6-8 月）**
*   基于 Tkinter 库设计并实现主界面布局。
*   开发数据库连接模块，实现数据的增删改查功能。
*   集成 RDKit 分子可视化功能，将静态分子数据转为动态 3D 图像。
*   集成 LangChain 接口，调试 Prompt 提示词，实现简易的报告生成功能。

**第四阶段：系统测试与优化（第 9-10 月）**
*   进行单元测试（Unit Test）和集成测试，修复软件 Bug。
*   邀请药学专业同学试用，根据反馈优化交互逻辑。
*   对模型进行剪枝和量化处理，提升软件在普通电脑上的运行速度。

**第五阶段：结题总结与成果发表（第 11-12 月）**
*   整理实验数据，绘制精美的结果对比图表。
*   撰写学术论文与结题报告。
*   录制软件演示视频，准备答辩 PPT。

---

## 七、 可行性分析

**1. 坚实的理论基础与技术积累**
项目组成员在前期已完成了大量相关文献的阅读与复现工作。目前的开源代码库中，我们已经实现了基于 PyTorch 的基础 DTA 预测框架以及 Tkinter 的界面原型。核心的 Mol2Vec 向量化技术和 CNN 网络结构已有成熟的代码实现，这为后续引入更高级的双线性注意力机制打下了坚实基础。技术路线上不存在无法逾越的“黑障”。

**2. 成熟的开发工具与生态支持**
本项目所依托的技术栈均为目前工业界和学术界的主流选择：
*   **Python**: 拥有最丰富的科学计算生态（NumPy, Pandas）。
*   **PyTorch**: 最灵活强大的深度学习框架，社区资源极其丰富。
*   **RDKit**: 化学信息学领域的实际标准库，功能强大且稳定。
*   **LangChain**: 连接 LLM 的标准中间件，极大简化了开发流程。
这些成熟工具的组合使用，大大降低了从零开发的风险，确保了项目的高完成度。

**3. 完备的软硬件实验条件**
项目组依托校级计算机实验教学中心与人工智能实验室，拥有充足的算力资源（NVIDIA GPU Server）用于模型训练。实验室具备稳定的网络环境以访问 HuggingFace 等开源社区。同时，我们拥有完整的数据集资源（已下载并备份了超过 10GB 的原始数据），数据来源合法、合规。

**4. 科学合理的项目管理**
项目组采用了敏捷开发（Agile Development）的管理模式。我们将大目标拆解为两周一个周期的 Sprint（冲刺），每个周期都有明确的可交付成果（如：完成数据清洗脚本、完成 UI 原型图）。成员之间分工明确，有人负责算法，有人负责界面，有人负责文档，并通过 Git 进行严格的代码版本管理，确保项目进度可控、质量可控。