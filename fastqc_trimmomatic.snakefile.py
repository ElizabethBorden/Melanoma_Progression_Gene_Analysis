# Workflow for FastQC, MultiQC, and adapter trimming using Trimmomatic.
from os.path import join
configfile: "bastian_melanoma.config.json"

# Directory variables
fastq_directory = "/data/CEM/buetowlab/controlled_access/dbGaP/proj_SRR6795478/fastqs/files/"
trimmed_fastqs = "/scratch/eknodel/bastian_melanoma/trimmed_fastqs/"
trimmed_fastqc_directory = "/scratch/eknodel/bastian_melanoma/trimmed_fastq_fastqc/" 
# Tools
fastqc_path = "fastqc"
multiqc_path = "multiqc"
trimmomatic_path = "trimmomatic"
PERL5LIB="/home/eknodel/miniconda3/envs/fastqc_environment/lib/perl5/5.22.0/"

SAMPLES = config["all_samples"]

ruleorder: fastqc_analysis_trimmomatic_trimmed_paired > multiqc_trimmed_paired

rule all:
    input:
        expand(trimmed_fastqs + "{sample}_trimmomatic_trimmed_paired_1.fastq", trimmed_fastqs=trimmed_fastqs, sample=SAMPLES),
        expand(trimmed_fastqs + "{sample}_trimmomatic_trimmed_paired_2.fastq", trimmed_fastqs=trimmed_fastqs, sample=SAMPLES),
        expand(trimmed_fastqs + "{sample}_trimmomatic_trimmed_unpaired_1.fastq", trimmed_fastqs=trimmed_fastqs, sample=SAMPLES),
        expand(trimmed_fastqs + "{sample}_trimmomatic_trimmed_unpaired_2.fastq", trimmed_fastqs=trimmed_fastqs, sample=SAMPLES),
        expand(trimmed_fastqs + "{sample}_trimmomatic.log", trimmed_fastqs=trimmed_fastqs, sample=SAMPLES),
        expand(trimmed_fastqc_directory + "{sample}_trimmomatic_trimmed_paired_1_fastqc.html", sample=SAMPLES),
        expand(trimmed_fastqc_directory + "{sample}_trimmomatic_trimmed_paired_2_fastqc.html", sample=SAMPLES),
        os.path.join(trimmed_fastqc_directory, "multiqc_report.html")

rule trimmomatic:
    input:
        fq1 = os.path.join(fastq_directory, "{sample}_1.fastq"),
        fq2 = os.path.join(fastq_directory, "{sample}_2.fastq"),
        ADAPTER_FASTA = "adapter_sequences.fa"
    output:
        paired_1 =   os.path.join(trimmed_fastqs,"{sample}_trimmomatic_trimmed_paired_1.fastq"),
        unpaired_1 = os.path.join(trimmed_fastqs,"{sample}_trimmomatic_trimmed_unpaired_1.fastq"),
        paired_2 =   os.path.join(trimmed_fastqs,"{sample}_trimmomatic_trimmed_paired_2.fastq"),
        unpaired_2 = os.path.join(trimmed_fastqs,"{sample}_trimmomatic_trimmed_unpaired_2.fastq"),    
        logfile =    os.path.join(trimmed_fastqs,"{sample}_trimmomatic.log")
    params:
        trimmomatic = trimmomatic_path,
        threads = 4,
        seed_mismatches = 2,
        palindrome_clip_threshold = 30,
        simple_clip_threshold = 10,
        leading = 10,
        trailing = 10,
        winsize = 4,
        winqual = 15,
        minlen = 50
    shell:
        """
        {params.trimmomatic} PE -threads {params.threads} -phred33 -trimlog {output.logfile} \
        {input.fq1} {input.fq2} {output.paired_1} {output.unpaired_1} \
        {output.paired_2} {output.unpaired_2} \
        ILLUMINACLIP:{input.ADAPTER_FASTA}:{params.seed_mismatches}:{params.palindrome_clip_threshold}:{params.simple_clip_threshold} \
        LEADING:{params.leading} TRAILING:{params.trailing} \
        SLIDINGWINDOW:{params.winsize}:{params.winqual} MINLEN:{params.minlen}
        """

rule fastqc_analysis_trimmomatic_trimmed_paired:
    input:
        fq1 = os.path.join(trimmed_fastqs , "{sample}_trimmomatic_trimmed_paired_1.fastq"),
        fq2 = os.path.join(trimmed_fastqs , "{sample}_trimmomatic_trimmed_paired_2.fastq")
    output:
        html1 = os.path.join(trimmed_fastqc_directory, "{sample}_trimmomatic_trimmed_paired_1_fastqc.html"),
        html2 = os.path.join(trimmed_fastqc_directory, "{sample}_trimmomatic_trimmed_paired_2_fastqc.html")
    params:
        fastqc = fastqc_path,
        fastqc_dir = trimmed_fastqc_directory
    shell:
        """
        PERL5LIB="/home/eknodel/miniconda3/envs/fastqc_environment/lib/perl5/5.22.0/" {params.fastqc} -o {params.fastqc_dir} {input.fq1} {input.fq2}
        """


rule multiqc_trimmed_paired:
    input:
    output:
        os.path.join(trimmed_fastqc_directory, "multiqc_report.html"),
        os.path.join(trimmed_fastqc_directory, "multiqc_data")
    message: "Running MultiQC for post-trimming FastQC reports located in {params.fastqc_dir}"
    params:
        fastqc_dir = trimmed_fastqc_directory,
        output_dir = trimmed_fastqc_directory
    shell:
        """
        multiqc {params.fastqc_dir} --outdir {params.output_dir} --interactive --verbose
        """
