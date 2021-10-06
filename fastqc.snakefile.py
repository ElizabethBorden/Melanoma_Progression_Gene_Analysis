# Workflow for FastQC, MultiQC, and adapter trimming using Trimmomatic.
from os.path import join
configfile: "bastian_melanoma.config.json"

# Directory variables
fastq_directory = "/data/CEM/buetowlab/controlled_access/dbGaP/proj_SRR6795478/fastqs/files/"
fastqc_directory = "/scratch/eknodel/bastian_melanoma/fastqc/"

# Tools
fastqc_path = "fastqc"
multiqc_path = "multiqc"
PERL5LIB="/home/eknodel/miniconda3/envs/fastqc_environment/lib/perl5/5.22.0/"

SAMPLES = config["all_samples"]

ruleorder: fastqc > multiqc

rule all:
    input:
        expand(fastqc_directory + "{sample}_1_fastqc.html", fastqc_directory=fastqc_directory, sample=SAMPLES),
        expand(fastqc_directory + "{sample}_2_fastqc.html", fastqc_directory=fastqc_directory, sample=SAMPLES),
        os.path.join(fastqc_directory, "multiqc_report.html")

rule fastqc:
    input:
        fq1 = os.path.join(fastq_directory , "{sample}_1.fastq"),
        fq2 = os.path.join(fastq_directory , "{sample}_2.fastq")
    output:
        html1 = os.path.join(fastqc_directory, "{sample}_1_fastqc.html"),
        html2 = os.path.join(fastqc_directory, "{sample}_2_fastqc.html")
    params:
        fastqc = fastqc_path,
        fastqc_dir = fastqc_directory
    shell:
        """
        PERL5LIB="/home/eknodel/miniconda3/envs/fastqc_environment/lib/perl5/5.22.0/" {params.fastqc} -o {params.fastqc_dir} {input.fq1} {input.fq2}
        """


rule multiqc:
    input:
    output:
        os.path.join(fastqc_directory, "multiqc_report.html"),
        os.path.join(fastqc_directory, "multiqc_data")
    message: "Running MultiQC for post-trimming FastQC reports located in {params.fastqc_dir}"
    params:
        fastqc_dir = fastqc_directory,
        output_dir = fastqc_directory
    shell:
        """
        multiqc {params.fastqc_dir} --outdir {params.output_dir} --interactive --verbose
        """
