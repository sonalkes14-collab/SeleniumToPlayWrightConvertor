import os
import subprocess
import sys

def run_batch_conversion(source_dir="samples"):
    """
    Triggers conversion for all .java files in the specified directory.
    """
    print(f"--- Starting Batch Trigger for: {source_dir}")
    
    if not os.path.exists(source_dir):
        print(f"[ERROR] Source directory not found: {source_dir}")
        return

    java_files = [f for f in os.listdir(source_dir) if f.endswith(".java")]
    
    if not java_files:
        print(f"[WARN] No .java files found in {source_dir}")
        return

    print(f"[INFO] Found {len(java_files)} files to process.")
    
    for file_name in java_files:
        full_path = os.path.join(source_dir, file_name)
        print(f"\n--- Processing: {file_name} ---")
        
        # Trigger the main coordinator
        try:
            subprocess.run(["python", "main_coordinator.py", full_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to convert {file_name}: {e}")

    print("\n[SUCCESS] Batch process complete! Check 'output/' for specs and reports.")

if __name__ == "__main__":
    dir_to_process = sys.argv[1] if len(sys.argv) > 1 else "samples"
    run_batch_conversion(dir_to_process)
