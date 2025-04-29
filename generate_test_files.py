import os

def generate_test_file(file_path: str, num_lines: int, include_search_string: str = None):
    """Generates a file with a given number of lines. Optionally includes a known search string."""
    with open(file_path, 'w') as f:
        for i in range(num_lines):
            f.write(f"random_line_{i}\n")
        if include_search_string:
            f.write(f"{include_search_string}\n")  #I  Insert a searchable line at the end

def prepare_all_test_files(output_dir: str, search_string: str = "test_match_string"):
    """Generates multiple test files of varying sizes for performance testing."""
    os.makedirs(output_dir, exist_ok=True)
    sizes = [10_000, 50_000, 100_000, 250_000, 500_000, 1_000_000]
    
    for size in sizes:
        file_name = f"{size}_lines.txt"
        path = os.path.join(output_dir, file_name)
        print(f"Generating file: {path}")
        generate_test_file(path, size, include_search_string=search_string)

if __name__ == "__main__":
    prepare_all_test_files(output_dir="test_data")
