"""
    Copyright 2020 Simon Vandevelde, Bram Aerts, Joost Vennekens
    This code is licensed under GNU GPLv3 license (see LICENSE) for more
    information.
    This file is part of the cDMN solver.
"""
import argparse
from cdmn.glossary import Glossary
from cdmn.interpret import VariableInterpreter
from cdmn.idply import Parser
import sys
from cdmn.table_operations import (fill_in_merged, identify_tables,
                                   find_glossary, find_execute_method,
                                   replace_with_error_check,
                                   create_voc, create_main,
                                   create_struct, create_theory,
                                   create_display)
# from post_process import merge_definitions


def main():
    """
    The main function for the cDMN solver.
    """

    # Parse the arguments.
    argparser = argparse.ArgumentParser(description='Run cDMN on DMN tables.')
    argparser.add_argument('--version', '-v', action='version',
                           version='2.0.0')
    argparser.add_argument('path_to_file', metavar='path_to_file', type=str,
                           help='the path to the xlsx or xml file')
    argparser.add_argument('-n', '--name', metavar='name_of_sheet', type=str,
                           help='the name(s) of the sheet(s) to execute',
                           nargs='+')
    argparser.add_argument('-o', '--outputfile', metavar='outputfile',
                           type=str,
                           default=None,
                           help='the name of the outputfile')
    argparser.add_argument('--idp', metavar='idp',
                           type=str,
                           default=None,
                           help='the path to the idp executable')
    argparser.add_argument('--idp-z3',
                           action='store_true')
    argparser.add_argument('--interactive-consultant',
                           help="generate file specifically for the"
                                " Interactive Consultant",
                           action='store_true')
    argparser.add_argument('--main',
                           help="create a main, to use when generating for"
                                " the IDP-Z3 Interactive Consultant",
                           action='store_true')
    argparser.add_argument('--errorcheck-overlap', metavar='overlaptable',
                           type=str,
                           help='the table to check for overlap errors'
                                ': table is identified by table id')
    argparser.add_argument('--errorcheck-shadowed', metavar='shadowedtable',
                           type=str,
                           help='the table to check for shadowed rules'
                                ': table is identified by table id')
    argparser.add_argument('--errorcheck-rule',
                           type=int,
                           help='the rule to check for being erronous')
    argparser.add_argument('--errorcheck-gap',
                           type=str,
                           help='the table to check for input gaps'
                                ': table is identified by table id')
    args = argparser.parse_args()


    # Open the file on the correct sheet and read all the tablenames.
    filepath = args.path_to_file

    if filepath.endswith('.xlsx'):
        xml = False
        sheetnames = args.name
        if sheetnames is None:
            raise IOError("No sheetname given")
        sheets = fill_in_merged(filepath, sheetnames)
        tables = identify_tables(sheets)

    elif filepath.endswith('.dmn') or filepath.endswith('.xml'):
        xml = True
        from cdmn.parse_xml import XMLparser
        with open(filepath, 'r') as f:
            p = XMLparser(f.read())
            tables = p.get_tables()

    else:
        raise IOError("Invalid filepath")

    # If error checking needs to be done, we change the model to a cDMN model
    # which can be used for error checking.
    if args.errorcheck_overlap:
        dependencies = p.get_table_dependencies(args.errorcheck_overlap)
        tables = replace_with_error_check(tables, 'overlap',
                                          args.errorcheck_overlap,
                                          deps=dependencies)

    elif args.errorcheck_shadowed:
        dependencies = p.get_table_dependencies(args.errorcheck_shadowed)
        tables = replace_with_error_check(tables, 'shadowed',
                                          args.errorcheck_shadowed,
                                          args.errorcheck_rule,
                                          deps=dependencies)

    elif args.errorcheck_gap:
        dependencies = p.get_table_dependencies(args.errorcheck_gap)
        tables = replace_with_error_check(tables, 'gap',
                                          args.errorcheck_gap,
                                          deps=dependencies)

    g = Glossary(find_glossary(tables))
    inf = find_execute_method(tables)

    i = VariableInterpreter(g)
    parser = Parser(i)

    # Create the main blocks.
    struct = create_struct(tables, parser, g)
    voc = create_voc(g)
    theory = create_theory(tables, parser)
    if args.main or args.idp_z3:
        main = create_main(inf, parser)
    elif args.interactive_consultant:
        if xml:
            goal_var = p.get_goal_variables()
        else:
            goal_var = []
        main = create_display(goal_var)
    else:
        main = ""
    file_path = None
    print('Done parsing.')
    if len(parser.parsing_errors) != 0:
        print("Errors detected in specification.\nUnable to parse headers:")
        for header, error_list in parser.parsing_errors.items():
            print(f"\tin {header}:")
            for error in error_list:
                print(f"\t\t{error}")
        print("No output was created.")
        return

    # If an output file is listed, write to it.
    if args.outputfile:
        file_path = args.outputfile
        if ".idp" not in args.outputfile:
            file_path += args.name_of_sheet.replace(' ', '_') + ".idp"
        fp = open(file_path, 'w')
        fp.write(voc)
        fp.write(theory)
        fp.write(struct)
        fp.write(main)
        fp.close()

    # If the IDP-Z3 tsystem was requested, run the idp_engine.
    if args.idp_z3:
        print("Running the IDP-Z3 idp_engine.")
        from idp_engine.Parse import idpparser
        idp = idpparser.model_from_str(voc + theory + struct + main)
        idp.execute()

    # If no options were supplied, print the specification.
    if not args.outputfile and not args.idp_z3:
        print(voc + theory + struct)
        if main:
            print(main)


if __name__ == "__main__":
    main()
