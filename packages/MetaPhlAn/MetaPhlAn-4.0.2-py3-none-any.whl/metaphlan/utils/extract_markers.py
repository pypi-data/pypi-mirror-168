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
    from .util_fun import info, error
except ImportError:
    from util_fun import info, error

if sys.version_info[0] < 3:
    error("StrainPhlAn " + __version__ + " requires Python 3, your current Python version is {}.{}.{}"
                    .format(sys.version_info[0], sys.version_info[1], 
                        sys.version_info[2]), exit=True)
                        
import pickle, bz2, os, time
import subprocess as sb
import argparse as ap
from Bio import SeqIO, Seq, SeqRecord
try:
    from .external_exec import generate_markers_fasta
except ImportError:
    from external_exec import generate_markers_fasta

# get the directory that contains this script
metaphlan_script_install_folder = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_FOLDER = os.path.join(metaphlan_script_install_folder, "../metaphlan_databases")
DEFAULT_DB_FOLDER = os.environ.get('METAPHLAN_DB_DIR', DEFAULT_DB_FOLDER)
DEFAULT_DB_NAME =  "mpa_vJan21_CHOCOPhlAnSGB_202103.pkl"
DEFAULT_DATABASE = os.path.join(DEFAULT_DB_FOLDER, DEFAULT_DB_NAME)

"""
Reads and parses the command line arguments of the script.

:returns: the parsed arguments
"""
def read_params():
    p = ap.ArgumentParser(description="", formatter_class=ap.ArgumentDefaultsHelpFormatter)
    p.add_argument('-d', '--database', type=str, default=DEFAULT_DATABASE,
                   help="The input MetaPhlAn database")
    p.add_argument('-c', '--clades', type=str, nargs='+', default=[],
                   help="The clades to investigate")   
    p.add_argument('-o', '--output_dir', type=str, default=None,
                   help="The output directory")
    
    return p.parse_args()


"""
Checks the mandatory command line arguments of the script.

:returns: the checked args
"""
def check_params(args):
    if len(args.clades) == 0:
        error('-c (or --clades) must be specified', exit=True, 
            init_new_line=True)
    elif not args.output_dir:
        error('-o (or --output_dir) must be specified', exit=True, 
            init_new_line=True)
    elif not os.path.exists(args.output_dir):
        error('The directory {} does not exist'.format(args.output_dir), exit=True, 
            init_new_line=True)
    elif not os.path.exists(args.database):
        error('The database does not exist', exit=True, 
            init_new_line=True)
    if not args.output_dir.endswith('/'):
        args.output_dir += '/'
    
    return args


"""
Checks the mandatory programs to execute of the script.

"""
def check_dependencies():
    try:
        sb.check_call("bowtie2-inspect", stdout=sb.DEVNULL, stderr=sb.DEVNULL)
    except Exception as e:
        error('Program not installed or not present in the system path\n'+str(e), 
            init_new_line=True, exit=True)


"""
Extract the markers of a specific clade in a MetaPhlAn database

:param database: the MetaPhlan markers database
:param clades: the clades to extract markers
:param output_dir: the output directory
:returns: the output file with the extracted sequences of the marker
"""
def extract_markers(database, clades, output_dir):
    info('\tExtracting markers from the Bowtie2 database...', init_new_line=True)
    fasta_markers = generate_markers_fasta(database, output_dir)
    info('\tDone.', init_new_line=True)
    info('\tLoading MetaPhlAn {} database...'.format(database.split('/')[-1][:-4]), init_new_line=True)
    db = pickle.load(bz2.BZ2File(database))
    info('\tDone.',init_new_line=True)
    for clade in clades:
        markers = set()
        for marker in db['markers']:
            if clade == db['markers'][marker]['clade']:
                markers.add(marker)
        if len(markers) == 0:
            error('No markers were found for the clade "{}".'.format(clade), exit=False, init_new_line=True)
        else:
            info('\tNumber of markers for the clade "{}": {}'.format(clade, len(markers)), init_new_line=True)
            output_file = output_dir+clade+".fna"
            info('\tExporting markers for clade {}...'.format(clade), init_new_line=True)
            with open(output_file, 'w') as ofile:
                for rec in SeqIO.parse(open(fasta_markers, 'r'), 'fasta'):
                    if rec.name in markers:
                        SeqIO.write(rec, ofile, 'fasta')
            info('\tDone.', init_new_line=True)    
    os.remove(fasta_markers)
    return output_file


"""
Main function

:param database: the MetaPhlan markers database
:param clade: the clade to extract markers
:param output_dir: the output directory
"""
def main():
    t0 = time.time()
    args = read_params()
    info("Start extract markers execution")
    # check_dependencies()
    args = check_params(args)
    extract_markers(args.database, args.clades, args.output_dir)
    exec_time = time.time() - t0
    info("Finish extract markers execution ("+str(round(exec_time, 2))+
        " seconds): Results are stored at \""+args.output_dir+"\"\n",
         init_new_line=True)

if __name__ == '__main__':
    main()
