# 5 篇论文要点 → 对应页码与章节（Section-level）

> 本文档由 `tools/paper_section_locator.py` 自动生成。
> 章节标题从 PDF 页面文本中用正则抽取（`\d. Title` 模式），若 PDF 排版不规则可能有偏差。


---

## Inoue 等 - 2025 - DrugAgent multi-agent large language model-based reasoning for drug-targe


### 要点：Inoue-DrugAgent-DTI: multi-agent framework + tool use

| 页码 | 所在章节（推断） | 关键词 | 上下文片段 |
|------|-----------------|--------|------------|
| p.1 | Abstract | `DrugAgent` | es face challenges due to complex biological systems and the lack of interpretability needed for clinical applications. DrugAgent is a multi-agent LLM system for DTI prediction tha… |
| p.2 | 2 R ELATED WORKS Machine Learning in Drug Target Interaction | `DrugAgent` | sential for clinical decision-making and regulatory compliance. Code is available at https: //anonymous.4open.science/r/DrugAgent-B2EA. 1 I NTRODUCTION Large Language Models (LLMs)… |
| p.3 | 3.1 O VERVIEW OF DRUG AGENT | `tool` | Preprint 2023). Recent studies have demonstrated that LLM-based search tools can enhance the efficiency and complexity of queries compared to traditional search engines (Spathariot… |
| p.4 | 3.2.1 C OORDINATOR AGENT | `Figure` | rom score and reason Answer 1. Evidence Analysis 2. Mechanism Evaluation 3. Consistency Validation 4. Score Calculation Figure 1: Multi-agent system architecture for DTI analysis. … |

### 要点：Inoue-DrugAgent-DTI: reasoning trace / stepwise reasoning

| 页码 | 所在章节（推断） | 关键词 | 上下文片段 |
|------|-----------------|--------|------------|
| p.1 | Abstract | `chain-of-thought` | omain-specific data sources, including ML predictions, knowledge graphs, and literature evidence, and (3) incorporating Chain-of-Thought (CoT) and ReAct (Reason+Act) frameworks for… |
| p.2 | 2 R ELATED WORKS Machine Learning in Drug Target Interaction | `reasoning` | specific aspect of the drug discovery process. Our architecture includes five agents: Coordinator, AI, KG, Search, and Reasoning Agent. The Coordinator Agent manages communication … |
| p.3 | 3.1 O VERVIEW OF DRUG AGENT | `chain-of-thought` | et al., 2023). LLMs with Reasoning LLMs with reasoning is a current trend in 2024. With several techniques, such as the Chain-of-Thought (CoT) (Wei et al., 2022b) and ReAct (Reason… |
| p.5 | 3.2.3 KG A GENT | `trace` | s, including FDA-approved small-molecule drugs, biopharmaceuticals (proteins, peptides, vaccines, and allergens), and nutraceuticals. • Comparative Toxicogenomics Database (CTD): T… |


---

## Li 等 - 2025 - DrugPilot LLM-based parameterized reasoning agent for drug discovery.compare


### 要点：Li-DrugPilot: parameterized reasoning (structured outputs)

| 页码 | 所在章节（推断） | 关键词 | 上下文片段 |
|------|-----------------|--------|------------|
| p.1 | Abstract | `DrugPilot` | DrugPilot: LLM-based Parameterized Reasoning Agent for Drug Discovery Kun Li1†, Zhennan Wu1†, Shoupeng Wang2†, Jia Wu3, Shirui Pan4, Wenbin Hu1* 1School of Computer Science, Wuhan … |
| p.2 | Abstract | `parameter` | s requiring automated, interactive, and data-integrated reasoning. Keywords: large language model, agent, tool calling, parameterized reasoning, drug discovery With the rapid devel… |
| p.3 | Abstract | `DrugPilot` | task focus DrugAgent, DrugAssist, MolecularGPT, … Difficulty in multi-turn collaboration MLE-bench, CTR, Granite, … DrugPilot (Ours) Solve Easily ! ! ! DrugPilot’s Application Scen… |
| p.4 | Abstract | `structured` | (=O)(=O)NC1=C(C(=C(C=C1)F)C(=O)C2=CNC3=C2C=C(C=N3)Cl)F' ] }Cut off due to length or space limit. Completely stored in a structured format. Precise Record Structured Data GDSS for R… |

### 要点：Li-DrugPilot: controllability / reproducibility

| 页码 | 所在章节（推断） | 关键词 | 上下文片段 |
|------|-----------------|--------|------------|
| p.1 | Abstract | `log` | hina. 3Department of Computing, Macquarie University, Sydney, Australia. 4School of Information and Communication Technology, Griffith University, Brisbane, Australia. *Correspondi… |
| p.2 | Abstract | `log` | affinity prediction [16], and molecular property prediction [17, 18] and so on. However, researchers in phar- macy, biology, and other related fields often lack the technical exper… |
| p.10 | Abstract | `determin` | e core engine for MPP. In this case study, we evaluate its predictive capabilities on a binary classification task that determines whether a molecule functions as a BACE inhibitor.… |
| p.12 | 5 Notations: | `determin` | tely based on tool specifications and observations. The distribution of samples across different tools and patterns was determined considering their usage scenarios, parameter comp… |


---

## Liu 等 - 2025 - DrugAgent automating AI-aided drug discovery programming through LLM multi-


### 要点：Liu-DrugAgent-AutoProg: multi-agent collaboration for coding

| 页码 | 所在章节（推断） | 关键词 | 上下文片段 |
|------|-----------------|--------|------------|
| p.1 | 1 Introduction and Related Work | `agent` | DrugAgent: Automating AI-aided Drug Discovery Programming through LLM Multi-Agent Collaboration Sizhe Liu1, Yizhou Lu1, Siyu Chen1, Xiyang Hu2, Jieyu Zhao1, Yingzhou Lu3, Yue Zhao1… |
| p.2 | 2 Methodology We present DrugAgent, a multi-agent LLM frame- | `agent` | Table 1: Key differences between DrugAgent and existing agent methods. DrugAgent stands out by: 1) interacting with the environment, 2) specializing in ML programming, 3) incorpora… |
| p.3 | 3.2 Quantitative Results | `code` | on specialized workflows, e.g., the correct handling of SMILES strings and tailored data preprocess- ing. When standard code-generation approaches ig- nore this domain requirements… |
| p.4 | 4 ADMET HTS DTI | `collaboration` | and the nu- anced demands of pharmaceutical research. We believe this work opens exciting new avenues for research and collaboration, pushing the boundaries of AI-driven drug disco… |

### 要点：Liu-DrugAgent-AutoProg: roles (planner/engineer/reviewer)

| 页码 | 所在章节（推断） | 关键词 | 上下文片段 |
|------|-----------------|--------|------------|
| p.1 | 1 Introduction and Related Work | `critic` | f domain-specific documentation covering data ac- quisition, data transformation, and advanced model design, supporting critical tasks in drug discov- ery. We evaluate DrugAgent on… |
| p.2 | 2 Methodology We present DrugAgent, a multi-agent LLM frame- | `planner` | tDomain Tools RandomForestGCN Final Code &Self DebuggingResearch Task(eg: ADMET) Coder Dataset DownloadingFingerprintingPlanner Instructor Construction Failed ...... Identified Dom… |
| p.3 | 3.2 Quantitative Results | `critic` | set of targeted doc- uments to build or refine specialized tools. The Instructor then generates a performance report—if critical functionalities are absent, it returns a failure re… |
| p.4 | 4 ADMET HTS DTI | `role` | he Plan- ner and Instructor contribute significantly to over- all performance. Additional qualitative analysis of their roles is provided in Appendix G. 3.3 Case Study Comparing Dr… |


---

## Sun 等 - ExDDI Explaining Drug-Drug Interaction Predictions with Natural Language.compare.p


### 要点：Sun-ExDDI: natural language explanation for DDI predictions

| 页码 | 所在章节（推断） | 关键词 | 上下文片段 |
|------|-----------------|--------|------------|
| p.1 | Abstract | `ExDDI` | ExDDI: Explaining Drug-Drug Interaction Predictions with Natural Language Zhaoyue Sun1, Jiazheng Li2, Gabriele Pergola1, Yulan He1,2,3 1Department of Computer Science, University o… |
| p.2 | Abstract | `ExDDI` | ive and in- ductive settings to meet the needs of application scenarios. We propose and evaluate the performance of the ExDDI family methods for DDI explanation generation, which i… |
| p.3 | Abstract | `rationale` | ween these drugs when administered together. Additionally, we aim to generate a textual explanation, s, elucidating the rationale behind the existence or non-existence of DDIs. For… |
| p.5 | Abstract | `generated` | diction, since our model does not di- rectly learn from multi-class tasks, we estimate its perfor- mance by mapping the generated explanations to mecha- nism categories. Specifical… |

### 要点：Sun-ExDDI: evaluation of explanations

| 页码 | 所在章节（推断） | 关键词 | 上下文片段 |
|------|-----------------|--------|------------|
| p.2 | Abstract | `evaluation` | tworthy AI-driven drug safety research. We created the ExDDI model family for this task and carried out a comprehensive evaluation, offering tools and baselines for future studies.… |
| p.4 | Abstract | `evaluation` | description and statistics of the data are reported in Appendix C (Sun et al. 2024). Settings for Model Generalisation Evaluation To exam- ine the model’s generalisation ability to… |
| p.5 | Abstract | `metric` | el faces greater challenges in multi-classification tasks, which should be considered when comparing models. Evaluation Metrics We evaluate DDI explanation gener- ation using metri… |
| p.9 | Abstract | `human` | ocessing systems, 35: 24824–24837. Wiegreffe, S.; Hessel, J.; Swayamdipta, S.; Riedl, M.; and Choi, Y . 2022. Reframing Human-AI Collaboration for Gen- erating Free-Text Explanatio… |


---

## Wang 等 - PKAG-DDI Pairwise Knowledge-Augmented Language Model for Drug-Drug Interaction Ev


### 要点：Wang-PKAG-DDI: knowledge-augmented language model

| 页码 | 所在章节（推断） | 关键词 | 上下文片段 |
|------|-----------------|--------|------------|
| p.1 | 1 Introduction Unexpected drug-drug interactions (DDIs) may | `PKAG` | ics (Volume 1: Long Papers), pages 10996–11010 July 27 - August 1, 2025 ©2025 Association for Computational Linguistics PKAG-DDI: Pairwise Knowledge-Augmented Language Model for Dr… |
| p.2 | 1 Introduction Unexpected drug-drug interactions (DDIs) may | `PKAG` | tion strategy is the second challenge. In this work, we propose a novel pairwise knowledge-augmented generative method (PKAG- DDI) for DDIE generation, which selects the pair- wise… |
| p.3 | 3.1 Problem Formulation | `entity` | focus on developing effi- cient feature encoders (e.g., DNNs, GNNs) to learn drug pair representations from molecular identity information, including SMILES (Simplified Molec- ular… |
| p.4 | 3.2 Pairwise Knowledge Selector (PKS) | `graph` | S to two commonly used initial molecular modalities by an RDKit tool: a fingerprint (Glen et al., 2006) and a molecular graph (i.e., atoms as nodes and bonds as edges). The molecul… |

### 要点：Wang-PKAG-DDI: pairwise knowledge / event generation

| 页码 | 所在章节（推断） | 关键词 | 上下文片段 |
|------|-----------------|--------|------------|
| p.1 | 1 Introduction Unexpected drug-drug interactions (DDIs) may | `event` | sociation for Computational Linguistics PKAG-DDI: Pairwise Knowledge-Augmented Language Model for Drug-Drug Interaction Event Text Generation Ziyan Wang1*, Zhankun Xiong1∗, Feng Hu… |
| p.2 | 1 Introduction Unexpected drug-drug interactions (DDIs) may | `generation` | E prediction. Thus, incorporating biological functions holds promise for improving the capa- bility of LM for DDIE text generation. However, biological functions are specialized kn… |
| p.3 | 3.1 Problem Formulation | `event` | llenging inductive scenarios, indicating its practicality and generalization. 2 Related Works 2.1 Drug-Drug Interaction Event Prediction Current DDIE prediction methods generally f… |
| p.5 | 3.3 Learning with Pairwise Knowledge Integration Strategy | `prompt` | , we also input the SMILES tokens of the drug pair Sa and Sb to LM. Thus, the query input xis formulated as: x= x(a,b) =Prompt(Sa,Sb,Ta,Tb), (5) where Prompt is the prompt text wit… |
