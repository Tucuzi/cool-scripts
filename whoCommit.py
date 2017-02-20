#!/usr/bin/python3
import os
import sys
import optparse

list_optparse = optparse.OptionParser(usage="usage: whoCommit.py -p [project path] -d [since date]")

group = list_optparse.add_option_group('Dispaly commitors options')
group.add_option('-p', '--path',
                 dest="path", 
                 help='git project location', metavar='PATH')

group.add_option('-d', '--date',
                 dest="date", 
                 help='since date', metavar='DATE')

group.add_option('-i', '--info',
                 dest="info", action="store_true", default=False,
                 help="display the short total info")

def usage():
    list_optparse.print_help()

def display_author_commit(authors, date):
    for author in authors:
     an="'"+author+"'"
     cmd = 'git log --pretty="" --since=' + date + ' --author=' + an + ' --name-only' + '|sort|uniq'
     modified_files = os.popen(cmd).read()
     cmd = 'git log --pretty="%ae" --since=' + date  + ' --author=' + an + '|sort|uniq'
     author_email = os.popen(cmd).read()
     author_email = author_email.strip('\n')
     print(author + " " + "<" +author_email + ">")
     print("==========================")
     print(modified_files)

def display_info(authors, date, path):
    an_num=authors.__len__()
    cmd = 'git log --pretty="" --since=' + date + ' --name-only' + '|sort|uniq'
    fstr = os.popen(cmd).read()
    mfiles = fstr.split('\n')
    mfiles.remove('')
    fnum=mfiles.__len__() 
    print("Since " + date + ":",an_num,"authors modified",fnum, "files"+" @"+path)
    

def main(orig_args):
    opt, args = list_optparse.parse_args(orig_args)
    if args:
        list_optparse.print_usage()
        sys.exit(1)
    
    project_path=opt.path
    if not project_path:
        list_optparse.print_usage()
        sys.exit(1)
        
    since_date=opt.date
    if not since_date:
        list_optparse.print_usage()
        sys.exit(1)
 
    os.chdir(project_path)
    cmd = 'git log --pretty="%an" --since=' + since_date + '|sort|uniq'
    authors_str = os.popen(cmd).read()
    authors=authors_str.split("\n")
    authors.remove('')
    authors_num = authors.__len__()
    if authors_num < 1:
        print("No bady commit since "+since_date+" at "+project_path)
        sys.exit(0)

    if opt.info == True:
	    display_info(authors,since_date,project_path)
    else:
        display_author_commit(authors,since_date)

    sys.exit(1)

if __name__ == '__main__':
    main(sys.argv[1:])
