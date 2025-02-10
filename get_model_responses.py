from llama_index.llms.ollama import Ollama
import csv
import random

llm = Ollama(model="llama3.2:latest")

def shuffle_csv(input_file, output_file, seed_value=42):
    """
    Reads a CSV file, shuffles the rows, and writes them to a new file.
    
    :param input_file: Path to the input CSV file.
    :param output_file: Path to the output CSV file where shuffled rows will be written.
    :param seed_value: The seed for the random shuffling to ensure reproducibility (default is 42).
    """
    # Read all rows from the input CSV file
    with open(input_file, mode="r", encoding="utf-8") as f_in:
        csv_reader = csv.reader(f_in)
        rows = list(csv_reader)  # Read all rows into a list
    
    # Shuffle the rows using the fixed seed for reproducibility
    random.seed(seed_value)
    random.shuffle(rows)
    
    # Write the shuffled rows to the new output CSV file
    with open(output_file, mode="w", newline="", encoding="utf-8") as f_out:
        csv_writer = csv.writer(f_out)
        csv_writer.writerows(rows)  # Write all rows to the output file

    print(f"Rows have been shuffled and written to {output_file}.")


def get_responses(input_file, output_file, append=False, max_queries=5):
    write_mode = "a" if append else "w"

    with open(output_file, write_mode, newline="", encoding="utf-8") as f_out, open(input_file, encoding="utf-8") as f_in:
        csv_writer = csv.writer(f_out, delimiter=",")
        csv_reader = csv.reader(f_in)

        # rows = list(csv_reader)
        # random.seed(42)
        # random.shuffle(rows)

        # Optionally write headers if needed
        csv_writer.writerow(["Prompt", "Response"])
        
        for i, row in enumerate(csv_reader, 1):
            prompt = row[0]
            response = llm.complete(prompt)
            print(f"Prompt: {prompt}")
            print(f"Response: {response.text[:400]}")
            csv_writer.writerow([prompt, response.text])
            if i == max_queries:
                break

if __name__ == "__main__":
    # get_responses("shuffled_prompts.csv", "llama3.2_base_responses.csv", max_queries=50)
    get_responses("new_data.csv", "llama3.2_base_responses.csv", append=True, max_queries=10)