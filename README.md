# Melanoma_Progression_Gene_Analysis

RNA sequencing data from Bastian dataset processed by
  1. FastQC quality control: fastqc.snakefile.py
  2. Trimming and repeat FastQC: fastqc_trimmomatic.snakefile.py
  3. Read mapping to a sex-specific reference genome and read count quantification with salmon: salmon.snakefile

Sex-specific reference genomes created with the GENCODE GRCH38 genome by hard masking the y-chromosome for the female-specific reference genome and hard masking the pseudoautosomal regions of the y-chromosome for the male-specific genome

