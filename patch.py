import os
import shutil

def reconstruct_and_replace(file_b_path, file_c_path):
    backup_path = file_b_path + ".backup"

    # Step 1: Make a backup
    if not os.path.exists(backup_path):
        shutil.copyfile(file_b_path, backup_path)
        print(f"Backup created: {backup_path}")
    else:
        raise FileExistsError(f"Backup already exists: {backup_path}")

    # Step 2: Read data
    with open(backup_path, 'rb') as fb, open(file_c_path, 'rb') as fc:
        data_b = fb.read()
        data_c = fc.read()

    if len(data_b) < len(data_c):
        raise ValueError("Backup file is shorter than diff file — cannot safely reconstruct.")

    # Step 3: Reconstruct
    result = bytearray()
    for i in range(len(data_c)):
        result.append(data_b[i] if data_c[i] == 0x00 else data_c[i])

    # Append any extra from the backup (optional)
    if len(data_b) > len(data_c):
        result.extend(data_b[len(data_c):])

    # Step 4: Overwrite file_b.bin with reconstructed file_a
    with open(file_b_path, 'wb') as fout:
        fout.write(result)

    print(f"Reconstructed file written to: {file_b_path}")


# Example usage
reconstruct_and_replace("resources.assets", "tokipona.bin")
