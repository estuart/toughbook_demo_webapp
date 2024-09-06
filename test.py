import subprocess

def run_ansible_playbook(playbook, inventory, extravars=None):
    """Run an Ansible playbook using subprocess."""
    try:
        # Base ansible-playbook command as a list of arguments
        command = ['ansible-playbook', '-i', inventory, playbook]

        # Add extra variables if they exist
        if extravars:
            extra_vars_option = ' '.join([f'{key}={value}' for key, value in extravars.items()])
            command.extend(['--extra-vars', extra_vars_option])

        # Run the ansible-playbook command
        print(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True)

        # Check if the playbook ran successfully
        if result.returncode == 0:
            print(f"Playbook executed successfully!\nOutput:\n{result.stdout}")
        else:
            print(f"Playbook execution failed with error:\n{result.stderr}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def execute_workload(workload):
    """Simulate executing a workload by switching images."""
    inventory_path = 'inventory.ini'    # Replace with the correct path to your inventory file
    playbook_path = 'playbooks/switch-image.yml'  # Replace with the correct playbook path

    # Run the playbook with extra vars (bootc_image_tag in this case)
    extra_vars = {'bootc_image_tag': workload}
    run_ansible_playbook(playbook_path, inventory_path, extra_vars)


def reboot_system():
    """Simulate rebooting the system by running the reboot playbook."""
    inventory_path = 'inventory.ini'    # Replace with the correct path to your inventory file
    playbook_path = 'playbooks/reboot.yml'  # Replace with the correct playbook path

    run_ansible_playbook(playbook_path, inventory_path)


if __name__ == "__main__":
    print("Choose an option:")
    print("1. Switch workload")
    print("2. Reboot system")
    choice = input("Enter 1 or 2: ")

    if choice == '1':
        workload = input("Enter the workload to switch to (e.g., f22, f35, etc.): ")
        execute_workload(workload)
    elif choice == '2':
        reboot_system()
    else:
        print("Invalid choice")
