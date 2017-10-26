lncRNA 流程使用说明

## 一 RNA-Seq_Standard
### 创建你自己的项目, 使用 `RNAseq_new`
```
USAGE: RNAseq_new <analysis_dir> [species_name: hg19]
```  
这里我们创建名为 TEST_RNA 的项目, 并使用用于测试的参考基因组 test  
```
RNAseq_new TEST_RNA test
```  
在当前目录下, 可以看到 TEST_RNA 项目文件夹. 该文件夹应当包含以下内容  
* code: 程序主目录
* meta_data
   + download_list.txt: 原始 fastq 文件所在路径, 及其对应的 ID, Sample 名称, 配置方法请参考设置部分
   + group_info.txt: 差异表达分析要用到的信息, 配置方法请参考设置部分
   + signature.txt / target.txt: 关注的 Gene ID
   + gdc-user-token.xxxxxx.txt
* params: 自定义运行参数
* pipeline: 运行结果所在目录
* raw_data: 存放原始 fastq 文件 (非必需), 可将原始数据存放于磁盘任何位置, 只要 `download_list.txt` 设置正确
* referenceFiles: 参考基因组及相应的注释文件等
* run.bash
* start_rna.bash: 任务提交脚本
### 设置
1. meta_data/download_list.txt: 第一列为 sample 名, 第二列为 ID 号, 第三列为原始 fastq.gz 所在路径. fastq.gz 需命名如下:
   * ID_L001_R1.fastq.gz
2. meta_data/group_info.txt: 第一行为表头. 第一列为 sample 名, 需要与 `download_list.txt` 的 sample 名对应; 第二列为分组信息
3. params: 该流程使用 `STAR` 进行比对, 需提供对应基因组注释文件 (GTF 格式). 参数可自定义
   * 修改 params 中 `STAR` 的参数 `--sjdbGTFfile` 到对应的 GTF 文件
   * 修改 params 中 `DESeq2` 的参数到对应的 GTF 文件
   * 若不希望执行某一步骤, 则注释该行
4. signature.txt / target.txt: 关注的 Gene ID, 注意 Gene ID 需要与 3 中基因组注释文件一致
5. [高级] 若分析的物种尚未建立 `STAR` 索引, 则项目底下的 `referenceFiles` 为 broken links. 删除并建立名为 `referenceFile` 的文件夹, 拷贝 `code` 下的 `files_needed.bash` 到 `referenceFile` 中, 根据需要修改 `files_needed.bash` 后在 `referenceFile` 下运行该脚本即可
### 任务提交
```
yhbatch -N 1 start_rna.bash
```
`start_rna.bash` 文件中, 修改 `NSLOTS` 变量, 指定所需线程数  
### 结果
pipeline 的文件结构为:   
```
|-- fastq
|-- alignment
   |-- <sample>: STAR, <Markduplicate> 运行结果所在文件夹. 主要有以下文件: 
       *.Log.final.out, *count.txt, *.bw (track file), accepted.bam, sequence_info.txt, run.bash
|-- cufflinks
   |-- <sample>: assembling 结果所在文件夹. 主要文件: *.fpkm_tracking, transcript.gtf, run.bash
|-- Fastqc
|-- summarize
   |-- <group>: align_summary.txt, raw_count.txt
|-- report & report.tar.gz: You can download this file and create a HTML report in your machine
|-- <DATE>_<TIME>: the Log files, check these files if you don’t have seen any expected file
```
## 二 lncRNA-screen
### 创建你自己的项目, 使用 `lncRNA_new`
```
USAGE: lncRNA_new <analysis_dir> <RNA_prj> <ChIP_prj> [species_name: hg19]
```  
这里我们创建名为 TEST_lncRNA 的项目, 并使用用于测试的参考基因组 test. 这里 TEST_RNA, TEST_ChIP 分别为你的 RNA-Seq 的项目, ChIP-seq 的项目, 并且与 TEST_lncRNA 位于同一目录下  
```
lncRNA_new TEST_lncRNA TEST_RNA TEST_ChIP test
```  
在当前目录下, 可以看到 TEST_lncRNA 项目文件夹. 该文件夹应当包含以下内容  
* ``_##_<NAME>``: ## 表示数字, 这些文件夹表示运行的中间结果, 其中 `_11_report` 包含 HTML 报告
* cdoe: 程序主目录
* input: 
* pipeline: 运行结果所在目录
* referenceFiles: 参考基因组及相应的注释文件等
* run.bash
* start_lncRNA.bash: 任务提交脚本
### 设置
1. inputs/<ChIP_prj>: Your ChIP-Seq analysis results. Make sure you have peak files in bed format in your `inputs/<ChIP_prj>/bed` directory. You can generate them by performing your own ChIP-Seq analysis. Otherwise, the bed files can be obtained from well-known projects, for example `ENCODE` project
2. inputs/<RNA_prj>: Make sure this link link properly with the directory of your `RNA-Seq_Standard` project you set in `STEP 1`
3. inputs/group_info.txt: Please follow this example file to set up your sample sheet. Please make sure you match your sample name with the sample name you used in `RNA-Seq_Standard` pipeline (Sample name should match the directory name in the `RNA-Seq/pipeline/alignment/` folder and `RNA-Seq/pipeline/cufflinks`)
4. inputs/params.bash: Please change the parameters as your desire in this file
   * [description of setting parameters] Building
5. inputs/custom-bashrc: this file set up the path to all necessary dependencies. Please check `inputs/system_requirement.txt` for all dependencies requirement
6. [Advanced]: If you are working on a different reference version or species, you may need to set up `referenceFiles` directory:
   * If you found the `referenceFiles` is a broken link, it means you provide a wrong ID for the species. If not, you should set up `referenceFiles` by yourself. Delete `referenceFiles` and create a new `referenceFiles` directory. Follow the `code/build_referenceFiles.bash` script (set up the necessary files in `referenceFiles`) and run this command at your project folder `<analysis_dir>`
   * You can obtain the files mentioned in `build_referenceFiles.bash` from well-known projects, for example `GENCODE` project
   * Please check if you have replaced all the files in this directory as your own desire. Also, please make sure you use the same reference version or species in `inputs/RNA-Seq/referenceFiles`
   * Please don't forget to change your `inputs/params.bash` file if you use a different reference version or species and finished setting up the `referenceFiles` directory
### 任务提交
```
yhbatch -N 1 start_lncRNA.bash
```
`start_lncRNA.bash` 文件中, 修改 `NSLOTS` 变量, 指定所需线程数  
### 结果
``_##_<NAME>`` 的文件结构为:   
```
|-- _01_ChIP-Seq
|-- _01_RNA-Seq
|-- _02_cuffmerge
   |-- merged.gtf, assemblies_list.txt, run.bash
|-- _03_identify: Identify lncRNA
|-- _04_whole_assembly
   |-- all.gtf
|-- _05_coding_potential: Accessment of potential coding region by using CPAT tool
   |-- gencode-lncRNA*
   |-- gencode-mRNA*
   |-- lncRNA*
   |-- novel-lncRNA*
|-- _05_featureCounts
   |-- <sample>: counts.txt, featureCounts.txt, featureCounts.txt.summary, run.bash
   |-- *out
   |-- raw_count.txt
|-- _06_annotate: annotate lncRNA from other annotation files
|-- _06_summarize: run DESeq2 by user-defined group
   |-- fpkm_table.txt
   |-- norm_count.txt
   |-- lncRNA_fpkm_table.txt
   |-- mRNA_fpkm_table.txt
|-- _07_fpkm_cutoff： Calculating FPKM Cutoff
   |-- Group
|-- _07_peak_overlap: Overlapping ChIP-Seq peaks grouping by user-defined group
   |-- Group
|-- _08_integrate_DE： Integrating FPKM cutoff and Differential Expression Analysis result grouping by user-defined group
   |-- Group
|-- _08_integrate_HistoneCombine： Integrating FPKM cutoff and ChIP-Seq peaks overlap grouping by user-defined group
   |-- Group
|-- _09_pie_matrix_DE: Making Pie-matrix
|-- _09_pie_matrix_peak: Making Pie-matrix
|-- _10_figures
|-- _10_snapshot
|-- _10_tracks
|-- _11_report: a HTML report
```
pipeline 的文件结构除了以上 ``_##_<NAME>`` 部分, 还包括:  
```
|-- <DATE>_<TIME>: the Log files, check these files if you don’t have seen any expected file
```

