import tldextract
import argparse
import sys
from tranco import Tranco
from datetime import datetime

def get_rank_score(rank):
    try:
        rank = int(rank)
        if rank == -1:
            return "No Rank Data"
        elif rank <= 1000:
            return "High (Very Popular)"
        elif rank <= 10000:
            return "Medium (Popular)"
        elif rank <= 100000:
            return "Low (Less Popular)"
        else:
            return "Very Low (Unpopular)"
    except (ValueError, TypeError):
        return "No Rank Data"

def getRoot(dom):
    ext = tldextract.extract(dom)
    if ext.domain and ext.suffix:
        return ext.registered_domain
    return None

def getRank(domain, t):
    try:
        rank = t.rank(domain)
        if rank is None or rank == 0:
            return "-1"
        return str(rank)
    except Exception as e:
        print(f"Error getting rank for {domain}: {str(e)}", file=sys.stderr)
        return "-1"

def main():
    parser = argparse.ArgumentParser(
        description="Extract the root domain and check Tranco rank from a list of domains."
    )
    parser.add_argument("-ld", "--listdomain", type=str, help="File containing the list of domains", required=False)
    parser.add_argument("-r", "--rank", action="store_true", help="Check domain rank using Tranco list")
    parser.add_argument("-s", "--score", choices=['all', 'none', 'low', 'medium', 'high'], 
                      help="Filter domains by rank score", default='all')
    parser.add_argument("-o", "--output", type=str, help="Save output to a file")
    
    if len(sys.argv) == 1 and sys.stdin.isatty():
        print("Extract the root domain from a list of domains.")
        parser.print_help()
        return

    args = parser.parse_args()
    
    output_file = None
    if args.output:
        try:
            output_file = open(args.output, 'w')
        except Exception as e:
            print(f"Error opening output file: {str(e)}", file=sys.stderr)
            return
    
    if args.rank:
        t = Tranco().list()
    
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
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    seen_domains = set()
    
    for dom in listdom:
        root_domain = getRoot(dom)
        if root_domain and root_domain not in seen_domains:
            seen_domains.add(root_domain)
            if args.rank:
                rank = getRank(root_domain, t)
                score = get_rank_score(rank)
                
                if rank != "-1":
                    if args.score != 'all':
                        if args.score == 'high' and 'High' not in score:
                            continue
                        elif args.score == 'medium' and 'Medium' not in score:
                            continue
                        elif args.score == 'low' and 'Low' not in score:
                            continue
                        elif args.score == 'none' and 'No Rank' not in score:
                            continue
                    
                    output = f"https://{root_domain} | {rank} | {current_date} | {score}"
                    print(output)
                    if output_file:
                        output_file.write(output + '\n')
            else:
                output = root_domain
                print(output)
                if output_file:
                    output_file.write(output + '\n')
    
    if output_file:
        output_file.close()

if __name__ == "__main__":
    main()
