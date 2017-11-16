## QualChk

**USAGE:** 
```
qualchk [+h] [+i INPUTS] [+l LIST] [+t {1,2}] [+q QUALITY]
        [+f FASTQC] [+a ADAPTER] [+n NS] [+o OUTPUT] [+c CLIP]
        [+r RRBS] [+p PAIRED] [+T TEMPLATE]
```

Consistently apply adapter trimming and quality check to FastQ files, with extra functionality for RRBS data. A wrapper around `Trim Galore` (a wrapper around `Cutadapt` and `FastQC`) and post-process script (such as information extraction and report generation).

To run this software, [Trim Galore](https://github.com/FelixKrueger/TrimGalore) and [FastQC](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/) should be installed and be added to your environment variable `PATH`.

Due to `-/--` would present in arguments frequently, users should be noticed that `+/++` were used as the prefix character(s) for each option, instead of `-/--`. Type `qualchk +h` to see more details. In addition, arguments inherit from `Trim Galore` should always be quoted and use the long option (e.g. use `--quality`, instead of `-q`). Here the example:   
```
qualchk +T template/1.QualChk.md +p "--paired" +t 2 +q "--quality 0 --phred33" +o "--output_dir _02_QC" +l _01_rawData/filelist.txt
```

the quoted string are the arguments inherit from `Trim Galore`, they are quoted and only use the long option.

**Installation** are simple: download the package and then type `mv qualchk /usr/bin` in your terminal.

Bellow are the **table of content** with the fully description of arguments:   
1. [General options](#generalopt)
2. [Options inherit from `Trim Galore`](#trimgalore)
	* [Quality](#quality)
	* [FastQC](#fastqc)
	* [Adapter](#adapter)
		* [Reduce random matches](#reduce-random-matches)
	* [Ns](#ns)
	* [Output](#output)
	* [Clip bases defined by user](#clip)
    * [RRBS-specific options (MspI digested material)](#rrbs-specific-options)
    * [Paired-end specific options](#paired-end)
3. [Example](#example)

### <a name="generalopt"></a>General options:

* `+h, ++help`
  * Print this help message and exits.
* `+i INPUTS, ++inputs INPUTS`
  * the input FastQ file(s) for for *one sample*, sperated by space and *should be quoted*.
* `+l LIST, ++list LIST`
  * filename that store the input FastQ list for multiple samples;
  This opt will cover `inputs` opt;
  If flag `paired` present, every two line stands for a sample. Otherwise, one line for one sample.
* `+t {1,2}, ++threads {1,2}`
  * number of threads used (better equal to the number of input files).
  * Default: `1`
* `+T TEMPLATE, ++template TEMPLATE`
  * the report template, see folder template for the available template.
  * Default: `template/1.QualChk.md`

### <a name="trimgalore"></a>Options inherit from `Trim Galore`:

* `+q QUALITY, ++quality QUALITY`
  * quality options of Trim Galore. *Should be quoted*.
  * Default: `--quality 20 --phred33`
* `+f FASTQC, ++fastqc FASTQC`
  * Run FastQC on the FastQ file before and after trimming. *Should be quoted*.
  * Default: `--fastqc_args \"--extract --quiet\"`
* `+a ADAPTER, ++adapter ADAPTER`
  * adapter options of Trim Galore. *Should be quoted*.
  * Default: `--illumina --length 20 --stringency 3 -e 0.1`
* `+n NS, ++Ns NS`
  * options for dealing with `N`s. *Should be quoted*.
* `+o OUTPUT, ++output OUTPUT`
  * output options of Trim Galore. *Should be quoted*.
  * Default: `--output_dir ./`
* `+c CLIP, ++clip CLIP`
  * clip bases defined by user. *Should be quoted*.
* `+r RRBS, ++rrbs RRBS`
  * RRBS-specific options (MspI digested material). *Should be quoted*.
* `+p PAIRED, ++paired PAIRED`
  * Paired-end specific options. *Should be quoted*.

**The available option from Trim Galore:**

#### <a name="quality"></a>1. Quality
* `--quality <INT>`
  * Trim low-quality ends from reads in addition to adapter removal. For RRBS samples, quality trimming will be performed first, and adapter trimming is carried in a second round. Other files are quality and adapter trimmed in a single pass. The algorithm is the same as the one used by BWA (Subtract INT from all qualities; compute partial sums from all indices to the end of the sequence; cut sequence at the index at which the sum is minimal).
  * Default Phred score: `20`.
* `--phred33`
  * Instructs Cutadapt to use `ASCII+33` quality scores as Phred scores (Sanger/Illumina 1.9+ encoding) for quality trimming.
  * Default: `ON`
* `--phred64`
  * Instructs Cutadapt to use `ASCII+64` quality scores as Phred scores (Illumina 1.5 encoding) for quality trimming.

#### <a name="fastqc"></a>2. FastQC
* `--fastqc`
  * Run FastQC in the default mode on the FastQ file once trimming is complete.
* `--fastqc_args "<ARGS>"`
  * Passes extra arguments to FastQC. If more than one argument is to be passed to FastQC they must be in the form `arg1 arg2 [..]`.
  * An example would be: `--fastqc_args "--nogroup --outdir /home/"`.
  * Passing extra arguments will automatically invoke FastQC, so `--fastqc` does not have to be specified separately.

#### <a name="adapter"></a>3. Adapter
* `--adapter <STRING>`
  * Adapter sequence to be trimmed. If not specified explicitly, Trim Galore will try to auto-detect whether the Illumina universal, Nextera transposase or Illumina small RNA adapter sequence was used. Also see `--illumina`, `--nextera` and `--small_rna`.
  * If no adapter can be detected within the first 1 million sequences of the first file specified Trim Galore defaults to `--illumina`.
* `--adapter2 <STRING>`
  * Optional adapter sequence to be trimmed off read 2 of paired-end files.
  * This option requires `--paired` to be specified as well.
* `--illumina`
  * Adapter sequence to be trimmed is the first 13bp of the Illumina universal adapter `AGATCGGAAGAGC` instead of the default auto-detection of adapter sequence.
* `--nextera`
  * Adapter sequence to be trimmed is the first 12bp of the Nextera adapter `CTGTCTCTTATA` instead of the default auto-detection of adapter sequence.
* `--small_rna`
  * Adapter sequence to be trimmed is the first 12bp of the _Illumina Small RNA 3' Adapter_ `TGGAATTCTCGG` instead of the default auto-detection of adapter sequence.
  * Selecting to trim smallRNA adapters will also lower the `--length` value to 18bp. If the smallRNA libraries are paired-end then `-a2` will be set to the Illumina small RNA 5' adapter automatically (`GATCGTCGGACT`) unless `-a 2` had been defined explicitly.
* `--max_length <INT>`
  * Discard reads that are longer than <INT> bp after trimming. This is only advised for smallRNA sequencing to remove non-small RNA sequences.
* `--length <INT>`
  * Discard reads that became shorter than length INT because of either quality or adapter trimming. A value of `0` effectively disables this behaviour.
  * Default: `20 bp`.
  * For paired-end files, both reads of a read-pair need to be longer than <INT> bp to be printed out to validated paired-end files (see option `--paired`). If only one read became too short there is the possibility of keeping such unpaired single-end reads (see `--retain_unpaired`).
  * Default pair-cutoff: `20 bp`.

##### <a name="reduce-random-matches"></a>Reduce random matches
* `--stringency <INT>`
  * Overlap with adapter sequence required to trim a sequence.
  * Defaults to a very stringent setting of `1`, _i.e._ even a single base pair of overlapping sequence will be trimmed of the 3' end of any read.
* `-e <ERROR RATE>`
  * Maximum allowed error rate (no. of errors divided by the length of the matching region)
  * Default: `0.1`

#### <a name="ns"></a>4. Ns
* `--max_n COUNT`
  * The total number of `Ns` (as integer) a read may contain before it will be removed altogether.
  * In a paired-end setting, either read exceeding this limit will result in the entire pair being removed from the trimmed output files.
* `--trim-n`
  * Removes `Ns` from either side of the read.
  * This option does currently not work in RRBS mode.

#### <a name="output"></a>5. Output
* `--output_dir <DIR>`
  * If specified all output will be written to this directory instead of the current directory.
* `--no_report_file`
  * If specified no report file will be generated.
* `--suppress_warn`
  * If specified any output to `STDOUT` or `STDERR` will be suppressed.
* `--gzip`
  * Compress the output file with `gzip`.
  * If the input files are gzip-compressed the output files will be automatically gzip compressed as well.
* `--dont_gzip`
  * Output files won't be compressed with gzip. This overrides `--gzip`.

#### <a name="clip"></a>6. Clip bases defined by user
* `--clip_R1 <int>`
  * Instructs Trim Galore to remove <int> bp from the 5' end of read 1 (or single-end reads). This may be useful if the qualities were very poor, or if there is some sort of unwanted bias at the 5' end.
  * Default: `OFF`
* `--clip_R2 <int>	`
  * Instructs Trim Galore to remove <int> bp from the 5' end of read 2 (paired-end reads only). This may be useful if the qualities were very poor, or if there is some sort of unwanted bias at the 5' end.
  * For paired-end BS-Seq, it is recommended to remove the first few bp because the end-repair reaction may introduce a bias towards low methylation. Please refer to the M-bias plot section in the Bismark User Guide for some examples.
  * Default: `OFF`
* `--three_prime_clip_R1 <int>`
  * Instructs Trim Galore to remove `<int>` bp from the 3' end of read 1 (or single-end reads) _AFTER_ adapter/quality trimming has been performed. This may remove some unwanted bias from the 3' end that is not directly related to adapter sequence or basecall quality.
  * Default: `OFF`
* `--three_prime_clip_R2 <int>`
  * Instructs Trim Galore to re move `<int>` bp from the 3' end of read 2 _AFTER_ adapter/quality trimming has been performed. This may remove some unwanted bias from the 3' end that is not directly related to adapter sequence or basecall quality.
  * Default: `OFF`

#### <a name="rrbs-specific-options"></a>RRBS-specific options (MspI digested material):
* `--rrbs`
  * Specifies that the input file was an MspI digested RRBS sample (recognition site: `CCGG`). Sequences which were adapter-trimmed will have a further 2 bp removed from their 3' end. This is to avoid that the filled-in C close to the second MspI site in a sequence is used for methylation calls. Sequences which were merely trimmed because of poor quality will not be shortened further.
* `--non_directional`
  * Selecting this option for non-directional RRBS libraries will screen quality-trimmed sequences for `CAA` or `CGA` at the start of the read and, if found, removes the first two base pairs. Like with the option `--rrbs` this avoids using cytosine positions that were filled-in during the end-repair step. `--non_directional` requires `--rrbs` to be specified as well.
* `--keep`
  * Keep the quality trimmed intermediate file. If not specified the temporary file will be deleted after adapter trimming. Only has an effect for RRBS samples since other FastQ files are not trimmed for poor qualities separately.
  * Default: `OFF`

##### Note for RRBS using MseI:
If your DNA material was digested with MseI (recognition motif: TTAA) instead of MspI it is _NOT_ necessary to specify `--rrbs` or `--non_directional` since virtually all reads should start with the sequence `TAA`, and this holds true for both directional and non-directional libraries. As the end-repair of `TAA` restricted sites does not involve any cytosines it does not need to be treated especially. Instead, simply run Trim Galore! in the standard, i.e. non-RRBS, mode.


#### <a name="paired-end"></a>Paired-end specific options:
* `--paired`
  * This option performs length trimming of quality/adapter/RRBS trimmed reads for paired-end files. To pass the validation test, both sequences of a sequence pair are required to have a certain minimum length which is governed by the option `--length` (see above). If only one read passes this length threshold the other read can be rescued (see option `--retain_unpaired`).
  * Using this option lets you discard too short read pairs without disturbing the sequence-by-sequence order of FastQ files which is required by many aligners.
  Trim Galore! expects paired-end files to be supplied in a pairwise fashion, e.g. `file1_1.fq` `file1_2.fq` `SRR2_1.fq.gz` `SRR2_2.fq.gz` `...` .
* `--trim1`
  * Trims 1 bp off every read from its 3' end.
  * This may be needed for FastQ files that are to be aligned as paired-end data with Bowtie 1. This is because Bowtie (1) regards alignments like this as invalid (whenever a start/end coordinate is contained within the other read):
```bash
R1 --------------------------->
R2 <---------------------------
# or this:
R1 ----------------------->
R2       <-----------------
```
* `--retain_unpaired`
  * If only one of the two paired-end reads became too short, the longer read will be written to either `.unpaired_1.fq` or `.unpaired_2.fq` output files. The length cutoff for unpaired single-end reads is governed by the parameters `-r1`/`--length_1` and `-r2`/`--length_2`.
  * Default: `OFF`.
* `--length_1 <INT>`
  * Unpaired single-end read length cutoff needed for read 1 to be written to `.unpaired_1.fq` output file. These reads may be mapped in single-end mode.
  * Default: `35 bp`
* `--length_2 <INT>`
  * Unpaired single-end read length cutoff needed for read 2 to be written to `.unpaired_2.fq` output file. These reads may be mapped in single-end mode.
  * Default: `35 bp`
  
### <a name="example"></a>Example:

```
qualchk +T template/1.QualChk.md +p "--paired" +t 2 +q "--quality 0 --phred33" +o "--output_dir _02_QC" +i "_01_rawData/SM1/SM1_lib1_lane1_R1.fq.gz _01_rawData/SM1/SM1_lib1_lane1_R2.fq.gz"
```

Here, we use the paired-end  mode by `+p "--paired"`; no quality restriction and use *ASCII+33* quality scores by `+q "--quality 0 --phred33"`; and output files to *_02_QC* by `+o "--output_dir _02_QC"`. For the final report, wo use the pre-defined template: `+T template/1.QualChk.md`   
**REPORT:** [link]()
