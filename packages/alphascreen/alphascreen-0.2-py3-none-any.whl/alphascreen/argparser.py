import optparse
import sys
import alphascreen

def argparse():

    """
    optparse is used to initialize all command-line options.
    """
    
    parser = optparse.OptionParser(usage="Usage: %prog [options]",
        version=alphascreen.__version__)

    jobsetup_opts = optparse.OptionGroup(
        parser, 'Job setup')

    jobsetup_opts.add_option("--parse",
        action="store", dest="table", type="string", default="", metavar='file',
        help="Path to the excel file (.xlsx) or table (.txt).")

    jobsetup_opts.add_option("--fragment",
        action="store", dest="fraglen", type="int", default=500, metavar='fragment-length',
        help="Approximate fragment length. Default is 500.")

    jobsetup_opts.add_option("--overlap",
        action="store", dest="overlap", type="int", default=50, metavar='overlap-length',
        help="Sequence is extended by this amount on either side of slices. Default is 50.")

    jobsetup_opts.add_option("--dimerize",
        action="store", dest="dimerize", type="string", default="", metavar='dimerize-id',
        help="Uniprot ID to dimerize.")

    jobsetup_opts.add_option("--consider",
        action="store", dest="consider", type="string", default="", metavar='sequence-to-consider',
        help="Uniprot ID and sequence range to consider. Example: \"Q86VS8/1/200\" only considers amino acids 1-200 for uniprot ID Q86VS8.")

    jobsetup_opts.add_option("--dontwrite",
        action="store_true", dest="dontwrite", default=False,
        help="Pass if you don't want to write out files.")

    jobsetup_opts.add_option("--alphafold_exec",
        action="store", dest="alphafold_exec", type="string", default="colabfold2", metavar='executable',
        help="Colabfold executable. Default is \"colabfold2\"")

    jobsetup_opts.add_option("--columnA",
        action="store", dest="columnA", type="string", default="SWISS-PROT Accessions Interactor A", metavar='columnA-name',
        help="Name of column heading for uniprot IDs for first interactors.")

    jobsetup_opts.add_option("--columnB",
        action="store", dest="columnB", type="string", default="SWISS-PROT Accessions Interactor B", metavar='columnB-name',
        help="Name of column heading for uniprot IDs for second interactors.")
    
    parser.add_option_group(jobsetup_opts)

    check_opts = optparse.OptionGroup(
        parser, 'Check runs')

    check_opts.add_option("--check",
        action="store_true", dest="check", default=False,
        help="Check how many jobs are left.")

    check_opts.add_option("--write_unfinished",
        action="store_true", dest="check_write", default=False,
        help="Check how many jobs are left and write a new script to only run those jobs.")

    parser.add_option_group(check_opts)

    analyze_opts = optparse.OptionGroup(
        parser, 'Analysis')

    analyze_opts.add_option("--show_top",
        action="store", dest="threshold", type="float", default=-1, metavar="threshold",
        help="Summarize results for top hits (above the threshold specified here) in tables and pdfs.")
    
    analyze_opts.add_option("--overwrite",
        action="store_true", dest="overwrite", default=False,
        help="Pass this to overwrite snapshot pngs if they already exist.")

    parser.add_option_group(analyze_opts)

    """
    The rest of the function parses the input and generates a dictionary for use in decisiontree.py
    """

    #Get the passed arguments from command-line
    options,args = parser.parse_args()

    #If there are less than 1 arguments passed, there were no options passed.
    if len(sys.argv) < 1:
            #parser.print_help()
            #print("\n>> You did not pass the arguments properly. For help, run \"starparser -h\".")
            print("\n>> Help: alphascreen -h\n")
            sys.exit()

    #Initialize an empty dictionary to place all the parameters in
    params={}

    #Place the passed parameters (or default values if none were passed) into the params dictionary
    for i in options.__dict__.items():
        params[i[0]] = i[1]
        
    #The dictionary is the main input to decisiontree.py
    return(params)