import os
import sys
import datetime

def create_test_file(instance_id):
    """Creates a test file to indicate that instance details have been collected."""
    report_dir = 'reports/instance-detail/'
    os.makedirs(report_dir, exist_ok=True)  # Ensure the directory exists

    # Format the timestamp for the filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    test_file_name = f"test_file_{instance_id}_{timestamp}.txt"
    test_file_path = os.path.join(report_dir, test_file_name)
    
    try:
        with open(test_file_path, 'w') as f:
            f.write("Instance details collection test completed successfully.\n")
        print(test_file_path)  # Output the path to stdout
    except Exception as e:
        print(f"Failed to write test file. Error: {e}")
        sys.exit(1)

    return test_file_path

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python instance-details.py <INSTANCE_ID>")
        sys.exit(1)

    instance_id = sys.argv[1]
    report_path = create_test_file(instance_id)
    print(report_path)  # Output the report path for the workflow to capture
