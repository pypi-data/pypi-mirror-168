#!/usr/bin/env python
__author__ = ('Aitor Blanco Miguez (aitor.blancomiguez@unitn.it), '
              'Duy Tin Truong (duytin.truong@unitn.it), '
              'Francesco Asnicar (f.asnicar@unitn.it), '
              'Moreno Zolfo (moreno.zolfo@unitn.it), '
              'Francesco Beghini (francesco.beghini@unitn.it)')
__version__ = '4.0.2'
__date__ = '22 Sep 2022'

import sys
try:
    from .util_fun import error
except ImportError:
    from util_fun import error

if sys.version_info[0] < 3:
    error("StrainPhlAn 3.0 requires Python 3, your current Python version is {}.{}.{}"
                    .format(sys.version_info[0], sys.version_info[1], 
                        sys.version_info[2]), exit=True)

import os, time, shutil, pickle, tempfile, bz2
import subprocess as sb
import argparse as ap
from cmseq import cmseq
try:
    from .external_exec import samtools_sam_to_bam, samtools_sort_bam_v1, decompress_bz2
    from .util_fun import info, optimized_dump, get_breath
    from .parallelisation import execute_pool
except ImportError:
    from external_exec import samtools_sam_to_bam, samtools_sort_bam_v1, decompress_bz2
    from util_fun import info, optimized_dump, get_breath
    from parallelisation import execute_pool

metaphlan_script_install_folder = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_FOLDER = os.path.join(metaphlan_script_install_folder, '..', "metaphlan_databases")
DEFAULT_DB_FOLDER = os.environ.get('METAPHLAN_DB_DIR', DEFAULT_DB_FOLDER)
DEFAULT_DB_NAME =  "mpa_vJan21_CHOCOPhlAnSGB_202103.pkl"
DEFAULT_DATABASE = os.path.join(DEFAULT_DB_FOLDER, DEFAULT_DB_NAME)

class SAMPLE2MARKERS_DEFAULTS:
    breadth_threshold = 80
    min_reads_aligning = 8

"""
Reads and parses the command line arguments of the script.

:returns: the parsed arguments
"""
def read_params():
    p = ap.ArgumentParser(description="", formatter_class=ap.ArgumentDefaultsHelpFormatter)
    p.add_argument('-i', '--input', type=str, 
                   nargs='+', default=[],
                   help="The input samples as SAM or BAM files")
    p.add_argument('--sorted', action='store_true', default=False,
                   help="Whether the BAM input files are sorted")
    p.add_argument('-f', '--input_format', type=str, default="bz2",
                   help="The input samples format {bam, sam, bz2}")
    p.add_argument('-o', '--output_dir', type=str, default=None,
                   help="The output directory")
    p.add_argument('-d', '--database', type=str, default=DEFAULT_DATABASE,
                   help="The input MetaPhlAn " + __version__ + " database")
    p.add_argument('-b', '--breadth_threshold', type=int, default=SAMPLE2MARKERS_DEFAULTS.breadth_threshold,
                   help="The breadth of coverage threshold for the consensus markers")
    p.add_argument('--min_reads_aligning', type=int, default=SAMPLE2MARKERS_DEFAULTS.min_reads_aligning,
                   help="The minimum number of reads to cover a marker")
    p.add_argument('--min_read_len', type=int, default=cmseq.CMSEQ_DEFAULTS.minlen,
                   help="The minimum lenght for a read to be considered")
    p.add_argument('--min_base_coverage', type=int, default=cmseq.CMSEQ_DEFAULTS.mincov,
                   help="The minimum depth of coverage for a base to be considered")
    p.add_argument('--min_base_quality', type=int, default=cmseq.CMSEQ_DEFAULTS.minqual,
                   help="The minimum quality for a base to be considered. This is performed BEFORE --min_base_coverage")
    p.add_argument('--dominant_frq_threshold', type=float, default=cmseq.CMSEQ_DEFAULTS.poly_dominant_frq_thrsh,
                   help="The cutoff for degree of 'allele dominance' for a position to be considered polymorphic")         
    p.add_argument('--clades', type=str, nargs='+', default=[],
                   help="Restricts the reconstruction of the markers to the specified clades")          
    p.add_argument('--tmp', type=str, default=None,
                   help="If specified, the directory where to store the temporal files")
    p.add_argument('--debug', action='store_true', default=False,
                   help=("If specified, StrainPhlAn will not remove the temporal folder. Not available with inputs in BAM format"))
    p.add_argument('-n', '--nprocs', type=int, default=1,
                   help="The number of threads to execute the script")
    
    return p.parse_args()


"""
Checks the mandatory command line arguments of the script.

:param args: the arguments of the script
:returns: the checked args
"""
def check_params(args):
    if not args.input:
        error('-i (or --input) must be specified', exit=True, 
            init_new_line=True)
    elif not args.input_format:
        error('-f (or --input_format) must be specified', exit=True, 
            init_new_line=True)
    elif not args.output_dir:
        error('-o (or --output_dir) must be specified', exit=True, 
            init_new_line=True)
    elif args.input_format.lower() != "bam" and args.input_format.lower() != "sam" and args.input_format.lower() != "bz2":
        error('The input format must be SAM, BAM, or compressed in BZ2 format', 
            exit=True, init_new_line=True)
    elif args.input_format.lower() == "bam" and len(args.clades) > 0:
        error('The --clades option cannot be used with inputs in BAM format', 
            exit=True, init_new_line=True)
    elif not os.path.exists(args.output_dir):
        error('The directory {} does not exist'.format(args.output_dir), exit=True, 
            init_new_line=True)
    elif not (args.tmp is None) and not os.path.exists(args.tmp):
        error('The directory {} does not exist'.format(args.tmp), exit=True, 
            init_new_line=True)
    else:
        check_input_files(args.input, args.input_format)
    if not args.output_dir.endswith('/'):
        args.output_dir += '/'    
    return args


"""
Checks the input sample files

:param input: the input files
:param input_format: the format of the input files
"""
def check_input_files(input, input_format):
    for s in input:
        _, extension = os.path.splitext(s)
        if not os.path.exists(s):
            error('The input file \"'+s+'\" does not exist', exit=True, 
                init_new_line=True)
        elif not input_format.lower() == extension[1:].lower():
            error('The the input file \"'+s+'\" must be in \"'+
                input_format.upper()+'\" format',
                exit=True, init_new_line=True)
    return True


#ToDo: Check CMSeq and samtools
"""
Checks the mandatory programs to execute of the script.

"""
def check_dependencies():
    try:
        # sb.check_call(["samtools", "tview"], stdout=sb.DEVNULL, stderr=sb.DEVNULL)
        sb.check_call(["bzip2", "--help"], stdout=sb.DEVNULL, stderr=sb.DEVNULL)
    except Exception as e:
        error('Program not installed or not present in the system path\n'+str(e), 
            init_new_line=True, exit=True)


"""
Decompressed SAM.BZ2 files

:param input: the list of samples as BZ2 files
:param tmp_dir: the temporal output directory
:param nprocs: the number of threads to use
:returns: the list of decompressed files
"""
def decompress_from_bz2(input, tmp_dir, nprocs):
    decompressed = []
    decompressed_format = []
    results = execute_pool(((decompress_bz2_file, i, tmp_dir) for i in input), 
        nprocs)
    for r in results:
        decompressed.append(r[0])
        decompressed_format.append(r[1])   

    if decompressed_format[1:] == decompressed_format[:-1]:
        if decompressed_format[0][1:].lower() == "sam":
            return decompressed, "sam"
        elif decompressed_format[0][1:].lower() == "bam":
            return decompressed, "bam"
        else:
            error("Decompressed files are not in SAM or BAM format",
                exit=True, init_new_line=True)
    else:
        error("Decompressed files have different formats",
            exit=True, init_new_line=True)


"""
Decompress a BZ2 file and returns the decompressed file and the 
decompressed file format

:param input: the input BZ2 file
:param output_dir: the output directory
:returns: the decompressed file and the decompressed file format
"""
def decompress_bz2_file(input, output_dir):
    decompressed_file = decompress_bz2(input, output_dir)
    _, e = os.path.splitext(decompressed_file)
    return decompressed_file, e


"""
Convert input sample files to sorted BAMs

:param input: the samples as SAM or BAM files
:param sorted: whether the BAM files are sorted
:param input_format: format of the sample files [bam or sam]
:param tmp_dir: the temporal output directory
:param nprocs: number of threads to use in the execution
:returns: the new list of input BAM files
"""
def convert_inputs(input, sorted, input_format, tmp_dir, nprocs):
    if input_format.lower() == "bz2":
        info("Decompressing samples...\n", init_new_line=True)
        input, input_format = decompress_from_bz2(input, tmp_dir, nprocs)
        info("Done.")
    if input_format.lower() == "sam":
        info("Converting samples to BAM format...\n", init_new_line=True)
        input = execute_pool(((samtools_sam_to_bam, i, tmp_dir) for i in input), 
            nprocs)
        info("Done.")
        info("Sorting BAM samples...\n", init_new_line=True)
        input = execute_pool(((samtools_sort_bam_v1, i, tmp_dir) for i in input), 
            nprocs)
        info("Done.")
    elif sorted == False:        
        info("Sorting BAM samples...\n", init_new_line=True)
        input = execute_pool(((samtools_sort_bam_v1, i, tmp_dir) for i in input), 
            nprocs)
        info("Done.")
    
    return input


"""
Gets the markers for each sample and writes the Pickle files

:param input: the samples as sorted BAM files
:param output_dir: the output directory
:param breath_threshold: the breath threshold for the consensus markers
:param min_reads_aligning: the minimum number of reads to cover a marker
:param min_read_len: the minimum length for a read to be considered
:param min_base_coverage: the minimum coverage for a base to be considered
:param min_base_quality: the minimum quality for a base to be considered
:param dominant_frq_threshold: the cutoff for degree of 'allele dominance' for a position to be considered polymorphic
:param filtered: string to append to the end of the output file if the SAM input was filtered
:param nprocs: number of threads to use in the execution
"""
def execute_cmseq(input, output_dir, breath_threshold, min_reads_aligning, min_read_len, min_base_coverage, min_base_quality, dominant_frq_threshold, filtered, nprocs):
    info("Getting consensus markers from samples...", init_new_line=True)
    for i in input:
        info("\tProcessing sample: "+i, init_new_line=True)
        n, _ = os.path.splitext(os.path.basename(i))
        consensus = []
        collection = cmseq.BamFile(i, index=True, minlen=min_read_len, minimumReadsAligning=min_reads_aligning)
        results = collection.parallel_reference_free_consensus(ncores=nprocs, mincov=min_base_coverage, minqual=min_base_quality, consensus_rule=cmseq.BamContig.majority_rule_polymorphicLoci, dominant_frq_thrsh=dominant_frq_threshold)
        for c, seq in results:
            breath = get_breath(seq)
            if breath > breath_threshold:
                consensus.append({"marker":c, "breath":breath, "sequence":seq})
        markers_pkl = open(output_dir+n+'{}.pkl'.format(filtered), 'wb')
        optimized_dump(markers_pkl, consensus)
        info("\tDone.", init_new_line=True)
    info("Done.", init_new_line=True)
     
    
"""
Filters an input SAM file with the hits against markers of specific clades

:param input_fle: whether the BAM files are sorted
:param input_format: format of the sample files [bam or sam]
:param tmp_dir: the path where to store the tmp directory
:param filtered_markers: the list with the filtered markers
:return: the output filtered SAM file
"""
def parallel_filter_sam(input_file, input_format, tmp_dir, filtered_markers):
    output_file = tmp_dir + input_file.split('/')[-1]
    if input_format.lower() == "bz2":
        ifn = bz2.open(input_file, 'rt')
        output_file = output_file.replace('.bz2','')
    elif input_format.lower() == "sam":
        ifn = open(input_file, 'r')
    with open(output_file, 'w') as ofn:
        for line in ifn:
            s_line = line.strip().split('\t')
            if line.startswith('@'):        
                if line.startswith('@HD'):
                    ofn.write(line)
                elif s_line[1].split(':')[1] in filtered_markers:
                    ofn.write(line)        
            elif s_line[2] in filtered_markers:
                ofn.write(line)
    ifn.close()
    return output_file
   
    
"""
Filters the input SAM files with the hits against markers of specific clades

:param clades: the filtered set of clades to reconstruct the markers
:param database: the MetaPhlan markers database:param input: the samples as SAM or BAM files
:param input_format: format of the sample files [bam or sam]
:param tmp_dir: the path where to store the tmp directory
:param nprocs: number of threads to use in the execution
:returns: the filtered input files
"""
def filter_sam_files(clades, database, input, input_format, tmp_dir, nprocs):
    info('Loading MetaPhlAn '+ database.split('/')[-1][:-4] + ' database...', init_new_line=True)
    filtered_markers = list()
    db = pickle.load(bz2.BZ2File(database))
    for marker in db['markers']:
        if db['markers'][marker]['clade'] in clades:
            filtered_markers.append(marker)
    info('Done.',init_new_line=True)
    filtered_input = execute_pool(((parallel_filter_sam, i, input_format, tmp_dir, filtered_markers) for i in input), nprocs)
    return filtered_input


"""
Gets the clade-specific markers from a list of aligned samples in 
SAM or BAM format and writes the results in Pickles files in the
user-selected output directory

:param input: the samples as SAM or BAM files
:param sorted: whether the BAM files are sorted
:param input_format: format of the sample files [bam or sam]
:param output_dir: the output directory
:param database: the MetaPhlan markers database
:param breath_threshold: the breath threshold for the consensus markers
:param min_reads_aligning: the minimum number of reads to cover a marker
:param min_read_len: the minimum length for a read to be considered
:param min_base_coverage: the minimum coverage for a base to be considered
:param min_base_quality: the minimum quality for a base to be considered
:param dominant_frq_threshold: the cutoff for degree of 'allele dominance' for a position to be considered polymorphic
:param clades: the filtered set of clades to reconstruct the markers
:param tmp: the path where to store the tmp directory
:param debug: whether to remove the tmp directory
:param nprocs: number of threads to use in the execution
"""
def samples_to_markers(input, sorted, input_format, output_dir, database, breath_threshold, min_reads_aligning, min_read_len, min_base_coverage, min_base_quality, dominant_frq_threshold, clades, tmp, debug, nprocs):  
    tmp_dir = tempfile.mkdtemp(dir=output_dir) + "/" if tmp is None else tempfile.mkdtemp(dir=tmp) + "/"
    filtered = ''
    if len(clades) > 0:
        input = filter_sam_files(clades, database, input, input_format, tmp_dir, nprocs)
        input_format = 'sam'
        sorted = False
        filtered = '_filtered'
    input = convert_inputs(input, sorted, input_format, tmp_dir, nprocs)
    execute_cmseq(input, output_dir, breath_threshold, min_reads_aligning, min_read_len, min_base_coverage, min_base_quality, dominant_frq_threshold, filtered, nprocs)        
    
    if not debug:
        shutil.rmtree(tmp_dir, ignore_errors=False, onerror=None)


"""
Main function

:param input: the samples as SAM or BAM files
:param sorted: whether the BAM files are sorted
:param input_format: format of the sample files [bam or sam]
:param output_dir: the output directory
:param database: the MetaPhlan markers database
:param breadth_threshold: the breadth threshold for the consensus markers
:param min_reads_aligning: the minimum number of reads to cover a marker
:param min_read_len: the minimum length for a read to be considered
:param min_base_coverage: the minimum coverage for a base to be considered
:param min_base_quality: the minimum quality for a base to be considered
:param dominant_frq_threshold: the cutoff for degree of 'allele dominance' for a position to be considered polymorphic
:param clades: the filtered set of clades to reconstruct the markers
:param tmp: the path where to store the tmp directory
:param debug: whether to remove the tmp directory
:param nprocs: number of threads to use in the execution
"""
def main():
    t0 = time.time()
    args = read_params()
    info("Start samples to markers execution")
    check_dependencies()
    args = check_params(args)
    samples_to_markers(args.input, args.sorted, args.input_format, args.output_dir, args.database, 
        args.breadth_threshold, args.min_reads_aligning, args.min_read_len, args.min_base_coverage, 
        args.min_base_quality, args.dominant_frq_threshold, args.clades, args.tmp, args.debug, args.nprocs)
    exec_time = time.time() - t0
    info("Finish samples to markers execution ("+str(round(exec_time, 2))+
        " seconds): Results are stored at \""+args.output_dir+"\"\n",
         init_new_line=True)

if __name__ == '__main__':
    main()
