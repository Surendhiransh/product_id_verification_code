import re
import pandas as pd

capacity_map = {"512": "512MB", "1": "1GB", "2": "2GB", "4": "4GB", "8": "8GB", "16": "16GB", "24": "24GB", "32": "32GB", "64": "64GB", "128": "128GB", "256": "256GB", "96":"96GB", "164": "164GB", "48": "48GB","296":"296GB"}
memory_type_map = {"D": "DDR", "D2": "DDR2", "D3": "DDR3", "D4": "DDR4","D5": "DDR5", "D6": "DDR6"}
ecc_map = {"E": "ECC", "N": "Non-ECC"}
dimm_type_map = {"S": "SODIMM", "U": "UDIMM", "R": "RDIMM", "L": "LRDIMM", "F": "FBDIMM"}
ranks_map = {"8": "8", "4": "4", "3": "3", "2": "2", "1": "1"}
speed_map = {"266": "266", "333": "333", "400": "400", "533": "533", "667": "667", "800": "800", "1066": "1066", "1333": "1333", "1600": "1600", "1866": "1866", "2133": "2133", "2400": "2400", "2666": "2666", "2933": "2933", "3200": "3200","4800":"4800", "5600":"5600", "6000":"6000", "6400":"6400", "7200":"7200", "8000":"8000", "9600":"9600"}
voltage_map = {"1.2": "1.2V", "1.35": "1.35V", "1.5": "1.5V", "1.8": "1.8V", "1.1":"1.1V"}
height_map = {"S": "STD", "V": "VLP"}
rank_width_map = {"1": "1","2": "2","4": "4","8": "8","16": "16"}
qty_map = {"1": "1","2": "2","3": "3","4": "4","5": "5","6": "6","7": "7","8": "8","9": "9"}

# Regex pattern to split product_id as requested
pattern = re.compile(r'^(?P<capacity>\d+)(?P<memory_type>[A-Za-z]+\d*)(?P<ecc>[EN])(?P<dimm_type>[A-Z])(?P<ranks>\d)(?P<rank_width>\d)(?P<speed>\d{3,4})(?P<voltage>\d{2})(?P<height>[A-Z])(?P<qty>\d)$')


def validate_product_id(product_id, memory_spec):
    # Strip leading/trailing spaces
    product_id = product_id.strip()
    # Check if product_id matches the expected format 
    match = pattern.match(product_id)
    if not match:
        print(f"Invalid Product ID format: {product_id}")
        return "Invalid"

    parts = match.groups()

    # Extract individual parts
    capacity, mem_type, ecc, dimm_type, ranks, rank_width, speed, voltage_code, height, qty = parts
    voltage = f"{voltage_code[0]}.{voltage_code[1]}V"  # Convert voltage code to voltage format
    # Validation against maps
    if capacity not in capacity_map:
        print(f"Invalid capacity: {capacity}")
        return "Invalid"

    if mem_type not in memory_type_map:
        print(f"Invalid memory type: {mem_type}")
        return "Invalid"

    if ecc not in ecc_map:
        print(f"Invalid ECC type: {ecc}")
        return "Invalid"

    if dimm_type not in dimm_type_map:
        print(f"Invalid DIMM type: {dimm_type}")
        return "Invalid"

    if ranks not in ranks_map:
        print(f"Invalid ranks: {ranks}")
        return "Invalid"

    if speed not in speed_map:
        print(f"Invalid speed: {speed}")
        return "Invalid"
    
    voltage_key = f"{voltage_code[0]}.{voltage_code[1]}"
    if voltage_key not in voltage_map:
        print(f"Invalid voltage: {voltage_key}")
        return "Invalid"
    
    if height not in height_map:
        print(f"Invalid height: {height}")
        return "Invalid"

    if rank_width not in rank_width_map:
        print(f"Invalid rank width: {rank_width}")
        return "Invalid"

    if qty not in qty_map:
        print(f"Invalid quantity: {qty}")
        return "Invalid"

    # Validate against memory_spec dictionary
    try:
        memory_spec_dict = eval(memory_spec)
    except Exception as e:
        print(f"Invalid memory_spec: {e}")
        return "Invalid"

    checks = [
        (memory_spec_dict.get('capacity') == capacity_map[capacity], f"Capacity mismatch: {memory_spec_dict.get('capacity')} != {capacity_map[capacity]}"),
        (memory_spec_dict.get('memory_type') == memory_type_map[mem_type], f"Memory type mismatch: {memory_spec_dict.get('memory_type')} != {memory_type_map[mem_type]}"),
        (memory_spec_dict.get('ecc') == ecc_map[ecc], f"ECC mismatch: {memory_spec_dict.get('ecc')} != {ecc_map[ecc]}"),
        (memory_spec_dict.get('dimm_type') == dimm_type_map[dimm_type], f"DIMM type mismatch: {memory_spec_dict.get('dimm_type')} != {dimm_type_map[dimm_type]}"),
        (str(memory_spec_dict.get('ranks')) == ranks_map[ranks], f"Ranks mismatch: {memory_spec_dict.get('ranks')} != {ranks_map[ranks]}"),
        (str(memory_spec_dict.get('speed')).startswith(speed), f"Speed mismatch: {memory_spec_dict.get('speed')} does not start with {speed}"),
        (memory_spec_dict.get('voltage') == voltage_map[voltage_key], f"Voltage mismatch: {memory_spec_dict.get('voltage')} != {voltage_map[voltage_key]}"),
        (memory_spec_dict.get('height') == height_map[height], f"Height mismatch: {memory_spec_dict.get('height')} != {height_map[height]}"),
        (str(memory_spec_dict.get('rank_width')) == rank_width_map[rank_width], f"Rank width mismatch: {memory_spec_dict.get('rank_width')} != {rank_width_map[rank_width]}"),
        (str(memory_spec_dict.get('qty')) == qty_map[qty], f"Quantity mismatch: {memory_spec_dict.get('qty')} != {qty_map[qty]}"),
    ]

    for condition, error_msg in checks:
        if not condition:
            print(error_msg)
            return "Invalid"

    return "Valid"

# File paths
csv_file_path = 'E:\\Pytest\\cisco_host_parts-encoded.csv'
output_file_path = 'output1.csv'

# Read the CSV file
df = pd.read_csv(csv_file_path)

# Apply validation to each row in the dataframe
df['product_id_validation'] = df.apply(lambda row: validate_product_id(row['Product_id'], row['memory_specification']), axis=1)

# Show the results of validation
print(df[['Product_id', 'product_id_validation']].head())

# Save the results to a new CSV file
df.to_csv(output_file_path, index=False)
