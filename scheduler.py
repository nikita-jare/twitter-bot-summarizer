import subprocess
import logging
from datetime import datetime
import schedule
import time

# Path to the query list file
config_file = "query_list.txt"
scheduler_running = True

def execute_script(query, num_of_tweets=None):
    # Command to execute the main script with query and optional num_of_tweets
    if num_of_tweets is not None:
        cmd = f"python main.py '{query}' --num_of_tweets {num_of_tweets}"
    else:
        cmd = f"python main.py '{query}'"
        num_of_tweets = 1

    try:
        result = subprocess.run(cmd, shell=True, check=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE)


        # Check the return code
        if result.returncode == 0:
            # Remove the line from the config file upon successful execution
            # with open(config_file, "r") as f:
            #     lines = f.readlines()
            # with open(config_file, "w") as f:
            #     for line in lines:
            #         if not line.startswith(f"{query}"):
            #             f.write(line)

            print(f"YAYY! Execution successful for: '{query}', num_of_tweets: {num_of_tweets}")
            logging.info(f"YAYY! Execution successful for: '{query}', num_of_tweets: {num_of_tweets}")
        else:
            # There was an error
            logging.info(f"OH NO! Execution failed for: '{query}', num_of_tweets: {num_of_tweets} with error code {result.returncode} \n error:{result.stderr.decode()}")  
            print("Command failed with error code:", result.returncode)
            print("Standard Error:")
            print(result.stderr.decode())  # Decode and print stderr
    
    except subprocess.CalledProcessError as e:
        print(f"A-Oh!Execution failed for: '{query}', num_of_tweets: {num_of_tweets}")
        print(e)
        logging.error(f"A-Oh! Execution failed for: '{query}', num_of_tweets: {num_of_tweets}: {str(e)}")

# The job that we'll schedule to run every X minutes
def job():
    logging.basicConfig(filename='bot.log', level=logging.INFO, filemode='a')
    logging.info(f"[SCHEDULER STARTED] at {datetime.utcnow().isoformat()} UTC")

    with open(config_file, "r") as f:
        lines = f.readlines()
    
    if not lines:
        logging.info("[SCHEDULER] No more queries to process. Exiting.")
        global scheduler_running
        scheduler_running = False
        return

    line = lines[0]
    query, *num_of_tweets = line.strip().split(", ")
    num_of_tweets = int(num_of_tweets[0]) if num_of_tweets else None

    logging.info(f"[SCHEDULER] Processing query: '{query}', num_of_tweets: {num_of_tweets}")
    execute_script(query, num_of_tweets)

    # Remove the processed line from the config file
    with open(config_file, "w") as f:
        for remaining_line in lines[1:]:
            f.write(remaining_line)

    logging.info(f"[SCHEDULER] Waiting for 6 hours before the next query.")
    print(f"[SCHEDULER] Waiting for 6 hours before the next query.")

if __name__ == "__main__":
    # Schedule the job to run every 6 hours.
    schedule.every(6).minutes.do(job)
    while scheduler_running:
        schedule.run_pending()
        time.sleep(1)
