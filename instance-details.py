import subprocess
import sys
import datetime

def get_installed_packages():
    try:
        command = "dpkg --get-selections"  # For Debian/Ubuntu
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error fetching installed packages: {e.stderr.decode('utf-8')}")
        sys.exit(1)

def write_report(instance_id, packages):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"reports/instance-detail/instance_report_{instance_id}_{timestamp}.txt"
    with open(report_path, 'w') as f:
        f.write(f"Instance ID: {instance_id}\n")
        f.write("Installed Packages:\n")
        f.write(packages)
    print(f"Instance details report written to {report_path}")
    return report_path

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python instance-details.py <INSTANCE_ID>")
        sys.exit(1)

    instance_id = sys.argv[1]
    packages = get_installed_packages()
    report_path = write_report(instance_id, packages)
    print(report_path)  # Output the report path for the workflow to capture
