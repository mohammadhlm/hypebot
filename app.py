import os
import subprocess
import time
from helpers import (
    trim,
    humanize_bytes,
    process_available_line,
    clear_console,
    prompt_enter,
    prompt,
    run_command
)
from colors import Colors, print_colored
from aios_cli_functions import (
    check_aios_cli_installed,
    install_aios_cli,
    run_hive_infer,
    add_model,
    list_available_models,
    add_model_with_list,
    remove_model
)

# متغیر گلوبال برای ذخیره فرآیند Daemon
daemon_process = None

# بازنشانی فایل لاگ در ابتدای اجرا
with open("aios.log", "w") as log_file:
    pass

# بررسی پلتفرم (فقط Linux و macOS پشتیبانی می‌شود)
platform = subprocess.run(["uname"], stdout=subprocess.PIPE, text=True).stdout.strip().lower()
if platform not in ["linux", "darwin"]:
    print_colored("This script only supports Linux and macOS.", "red")
    exit(1)

# -------------------------------------------
# Coder Sign
# -------------------------------------------
def coder_mark():
    """Print the coder mark."""
    print(f"""
╭━━━╮╱╱╱╱╱╱╱╱╱╱╱╱╱╭━━━┳╮
┃╭━━╯╱╱╱╱╱╱╱╱╱╱╱╱╱┃╭━━┫┃{Colors.Green}
┃╰━━┳╮╭┳━┳━━┳━━┳━╮┃╰━━┫┃╭╮╱╭┳━╮╭━╮
┃╭━━┫┃┃┃╭┫╭╮┃╭╮┃╭╮┫╭━━┫┃┃┃╱┃┃╭╮┫╭╮╮{Colors.Blue}
┃┃╱╱┃╰╯┃┃┃╰╯┃╰╯┃┃┃┃┃╱╱┃╰┫╰━╯┃┃┃┃┃┃┃
╰╯╱╱╰━━┻╯╰━╮┣━━┻╯╰┻╯╱╱╰━┻━╮╭┻╯╰┻╯╰╯{Colors.Reset}
╱╱╱╱╱╱╱╱╱╱╱┃┃╱╱╱╱╱╱╱╱╱╱╱╭━╯┃{Colors.Blue}{{{Colors.Neon}cmalf{Colors.Blue}}}{Colors.Reset}
╱╱╱╱╱╱╱╱╱╱╱╰╯╱╱╱╱╱╱╱╱╱╱╱╰━━╯

{Colors.Reset}HyperSpace {Colors.Gold}LUA {Colors.Blue}{{ {Colors.Neon}aios-cli{Colors.Blue} }}{Colors.Reset}

{Colors.Green}{'-' * 50}{Colors.Reset}

{Colors.Gold}[+]{Colors.Reset} DM : {Colors.Teal}https://t.me/furqonflynn{Colors.Reset}
{Colors.Gold}[+]{Colors.Reset} GH : {Colors.Teal}https://github.com/cmalf/{Colors.Reset}
{Colors.Gold}[+]{Colors.Reset} BOT: {Colors.Blue}{{ {Colors.Neon}HyperSpace-Cli v1.0{Colors.Blue} }} {Colors.Reset}{Colors.Blue}{{ {Colors.Gold}Lua v5.4.7{Colors.Blue} }} {Colors.Reset}

{Colors.Green}{'-' * 50}{Colors.Reset}
    """)

# -------------------------------------------
# Hive Commands Sub Menu
# -------------------------------------------
def hive_menu():
    """Hive commands submenu."""
    clear_console()
    coder_mark()
    print_colored("\n=== HIVE Commands Submenu ===\n", "neon")
    print_colored("1.  Hive: Login               >", "gold")
    print_colored("2.  Hive: Import keys         >", "gold")
    print_colored("3.  Hive: Connect             >", "gold")
    print_colored("4.  Hive: Registered          >", "gold")
    print_colored("5.  Hive: Reregister          >", "gold")
    print_colored("6.  Hive: Whoami              >", "gold")
    print_colored("7.  Hive: Disconnect          >", "gold")
    print_colored("8.  Hive: Infer               >", "gold")
    print_colored("9.  Hive: Listen              >", "gold")
    print_colored("10. Hive: Interrupt           >", "gold")
    print_colored("11. Hive: Select-tier         >", "gold")
    print_colored("12. Hive: Allocate            >", "gold")
    print_colored("13. Hive: Points              >", "gold")
    print_colored("14. Hive: Rounds              >", "gold")
    print_colored("15. Hive: Help                >", "gold")
    print_colored("0.  Return to Main Menu       >", "gold")

    choice = prompt("\nSelect a Hive option: ")
    if choice == "1":
        run_command("aios-cli hive login", hive_menu)
    elif choice == "2":
        key_file = prompt("Enter the file path for your key (.pem or .base58): ")
        if key_file:
            run_command(f"aios-cli hive import-keys {key_file}", hive_menu)
        else:
            print_colored("File path is required.", "red")
            prompt_enter(hive_menu)
    elif choice == "3":
        run_command("aios-cli hive connect", hive_menu)
    elif choice == "4":
        run_command("aios-cli hive registered", hive_menu)
    elif choice == "5":
        run_command("aios-cli hive reregister", hive_menu)
    elif choice == "6":
        run_command("aios-cli hive whoami", hive_menu)
    elif choice == "7":
        run_command("aios-cli hive disconnect", hive_menu)
    elif choice == "8":
        run_hive_infer(hive_menu)
    elif choice == "9":
        run_command("aios-cli hive listen", hive_menu)
    elif choice == "10":
        run_command("aios-cli hive interrupt", hive_menu)
    elif choice == "11":
        tier = prompt("Enter the tier (e.g., 5,4,3,2,1): ")
        if tier:
            run_command(f"aios-cli hive select-tier {tier}", hive_menu)
        else:
            print_colored("Tier selection is required.", "red")
            prompt_enter(hive_menu)
    elif choice == "12":
        run_command("aios-cli hive allocate", hive_menu)
    elif choice == "13":
        run_command("aios-cli hive points", hive_menu)
    elif choice == "14":
        run_command("aios-cli hive rounds", hive_menu)
    elif choice == "15":
        run_command("aios-cli hive help", hive_menu)
    elif choice == "0":
        clear_console()
        menu()
    else:
        print_colored("Invalid option.", "red")
        prompt_enter(hive_menu)

# -------------------------------------------
# Main Menu
# -------------------------------------------
def menu():
    """Main menu."""
    clear_console()
    coder_mark()
    print_colored("\n=== aios-cli Bot Menu ===\n", "neon")
    print_colored("1.  Start daemon           >", "gold")
    print_colored("2.  Check daemon status    >", "gold")
    print_colored("3.  Kill daemon            >", "gold")
    print_colored("4.  List downloaded models >", "gold")
    print_colored("5.  Add a model            >", "gold")
    print_colored("6.  Remove a model         >", "gold")
    print_colored("7.  List available models  >", "gold")
    print_colored("8.  Show system info       >", "gold")
    print_colored("9.  Run inference          >", "gold")
    print_colored("10. Show version           >", "gold")
    print_colored("11. Hive Submenu           >", "gold")
    print_colored("12. Uninstall              >", "gold")
    print_colored("0.  Exit                   >", "gold")

    choice = prompt("\nSelect an option: ")
    if choice == "1":
        global daemon_process
        if daemon_process:
            print_colored("Daemon is already running in the background.", "yellow")
            prompt_enter(menu)
        else:
            result = subprocess.run("aios-cli start --connect >> aios.log 2>&1 & echo $!", shell=True, stdout=subprocess.PIPE, text=True)
            daemon_process = int(result.stdout.strip())
            print_colored("Daemon started in the background. Logs are appended to aios.log.", "green")
            prompt_enter(menu)
    elif choice == "2":
        run_command("aios-cli status", menu)
    elif choice == "3":
        global daemon_process
        if daemon_process:
            run_command("pkill -f aios", lambda: print_colored("Background daemon process has been killed.", "green"))
            daemon_process = None
            prompt_enter(menu)
        else:
            print_colored("No background daemon process is currently running.", "yellow")
            prompt_enter(menu)
    elif choice == "4":
        run_command("aios-cli models list", menu)
    elif choice == "5":
        add_model_with_list(menu)
    elif choice == "6":
        remove_model(menu)
    elif choice == "7":
        run_command("aios-cli models available", menu)
    elif choice == "8":
        run_command("aios-cli system-info", menu)
    elif choice == "9":
        run_hive_infer(menu)
    elif choice == "10":
        run_command("aios-cli version", menu)
    elif choice == "11":
        hive_menu()
    elif choice == "12":
        run_command("curl https://download.hyper.space/api/uninstall | sh", menu)
    elif choice == "0":
        print_colored("Exiting...", "green")
        exit(0)
    else:
        print_colored("Invalid option.", "red")
        prompt_enter(menu)

# اجرای برنامه
if __name__ == "__main__":
    if not check_aios_cli_installed():
        install_aios_cli()
        if not check_aios_cli_installed():
            print_colored("aios-cli installation failed. Exiting.", "red")
            exit(1)
    menu()
