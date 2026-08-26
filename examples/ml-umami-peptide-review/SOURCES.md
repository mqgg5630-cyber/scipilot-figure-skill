# 机器学习筛选鲜味肽综述图：资料依据

本图是根据下列文献独立综合绘制的概念框架，并未复刻任何一篇论文的原图。图中候选数量为示意范围，不代表固定阈值。

## 主要资料

1. **Charoenkwan et al. (2020), iUmami-SCM.** 首个基于一级序列、氨基酸/二肽倾向评分卡的鲜味肽预测器；为图中“可解释模型”路线提供依据。  
   DOI: https://doi.org/10.1021/acs.jcim.0c00602

2. **Charoenkwan et al. (2021), UMPred-FRL.** 融合 7 类序列编码和 6 类机器学习算法的特征表示学习元预测器；支持“多编码 + 集成学习”路线。  
   DOI: https://doi.org/10.3390/ijms222313124

3. **Jiang et al. (2022), iUP-BERT.** 使用 BERT 表征、SMOTE 和 SVM 进行鲜味肽识别，并强调交叉验证和独立测试；支持“预训练嵌入 + 类别平衡 + 外部验证”路线。  
   DOI: https://doi.org/10.3390/foods11223742  
   Full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC9689418/

4. **Cui et al. (2023), TastePeptides-Meta / Umami_YYDS.** 整合 TastePeptidesDB、GBDT 分类模型和开放工具；支持“数据库—模型—筛选”基础设施。  
   DOI: https://doi.org/10.1016/j.foodchem.2022.135216

5. **Qi et al. (2023), Umami-MRNN.** 将 RNN 与 MLP 合并，并使用多种特征向量；独立测试报告 ACC 90.5%、MCC 0.811，支持深度学习筛选路线。  
   DOI: https://doi.org/10.1016/j.foodchem.2022.135248

6. **Geng et al. (2025).** 将宏基因组候选库、CNN/LSTM/Attention/Transformer 集成预测、SHAP、分子建模与感官验证串联；三条候选肽的感官阈值为 0.11、0.37 和 0.44 mg/mL。  
   DOI: https://doi.org/10.3390/foods14142422  
   Full text: https://www.mdpi.com/2304-8158/14/14/2422

7. **Wu et al. (2026).** 在非酒精啤酒中串联肽组学、机器学习、T1R1/T1R3 对接、MM-GBSA 和食品基质感官验证，并明确指出计算筛选不能替代感官证据。  
   DOI: https://doi.org/10.3390/foods15101671

## 图中信息与文献的对应关系

- **候选库来源**：肽组学、从头测序、虚拟酶解和宏基因组见文献 6–7。
- **序列表征**：AAC/DPC/CTD 等人工特征见文献 1–2；BERT 表征见文献 3。
- **模型谱系**：评分卡、集成学习、GBDT、RNN/MLP 与 Transformer 路线见文献 1–6。
- **机制排序**：T1R1/T1R3 对接、分子动力学或 MM-GBSA 用于解释和优选，见文献 6–7。
- **最终验证**：合成肽、盲法感官阈值、正交仪器证据和食品基质验证见文献 4、6–7。
- **闭环思想**：图中“实验标签回流再训练”为对现有流水线的工程化综合建议，并非某篇论文的原句。

## 编辑说明

SVG 中的文字全部保留为 `<text>`，每个流程阶段均置于独立 `<g id="stage-N">` 图层。可使用 Inkscape、Adobe Illustrator、Affinity Designer、Figma 或浏览器直接编辑。重新生成：

```bash
python examples/ml-umami-peptide-review/generate_figure.py
```
