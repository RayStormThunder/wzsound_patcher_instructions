import os
import struct

VERSION = "1.1.8"

def extract_rwsd_files_from_all_brsar(folder_path):
    print(f"RWSD Extractor - Version {VERSION}")

    # Automatically look for all .brsar files in the folder
    brsar_files = [file for file in os.listdir(folder_path) if file.endswith('.brsar')]
    
    if not brsar_files:
        print("No .brsar files found in the folder.")
        return
    
    for brsar_file in brsar_files:
        print(f"Found .brsar file: {brsar_file}")
        brsar_file_path = os.path.join(folder_path, brsar_file)

        # Create a unique extraction folder for each .brsar file
        base_filename = os.path.splitext(brsar_file)[0]
        extraction_folder = os.path.join(folder_path, f"{base_filename}_Extract_RWSD")
        
        if not os.path.exists(extraction_folder):
            os.makedirs(extraction_folder)
            print(f"Created extraction folder: {extraction_folder}")

        with open(brsar_file_path, 'rb') as f:
            data = f.read()

        # Start the search at the given offset and limit to first RWSD
        extract_rwsd_files(data, extraction_folder, start_offset=0x0, search_first_only=False)

def extract_rwsd_files(data, extraction_folder, start_offset=0, search_first_only=False):
    signature = "RWSD"
    signature_bytes = signature.encode('ascii')
    count = 0
    offset = start_offset
    a = 0  # Initialize the A variable, which will be used only if RBNK is found

    while offset < len(data):
        pos = data.find(signature_bytes, offset)
        if pos == -1:
            break

        print(f"Found {signature} at: {hex(pos)}")

        x_pos = pos + 0x8
        x = struct.unpack_from('>I', data, x_pos)[0]
        print(f"At offset {hex(x_pos)}: X Dec = {x}, Hex X = {hex(x)}")

        label_pos = pos + x
        label = data[label_pos:label_pos + 4].decode('ascii', errors='ignore')
        print(f"Found '{label}' at {hex(label_pos)}")  # Print the label before adding any offsets

        is_rseq = False
        a = 0  # Reset A for each new RWSD section

        if label == "RSEQ":
            print(f"Found 'RSEQ' at {hex(label_pos)}, moving forward 0x8 bytes.")
            is_rseq = True
            y_pos = label_pos + 0x8
            y = struct.unpack_from('>I', data, y_pos)[0]
            print(f"At offset {hex(y_pos)}: Y Dec = {y}, Hex Y = {hex(y)}")

            # Look for RBNK directly
            rbnk_pos = pos + x + y
            rbnk_label = data[rbnk_pos:rbnk_pos + 4].decode('ascii', errors='ignore')
            print(f"Found '{rbnk_label}' at {hex(rbnk_pos)}")

            if rbnk_label == "RBNK":
                print(f"Found 'RBNK' at {hex(rbnk_pos)}, moving forward 0x8 bytes.")
                # Move 8 bytes forward and add the next 4 bytes to the offset for A
                rbnk_offset_pos = rbnk_pos + 0x8
                a = struct.unpack_from('>I', data, rbnk_offset_pos)[0]
                print(f"At offset {hex(rbnk_offset_pos)}: A Dec = {a}, Hex A = {hex(a)}")

                # Correct the position for Z based on X, Y, and A, and move 8 bytes forward
                z_pos = pos + x + y + a + 0x8  # Adding 0x8 after calculating X + Y + A
            else:
                z_pos = pos + x + y + 0x8

            z = struct.unpack_from('>I', data, z_pos)[0]
            print(f"At offset {hex(z_pos)}: Z Dec = {z}, Hex Z = {hex(z)}")
            file_size = x + y + z + a

        elif label == "RWAR":
            print(f"Found 'RWAR' at {hex(label_pos)}, skipping Y.")
            y = 0
            z_pos = pos + x + 0x8
            z = struct.unpack_from('>I', data, z_pos)[0]
            print(f"At offset {hex(z_pos)}: Z Dec = {z}, Hex Z = {hex(z)}")
            file_size = x + z

        elif label == signature:
            print(f"Found '{signature}' at {hex(label_pos)}, skipping Y and Z.")
            file_size = x

        else:
            print(f"Unknown label '{label}' at {hex(label_pos)}, skipping this {signature}.")
            offset = pos + 4
            continue

        section_data = data[pos:pos + file_size]
        rwav_count = section_data.count(b'RWAV')
        if rwav_count == 0:
            print(f"No RWAV found in this {signature}, skipping.")
            offset = pos + file_size
            continue

        print(f"Found {rwav_count} RWAV occurrences.")

        file_data = section_data

        count += 1
        rwav_suffix = f"{rwav_count:03d}"
        file_suffix = "_Q" if is_rseq else "_D"
        output_filename = os.path.join(extraction_folder, f'{signature}_{count}_{rwav_suffix}{file_suffix}.brwsd')
        with open(output_filename, 'wb') as out_file:
            out_file.write(file_data)
        print(f"Extracted {signature} file: {output_filename}")

        offset = pos + file_size

        if search_first_only:
            break

    print(f"Extracted {count} {signature} files in total.")

    while check_for_duplicate_files(extraction_folder):
        print("Duplicates found and deleted, re-checking...")

    # Fix the files that end with _Q
    fix_broken_rseq_files(extraction_folder)



def fix_broken_rseq_files(folder_path):
    """Fixes files ending with '_Q' by deleting data between RSEQ and RWAR and inserting new data."""
    for filename in os.listdir(folder_path):
        if filename.endswith('_Q.brwsd'):
            file_path = os.path.join(folder_path, filename)
            print(f"Fixing file: {file_path}")

            with open(file_path, 'rb+') as f:
                data = f.read()

                rseq_pos = data.find(b'RSEQ')
                rwar_pos = data.find(b'RWAR')

                if rseq_pos == -1 or rwar_pos == -1 or rseq_pos >= rwar_pos:
                    print(f"Skipping {filename}: Invalid RSEQ or RWAR positions.")
                    continue

                # Delete the data between RSEQ and RWAR
                fixed_data = data[:rseq_pos] + data[rwar_pos:]
                f.seek(0)
                f.write(fixed_data)
                f.truncate()

                # Count RWAV files after RWAR
                rwav_count = fixed_data[rwar_pos:].count(b'RWAV')
                print(f"RWAV count: {rwav_count}")

                # Prepare the data to insert
                insert_data = bytearray()
                insert_data += b'LABL'
                insert_data += struct.pack('>I', (16 * rwav_count) + 16)
                insert_data += struct.pack('>I', rwav_count)

                # Add the calculated offsets
                offset_value = (4 * rwav_count) + 12
                for i in range(rwav_count):
                    insert_data += struct.pack('>I', offset_value)
                    offset_value += 12

                # Insert repeating pattern for each RWAV file
                for i in range(rwav_count):
                    insert_data += struct.pack('>I', i)  # Loop index
                    insert_data += struct.pack('>I', 4)
                    insert_data += b'TEST'

                # Insert final 4 bytes of "00"
                insert_data += b'\x00' * 4

                # Insert the new data at the position of RSEQ
                final_data = fixed_data[:rseq_pos] + insert_data + fixed_data[rseq_pos:]
                f.seek(0)
                f.write(final_data)
                f.truncate()

                print(f"Fixed file: {file_path}")

def check_for_duplicate_files(folder):
    files_by_size = {}
    files_to_remove = set()

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            if file_size not in files_by_size:
                files_by_size[file_size] = []
            files_by_size[file_size].append(file_path)

    any_deleted = False
    for file_list in files_by_size.values():
        if len(file_list) > 1:
            for i in range(len(file_list) - 1):
                for j in range(i + 1, len(file_list)):
                    match_percentage = compare_files(file_list[i], file_list[j])
                    print(f"Comparing {file_list[i]} and {file_list[j]}: {match_percentage:.2f}% match")
                    if match_percentage > 75:
                        higher_numbered_file = max(file_list[i], file_list[j], key=lambda f: int(f.split('_')[-2]))
                        print(f"Marking {higher_numbered_file} for deletion")
                        files_to_remove.add(higher_numbered_file)

    for file_to_remove in files_to_remove:
        try:
            os.remove(file_to_remove)
            print(f"Deleted duplicate file: {file_to_remove}")
            any_deleted = True
        except FileNotFoundError as e:
            print(f"Error: {e}")

    return any_deleted

def compare_files(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        f1_data = f1.read()
        f2_data = f2.read()

    min_len = min(len(f1_data), len(f2_data))
    match_count = sum(b1 == b2 for b1, b2 in zip(f1_data[:min_len], f2_data[:min_len]))
    return (match_count / min_len) * 100 if min_len > 0 else 0

if __name__ == "__main__":
    current_folder = os.path.dirname(os.path.abspath(__file__))
    extract_rwsd_files_from_all_brsar(current_folder)
