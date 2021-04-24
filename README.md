# EMOFM-Python-reproducing

算法未能够完全实现复现，只是实现了前半部分，未能达到预期，且可预见后半部分复杂度过于高，靠个人计算机基本不可能达到文章宣称的算法效果，因此放弃。
但是依然具有部分参考意义，起码是想法还不错。


使用方法：
运行ARMOEA.py可以实现文章算法stage1部分内容
EFOMF.py是整个算法的大框架，其中stage2部分尚未实现

结果：运行20次进化，画出最后一次所有chromosome的聚类图形，以及优化值的对比


refpoint_adaption.py为论文“An indicator based multi-objective evolutionary algorithm with reference point adaptation for better versatility”中的算法，并进一步使用了nondominated sorting(NS)算法，NS算法在文章“An Efficient Approach to Nondominated Sorting for Evolutionary Multiobjective Optimization”中


由于实验复现未全部完成，所以没有详细地写各个部分的注释，望谅解以及改进
