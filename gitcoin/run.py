import argparse
import subprocess
from gitcoin.transact import make_keys

# only integer transactions are allowed


def dest_and_amt_info(args):
    # join all arguments into a single string
    input = ' '.join(args)
    #print(input)
    try:
        args = input.split(' ')
    except Exception:
        print("Invalid Argument Sequences for 'Pay' command.")

    for i in range(len(args)):
        # even index = destinations
        if i % 2 == 0 and not args[i].isalpha():
            raise TypeError("Destination must be a string.")
        if i % 2 != 0 and not args[i].isdigit():
            print(args[i])
            #print(args[i])
            raise TypeError("Amount must be an integer.")

    return args


def run():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    # payment command
    pay_parser = subparsers.add_parser(
        "pay", help="Pay a destination a certain amount of Gitcoin")
    pay_parser.add_argument("dest_and_amt", nargs='+',
                            help="Paying a destination a certain amount of Gitcoin with fees")

    # subparser for remote command
    remote_parser = subparsers.add_parser("remote", help="git remote clone")
    remote_subparsers = remote_parser.add_subparsers(
        dest="remote_action", help="sub-command help")

    # subparser remote add
    remote_add_parser = remote_subparsers.add_parser(
        "add", help="git remote add clone")
    remote_add_parser.add_argument("name", help="Name of the remote", type=str)
    remote_add_parser.add_argument("url", help="URL of the remote", type=str)

    # subparser remote remove
    remote_remove_parser = remote_subparsers.add_parser(
        "remove", help="git remote remove clone")
    remote_remove_parser.add_argument(
        "name", help="Name of the remote", type=str)

    # mine command
    mine_parser = subparsers.add_parser(
        "mine", help="Mine Gitcoin, with love <3")

    # observer command
    observer_parser = subparsers.add_parser(
        "observer", help="Take a look at your own blockchain")

    keypair_parser = subparsers.add_parser("keypair", help="generate or set keypairs")
    keypair_subparsers = keypair_parser.add_subparsers(dest="keypair_action", help="idk")

    keypair_subparsers.add_parser("generate", help="generate private key")
    keypair_set_parser = keypair_subparsers.add_parser("set", help="set your private key")
    keypair_set_parser.add_argument("privkey", help="your private key", type=str)

    

    args = parser.parse_args()

    # no input, print help message
    print(vars(args))
    if args.command is None:
        parser.print_help()

    if args.command == "pay":
        print("pay")
        payment_info = dest_and_amt_info(args.dest_and_amt)
        if len(payment_info) % 2 != 0:
            fee = payment_info.pop(-1)
        else:
            fee = 1

        print(f"fee is {fee}")
        for i in range(0, len(payment_info), 2):
            print(
                f"Destination: {payment_info[i]}, Amount: {payment_info[i+1]}")

    elif args.command == "remote":
        print('remote')
        if args.remote_action == "add":
            print(f"Adding remote: {args.name} with URL: {args.url}")
            subprocess.Popen(
                f'git remote add {args.name} {args.url}', shell=True)
        elif args.remote_action == "remove":
            print(f"Removing remote: {args.name}")
            subprocess.Popen(f'git remote rm {args.name}', shell=True)
        else:
            raise Exception("Invalid remote command")

    elif args.command == "mine":
        print("Mining Gitcoin...")

    elif args.command == "observer":
        print("Observer placeholder")

    if args.command == "keypair":
        if args.keypair_action == "set":
            print(f"setting private key {args.privkey}")
        if args.keypair_action == "generate":
            [priv, pub] = make_keys()
            print(f"keys:\nprivate {priv}\npublic: {pub}\n\nthese are saved")
    


if __name__ == "__main__":
    run()