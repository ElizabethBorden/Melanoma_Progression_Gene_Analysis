#! importing join
from os.path import join

# Workflow for quasi-quantification of RNAseq read counts with Salmon in non-alignment-based mode.

# Configuration file
configfile: "bastian_melanoma.config.json"

# Tools
SALMON = "salmon"

# Reference genome files: XX with Y chromosome masked, XY with both Y-chromosomal PAR masked
SALMON_INDEX_XX = "/data/CEM/shared/public_data/references/GENCODE/gencode_salmon_index_XXonly/"
SALMON_INDEX_XY = "/data/CEM/shared/public_data/references/GENCODE/gencode_salmon_index_XY/"

# Directories
FQ_DIR = "/data/CEM/buetowlab/controlled_access/dbGaP/proj_SRR6795478/trimmed_fastqs/"
SALMON_DIR = "/data/CEM/buetowlab/controlled_access/dbGaP/proj_SRR6795478/salmon_quants/"

# Samples
XX_SAMPLES = config["female"]
XY_SAMPLES= config["male"]
SAMPLES = config["all_samples"]

rule all:
    input:
        # Defining the files that snakemake will attempt to produce as an output.
        # If there is no rule defined to produce the file, or if the file already
        # exists, snakemake will throw "Nothing to be done"
        expand(SALMON_DIR + "{sample}_salmon_quant/", SALMON_DIR=SALMON_DIR, sample=SAMPLES),

rule salmon_quant_paired:
    input:
        R1 = os.path.join(FQ_DIR, "{sample}_trimmomatic_trimmed_paired_1.fastq"),
        R2 = os.path.join(FQ_DIR, "{sample}_trimmomatic_trimmed_paired_2.fastq")
    output:
        OUTPUT = os.path.join(SALMON_DIR, "{sample}_salmon_quant/"),
    params:
        SALMON = SALMON,
        SALMON_INDEX_XX = SALMON_INDEX_XX,
        SALMON_INDEX_XY = SALMON_INDEX_XY,
        LIBTYPE = "A", # LIBTYPE A for automatic detection of library type
        threads = 8
    message: "Quantifying {wildcards.sample} transcripts with Salmon."
    run:
        if "{wildcards.sample}" in XX_SAMPLES: 
            shell("{params.SALMON} quant -i {params.SALMON_INDEX_XX} --validateMappings -l {params.LIBTYPE} -1 {input.R1} -2 {input.R2} -o {output.OUTPUT}")
        else:
            shell("{params.SALMON} quant -i {params.SALMON_INDEX_XY} --validateMappings -l {params.LIBTYPE} -1 {input.R1} -2 {input.R2} -o {output.OUTPUT}")

