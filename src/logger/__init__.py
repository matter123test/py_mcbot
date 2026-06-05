from colorama import Fore, Style


class Logger:
    @staticmethod
    def log(content: str):
        print(Fore.BLUE + f"LOG: {content}" + Style.RESET_ALL)

    @staticmethod
    def warn(content: str):
        print(Fore.YELLOW + f"WARNING: {content}" + Style.RESET_ALL)

    @staticmethod
    def err(content: str):
        print(Fore.RED + f"ERROR: {content}" + Style.RESET_ALL)
