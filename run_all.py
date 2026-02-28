import sys
import os
import subprocess
import logging

def setup_logger():
    
    logger = logging.getLogger("WorkflowLogger")
    logger.setLevel(logging.INFO)
    
    
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    
    fh = logging.FileHandler("run_all.log", mode="a", encoding="utf-8")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    return logger

def main():
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    logger = setup_logger()
    logger.info("Starting benchmarking workflow...")
    
    
    script_sequence = [
        os.path.join("scripts", "run_bandit.py"),
        os.path.join("scripts", "parse_bandit.py"),
        os.path.join("scripts", "run_llm.py"),
        os.path.join("scripts", "metrics.py")
    ]
    
    summary = {}
    
    for script_path in script_sequence:
        logger.info("-" * 50)
        logger.info(f"Executing script: {script_path}")
        
        
        if not os.path.exists(script_path):
            error_msg = f"File not found: {script_path}. Skipping."
            logger.error(error_msg)
            summary[script_path] = "Failed (File not found)"
            continue
            
        try:
            
            command = [sys.executable, script_path]
            
            
            process = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False
            )
            
            
            script_name = os.path.basename(script_path)
            if process.stdout:
                for line in process.stdout.strip().splitlines():
                    logger.info(f"[{script_name}] {line}")
            
            
            if process.returncode == 0:
                logger.info(f"Successfully finished: {script_path}")
                summary[script_path] = "Success"
            else:
                logger.error(f"Script {script_path} failed with exit code {process.returncode}")
                summary[script_path] = f"Failed (Exit code {process.returncode})"
                
        except Exception as e:
            logger.error(f"An exception occurred while running {script_path}: {e}")
            summary[script_path] = f"Failed (Exception: {e})"

    
    logger.info("=" * 50)
    logger.info("WORKFLOW SUMMARY")
    logger.info("=" * 50)
    for script_path, status in summary.items():
        if status == "Success":
            logger.info(f"[ OK ] {script_path}: {status}")
        else:
            logger.error(f"[FAIL] {script_path}: {status}")
    logger.info("=" * 50)
    logger.info("Benchmarking workflow completed.")

if __name__ == "__main__":
    main()
