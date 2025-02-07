import subprocess
import time
from helpers import trim, humanize_bytes, process_available_line, prompt_enter, prompt, run_command
from colors import Colors, print_colored


# بررسی نصب بودن aios-cli
def check_aios_cli_installed():
    """Check if aios-cli is installed."""
    try:
        result = subprocess.run(["which", "aios-cli"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0 or trim(result.stdout) == "":
            return False
        return True
    except Exception as e:
        print_colored(f"Error checking aios-cli: {e}", "red")
        return False


# نصب خودکار aios-cli
def install_aios_cli():
    """Install aios-cli automatically."""
    print_colored("Installing aios-cli...", "yellow")
    try:
        run_command('curl https://download.hyper.space/api/install | sh')
        print_colored("aios-cli installation process finished.", "green")
        time.sleep(2)  # Give a short delay for installation to settle
    except Exception as e:
        print_colored(f"Error installing aios-cli: {e}", "red")


# اجرای مدل‌های Hive
def run_hive_infer():
    """Run Hive inference logic."""
    try:
        result = subprocess.run(["aios-cli", "hive", "registered"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print_colored(f"Error retrieving registered models: {result.stderr}", "red")
            prompt_enter()
            return

        models = [trim(line) for line in result.stdout.split("\n") if trim(line) and not line.startswith("Found")]

        if not models:
            print_colored("No registered models found.", "yellow")
            model_name = prompt("Enter the model identifier for hive inference: ")
            prompt_text = prompt("Enter the prompt text: ")
            if model_name and prompt_text:
                run_command(f'aios-cli hive infer --model {model_name} --prompt "{prompt_text}"')
            else:
                print_colored("Both model identifier and prompt are required.", "red")
                prompt_enter()
        elif len(models) == 1:
            print_colored(f"Automatically selected model: {models[0]}", "green")
            prompt_text = prompt("Enter the prompt text: ")
            if prompt_text:
                run_command(f'aios-cli hive infer --model {models[0]} --prompt "{prompt_text}"')
            else:
                print_colored("Prompt text is required.", "red")
                prompt_enter()
        else:
            print_colored("Multiple registered models found. Please select one:", "green")
            for i, model in enumerate(models, 1):
                print_colored(f"{i}. {model}", "gold")
            choice_index = prompt("Enter your choice (number): ")
            try:
                index = int(choice_index)
                selected_model = models[index - 1]
                prompt_text = prompt("Enter the prompt text: ")
                if prompt_text:
                    run_command(f'aios-cli hive infer --model {selected_model} --prompt "{prompt_text}"')
                else:
                    print_colored("Prompt text is required.", "red")
                    prompt_enter()
            except (ValueError, IndexError):
                print_colored("Invalid selection.", "red")
                prompt_enter()
    except Exception as e:
        print_colored(f"Error running hive inference: {e}", "red")


# اضافه کردن مدل
def add_model(model_arg):
    """Add a model with error handling."""
    try:
        result = subprocess.run(["aios-cli", "models", "add", model_arg], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            if "unexpected argument" in result.stdout:
                print_colored("Error detected: Unexpected argument.", "yellow")
                manual_model = prompt("Enter the model identifier to add: ")
                if manual_model:
                    run_command(f"aios-cli models add {manual_model}")
                else:
                    print_colored("Model identifier is required.", "red")
                    prompt_enter()
            else:
                print_colored(f"Error adding model: {result.stdout}", "red")
                prompt_enter()
        else:
            print_colored("Model added successfully.", "green")
            prompt_enter()
    except Exception as e:
        print_colored(f"Error adding model: {e}", "red")


# لیست مدل‌های موجود
def list_available_models():
    """List available models."""
    try:
        result = subprocess.run(["aios-cli", "models", "available"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print_colored(f"Error retrieving available models: {result.stderr}", "red")
            prompt_enter()
            return

        for line in result.stdout.split("\n"):
            processed = process_available_line(line)
            print(processed)
        prompt_enter()
    except Exception as e:
        print_colored(f"Error listing available models: {e}", "red")


# حذف مدل
def remove_model():
    """Remove a downloaded model."""
    try:
        result = subprocess.run(["aios-cli", "models", "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print_colored(f"Error retrieving downloaded models: {result.stderr}", "red")
            prompt_enter()
            return

        models = [trim(line) for line in result.stdout.split("\n") if trim(line)]

        if not models:
            print_colored("No downloaded models found.", "yellow")
            prompt_enter()
        elif len(models) == 1:
            print_colored(f"Only one downloaded model found: {models[0]}", "green")
            answer = prompt("Are you sure you want to remove this model? (y/n): ")
            if answer.lower() == "y":
                run_command(f"aios-cli models remove {models[0]}")
            else:
                print_colored("Operation cancelled.", "yellow")
                prompt_enter()
        else:
            print_colored("Downloaded models:", "green")
            for i, model in enumerate(models, 1):
                print_colored(f"{i}. {model}", "gold")
            choice_index = prompt("Enter the number of the model to remove: ")
            try:
                index = int(choice_index)
                selected_model = models[index - 1]
                run_command(f"aios-cli models remove {selected_model}")
            except (ValueError, IndexError):
                print_colored("Invalid selection.", "red")
                prompt_enter()
    except Exception as e:
        print_colored(f"Error removing model: {e}", "red")
