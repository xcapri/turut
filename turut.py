import tldextract
import argparse
import sys

def getRoot(dom):
    ext = tldextract.extract(dom)
    return ext.registered_domain

def main():
    parser = argparse.ArgumentParser(
        description="Extract the root domain from a list of domains."
    )
    parser.add_argument("-ld", "--listdomain", type=str, help="File containing the list of domains", required=False)
    
    if len(sys.argv) == 1 and sys.stdin.isatty():
        print("Extract the root domain from a list of domains.")
        parser.print_help()
        return

    args = parser.parse_args()
    
    if args.listdomain:
        try:
            with open(args.listdomain, "r") as f:
                listdom = [line.strip() for line in f.readlines()]
            if not listdom: 
                print("The file is empty.")
                return
        except FileNotFoundError:
            print(f"File {args.listdomain} not found.")
            return
    else:
        listdom = [line.strip() for line in sys.stdin]
        if not listdom:  
            print("No domains provided through stdin or file.")
            return
    
    for dom in listdom:
        print(getRoot(dom))

if __name__ == "__main__":
    main()
