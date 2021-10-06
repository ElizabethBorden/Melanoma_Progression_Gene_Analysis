# Melanoma_Progression_Gene_Analysis

RNA sequencing data from Bastian dataset processed by
  1. FastQC quality control:
      - program: fastqc.snakefile.py
  3. Trimming and repeat FastQC:
      - program: fastqc_trimmomatic.snakefile.py
  5. Read mapping to a sex-specific reference genome and read count quantification with salmon: 
      - program: salmon.snakefile

All programs run in a conda environment for version control. Conda environment can be recreated with fastqc_environment.yml 

Sex-specific reference genomes created with the GENCODE GRCH38 genome by hard masking the y-chromosome for the female-specific reference genome and hard masking the pseudoautosomal regions of the y-chromosome for the male-specific genome

