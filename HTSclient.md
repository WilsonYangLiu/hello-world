# HTSclient

HTSclient is the pipeline processing high-throughput sequencing data. Currently, it support DNA-seq analysis with various options. The RNA-seq, ChIP-seq, et al. will be added in future.

Here the DNA-seq workflow:  
![HTSclient workflow - DNA-seq](src/DNA-seq_workfolw.png)

## Table of contents

1. [Quick start](#quick-start)
2. [Installation](#installation)
3. [Reference genome and annotations](#reference-genome-and-annotations)
4. [Usage](#usage)
	* [index](#htsclient-index)
	* [align](#htsclient-align)
	* [markdup](#htsclient-markdup)
	* [merge](#htsclient-merge)
	* [var](#htsclient-var)
	* [SV](#htsclient-sv)
	* [VEP](#htsclient-vep)
5. [Example workflows](#example-workflows)

## Quick start

1. Install  
[BUIDING]...

2. Run the [example script](example/example_code.sh)  
	```
	cd example
	./example_code.sh
	```
	
	This should produce the following files:  
	* ID1.germline/*
	* ID1.germline.vcf_stats.txt
	* ID1.somatic_indel/*
	* ID1.somatic_snp/*
	* ID1.somatic_stats.txt
	* SM1/*
	* SM1.realign.bai
	* SM1.realign.bam
	* SM1_lib1/*
	* SM1_lib1.markdup.bai
	* SM1_lib1.markdup.bam

## Installation

#### Prerequisites

* g++ and the standard C and C++ development libraries (https://gcc.gnu.org/)
* CMake (http://www.cmake.org/)
* GNU awk and core utils
* JRE (http://www.oracle.com/technetwork/java/javase/downloads/index.html)
* ROOT (https://root.cern.ch/) (required if running CNVnator)
* Variant Effect Predictor (http://www.ensembl.org/info/docs/tools/vep/index.html) (required if annotating VCF files)

#### Configuration

System paths to HTSclient's component software are specified in the [HTSclient.config](HTSclient.config) file, which should reside in the same directory as the HTSclient executable

#### Install core components

* BWA (http://bio-bwa.sourceforge.net/)
* Samtools (http://www.htslib.org)
* Picard (http://broadinstitute.github.io/picard/)
* VarScan2 (http://dkoboldt.github.io/varscan/)
* Delly (https://github.com/dellytools/delly)
* Vawk (https://github.com/cc2qe/vawk)

#### Install optional components

* GATK (https://software.broadinstitute.org/gatk/)
* Variant Effect Predictor (http://www.ensembl.org/info/docs/tools/vep/index.html)
* CNVnator (https://github.com/abyzovlab/CNVnator)

#### Install HTSclient

[BUIDING]...

## Reference genome and annotations

#### Reference genome

1. 1000genomes:  
ftp://ftp-trace.ncbi.nih.gov/1000genomes/ftp/technical/reference/human_g1k_v37.fasta.gz  
ftp://ftp-trace.ncbi.nih.gov/1000genomes/ftp/technical/reference/human_g1k_v37.fasta.fai

2. Ensembl GRCh37:  
ftp://ftp.ensembl.org/pub/release-75/fasta/homo_sapiens/dna/Homo_sapiens.GRCh37.75.dna.primary_assembly.fa.gz

The genome FASTA file should be unzipped and indexed

#### Annotations

For human genome alignment using the GRCh37 build, here i recommend the following files:  
ftp://ftp.ensembl.org/pub/release-75/variation/VEP/homo_sapiens_refseq_vep_75.tar.gz  
ftp.broadinstitute.org/bundle/bundle/b37/Broad.human.exome.b37.interval_list.gz  
ftp.broadinstitute.org/bundle/bundle/b37/Mills_and_1000G_gold_standard.indels.b37.vcf.gz
ftp.broadinstitute.org/bundle/bundle/b37/dbsnp_138.b37.vcf.gz

In addition, the [speedseq](https://github.com/hall-lab/speedseq#reference-genome-and-annotations) repo introduced the following files:  
[ceph18.b37.exclude.2014-01-15.bed](annotation/ceph18.b37.exclude.2014-01-15.bed)  
[ceph18.b37.include.2014-01-15.bed](annotation/ceph18.b37.include.2014-01-15.bed)

In the [`HTSclient SV`](#htsclient-sv) module, [delly](https://github.com/dellytools/delly) recommend excluding the telomere and centromere genomic regions:  
[BUIDING]

## Usage

HTSclient is a modular framework with the following components:  
* [index](#htsclient-index) - create index file for reference fasta file
* [align](#htsclient-align) - align FASTQ files with BWA-MEM
* [markdup](#htsclient-markdup) - merge lane level bam files, mark duplication and produce the merged file (library level)
* [merge](#htsclient-merge) - merge library level bam files for distribution
* [var](#htsclient-var) - call snp/indel and CNV (WES only) variants with VarScan 2
* [SV](#htsclient-sv) - call SV (DUP|DEL|INV|TRA|INS) variants with delly
* [VEP](#htsclient-vep) - annotation with VEP

These modules operate independently of each other and produce universal output formats that are compatible with external tools. HTSclient modules can also run on BAM alignments that were produced outside of the framework.

```
USAGE: HTSclient <command> [options]

pre-process command:
   index   Create index file for reference fasta file
   align   align FASTQ files with BWA-MEM
   markdup merge lane level bam files, mark duplication and produce the merged file (library level)
   merge   merge library level bam files for distribution

call variants command:
   var     call snp/indel and CNV (WES only) variants with VarScan 2
   SV      call SV (DUP|DEL|INV|TRA|INS) variants with delly

annotation command:
   VEP     annotation with VEP

options:
   -h      show this message
```

### HTSclient index

```
USAGE: HTSclient index [options] <ref_fa> <ref_dict>

positional args:
   ref_fa   reference fasta file
   ref_dict name of sequence dictionary of reference fasta file

bwa index options:
   -a STR   BWT construction algorithm: bwtsw, is or rb2 [is]
   -f       force overwrite

global options:
   -v       verbose
   -j STR   java argument, which should be quoted. [\"-Xmx2g\"]
   -h       show this message
```

### HTSclient align

```
USAGE: HTSclient align [options] <ref_fa> <in1.fq> [<in2.fq>]

positional args:
   ref_fa   reference fasta file
   in1.fq   paired-end fastq file. if -p flag is used then expected to be
             an interleaved paired-end fastq file, and in2.fq may be omitted.
             (can be gzipped)
   in2.fq   paired-end fastq file. (can be gzipped)

alignment options:
   -o STR   output prefix [lane]
   -R STR   read group header line. (required) [\"RGID:RGPL:RGPU:RGLB:RGSM\"]
   -p       first fastq file consists of interleaved paired-end sequences
   -t INT   threads [2]
   -T DIR   temp directory [./output_prefix.XXXXXXXXXXXX]

indel realignment options:
   -I STR   input VCF file(s) with known indels. (required if enable indel realignment)

base quality scores recalibration
   -D STR   a database of known polymorphic sites, e.g. dbSNP. (required if enable BQSR)
   -L STR   one or more genomic intervals over which to operate.

global options:
   -v       verbose
   -j STR   java argument, which should be quoted. [\"-Xmx2g\"]
   -h       show this message
```

### HTSclient markdup

```
USAGE: HTSclient markdup [options] <bam_list>

positional args:
   bam_list lane level bam file list, seperated by comma 

options:
   -o STR   output prefix [lib]
   -s SRT   assume sorted by coodinate (true|false) [true]
   -v       verbose
   -j STR   java argument, which should be quoted. [\"-Xmx2g\"]
   -h       show this message
```

### HTSclient merge

```
USAGE: HTSclient merge [options] <bam_list>

positional args:
   bam_list library level bam file list, seperated by comma 

merge options:
   -o STR   output prefix [SM]

indel realignment options:
   -f STR   reference fasta file
   -I STR   input VCF file(s) with known indels (required if enable indel realignment)

global options:
   -v       verbose
   -j STR   java argument, which should be quoted. [\"-Xmx2g\"]
   -h       show this message
```

### HTSclient var

```
USAGE: HTSclient var [options] <tumor_list> [<normal_list>]

positional args:
   tumor_list   sample level bam file tumor list, seperated by comma
   normal_list  sample level bam file normal list, seperated by comma 

required options:
   -T STR   analysis type (germline|somatic|CNV). [germline]
              germline: germline analysis
              somatic: somatic analysis
              CNV: (WES only)(! Not implement yet) copy number variant analysis.
   
options:
   -f STR   reference fasta file (required)
   -m STR   mpileup arguments, which should be quoted, e.g. \"-f ref_fa\"
   -g STR   basic VarScan arguments, seperated by colon. [\"8:15:0.08:0.75:0.95\"]
              format: \"Min coverage\":\"Min base qual\":\"Min var freq\":\"Min freq for hom\":\"p-val\"

 For somatic:
   -s STR   VarScan arguments for somatic, seperated by colon. [\"8:6:0.95:0.05\"]
              format: \"Min normal coverage\":\"Min tumor coverage\":\"p-val for heterozygote\":\"p-val for somatic\". 
   -p STR   this options used for isolate Germline/LOH/Somatic calls from output (indel OR snp)
              arguments seperated by colon. [\"0.10:0.05:0.07\"]
              format: \"Min freq in tumor\":\"Mam freq in normal\":\"p-val for HC\".

 For CNV:
   Not implement yet

global options:
   -t INT   Enable forking, using the specified number of forks. [1]
   -a       annotation flag, default to not annotate
   -o STR   output prefix [SM]
   -v       verbose
   -j STR   java argument, which should be quoted. [\"-Xmx2g\"]
   -h       show this message
```

### HTSclient SV

```
USAGE: HTSclient SV [options] <ref_fa> <bam_list> [<control_list>]

positional args:
   ref_fa       reference fasta file (required)
   bam_list     library level sorted bam file list, seperated by comma
   control_list somatic analysis type only, seperated by comma. if analysis type is germline, 
                  this arguments would be omitted.
                  NOTE that each bam file in control_list should have its matched bam file in bam_list.
                  the matched tumor-control pair share the same position in both list

generic options:
   -o STR   output prefix. If you need vcf output, use \`bcftools view' for file conversion [ID]
   -T STR   analysis type (germline|somatic). [germline]
   -t STR   SV type (DEL|DUP|INV|BND|INS) [DEL]
   -x STR   file with regions (such as centromere and telomere) to exclude.
   -D STR   discovery options, seperated by colon. [1:9]
              format: \"min. paired-end mapping qual\":\"insert size cutoff\"
   -u INT   min. mapping quality for genotyping. [5]

somatic options:
   -s SRT   a tab-delimited sample description file where the first column is the sample id 
              (as in the VCF/BCF file) and the second column is either tumor or control

merge options:
   -M STR   delly merge options, seperated by colon. [\"500:1000000:500:0.5\"]
              format: \"min. SV size\":\"max. SV size\":\"max. breakpoint offset\":\"min. reciprocal overlap\"
   -B STR   bcftools merge arguments, which should be quoted, e.g. \"-0\"

global options:
   -f       apply SV filter
   -v       verbose
   -h       show this message
```

### HTSclient VEP

```
USAGE: HTSclient VEP [options] <in_file> <out_file>

positional args:
   in_file   Raw input data
   out_file  Output file name [STDOUT]

options:
   -t INT    Enable forking, using the specified number of forks. [1]
   -s STR    Species for your data [homo_sapiens]
   -a STR    Select the assembly version to use if more than one available [GRCh37]
   -I STR    Other input options, must be quoted. [\"--force_overwrite --stats_text\"]
               --force_overwrite: force the overwrite of the existing file
               --stats_text: generate a plain text stats file in place of the HTML
               other options please see the VEP website
   -d STR    Specify the base cache/plugin directory to use. [\"\$HOME/.vep/\"]
   -C STR    Other cache options, must be quoted. [\"--cache --offline --merged\"]
               --cache: enables use of the cache
               --offline: enable offline mode
               --merged: use the merged Ensembl and RefSeq cache.
               other options please see the VEP website
   -T STR    Output annotation term options, must be quoted. 
               [\"--sift b --polyphen b --symbol --numbers --biotype --total_length\"[ | \"--everything\"]]
               other options please see the VEP website
   -L STR    Co-located variants options, must be quoted. [\"--check_existing\"]
               --check_existing: checks for the existence of known variants that are co-located with your input
               other options please see the VEP website
   -f [0|1|STR]
             Configure the output format. 0 for disable this option; 1 for enable; and STR for customize output. [0]
               Note that if you ues SRT, the term should already be contained in \"-T STR\" and \"-L STR\"

global options:
   -v        verbose
   -h        show this message
```
