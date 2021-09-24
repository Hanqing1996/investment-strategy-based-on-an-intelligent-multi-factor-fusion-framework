## Introduction
This repository is the source code of the paper **'An Analytical Model for Normative Financial Textsand Research on Financial Strategies in anIntelligent Multi-factor Framework'**,which has been accepted by as a regular paper to be presented in CyberSciTech 2021. 
---
## Moduels
#### GetStockData
> Collect stock data of specified codes (including historical price, volume, etc.), filter redundant data, serialize to DataFrame format, and output to specified directory.

#### DealWithReportsTable
> Collect report data, extract and summarize valid fields of the report, such as report title, stock recommendation, rating and so on.

#### GetSeriesFactories
> Serialize the valid factors, including RC factory and RV factory.

#### MainStrategy
> After extracting these factors, we use genetic algorithm to determine the optimal weight allocated to each factor in the near period of time, so as to constitute the investment strategy most consistent with the current market style.
---
## Additional instructions 
The investment strategy based on this model has been used for commercial purposes. In consideration of commercial agreements and intellectual property issues, some algorithm details have been blurred, and some original data have not been disclosed.
---

## Author
Hanqing Zhu,
College of Computer Science and Technology,Hangzhou Dianzi University,
zhq192050154@hdu.edu.cn
