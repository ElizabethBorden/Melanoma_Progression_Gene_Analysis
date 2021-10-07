# Melanoma_Progression_Gene_Analysis

## RNA sequencing processing and read count quantification:
  1. FastQC quality control:
      - program: fastqc.snakefile.py
  3. Trimming and repeat FastQC:
      - program: fastqc_trimmomatic.snakefile.py
  5. Read mapping to a sex-specific reference genome and read count quantification with salmon: 
      - program: salmon.snakefile

* All programs run in a conda environment for version control. Conda environment can be recreated with fastqc_environment.yml 

* Sex-specific reference genomes created with the GENCODE GRCH38 genome by hard masking the y-chromosome for the female-specific reference genome and hard masking the pseudoautosomal regions of the y-chromosome for the male-specific genome

## Data analysis:
  1. Differential expression analysis, visualization, and regularized regression models:
      - program: Differential_Expression_Krueger_Bastian_Scatolini.Rmd
  3. Association of genes with progression of melanoma
      - program: Scatolini_progression_of_genes.Rmd

* Gene lists were harmonized using David Web Services to convert all probe names from the Krueger and Scatolini datasets into official gene symbols
