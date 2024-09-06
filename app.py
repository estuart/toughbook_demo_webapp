import subprocess
from flask import Flask, render_template

app = Flask(__name__)

def run_switch_image_playbook(workload, ip_address):
    """Run the Ansible playbook to switch the image."""
    try:
        switch_image_command = [
            'ansible-playbook',
            '-i', 'inventory.ini',  # Replace with the actual path to your inventory file
            'playbooks/switch-image.yml',     # Replace with the actual path to your playbook
            '--limit', ip_address,
            '--extra-vars', f'bootc_image_tag={workload}'
        ]
        print(switch_image_command) 
        result_switch = subprocess.run(switch_image_command, capture_output=True, text=True)
        
        #if result_switch.returncode != 0:
        #    return f"Image switch playbook failed. Error: {result_switch.stderr}"
        
        return f"Image switch playbook executed successfully!\nOutput:\n{result_switch.stdout}"
    
    except Exception as e:
        return f"An error occurred during the image switch playbook: {str(e)}"

def run_reboot_playbook(ip_address):
    """Run the Ansible playbook to reboot the machine."""
    try:
        reboot_command = [
            'ansible-playbook',
            '-i', 'inventory.ini',
            'playbooks/reboot.yml',  # Replace with the actual path to your reboot playbook
            '--limit', ip_address
        ]
        
        result_reboot = subprocess.run(reboot_command, capture_output=True, text=True)
        
        #if result_reboot.returncode != 0:
        #    return f"Reboot playbook failed. Error: {result_reboot.stderr}"
        
        return f"Reboot playbook executed successfully!\nOutput:\n{result_reboot.stdout}"
    
    except Exception as e:
        return f"An error occurred during the reboot playbook: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/workload/<workload>', methods=['POST'])
def execute_workload(workload):
    ip_address = '192.168.8.100'  # Replace with the actual IP address
    return run_switch_image_playbook(workload, ip_address)

@app.route('/reboot', methods=['POST'])
def reboot_system():
    ip_address = '192.168.8.100'  # Replace with the actual IP address
    return run_reboot_playbook(ip_address)

if __name__ == '__main__':
    app.run(debug=True)
