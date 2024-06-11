MODEL_FULL_PATH = "F:/NOVELAI/astolfo_mix/sdxl/raw/_x112-heartOfAppleXL_v30.safetensors"
OUTPUT_JSON = "./logs/result.json"

import struct
import json

# Return the metadata dict
def parse_safetensors_metadata(file_path):
    # Open the file in binary mode
    with open(file_path, 'rb') as file:
        length_of_header_bytes = file.read(8)
        # Interpret the bytes as a little-endian unsigned 64-bit integer
        length_of_header = struct.unpack('<Q', length_of_header_bytes)[0]
        header_bytes = file.read(length_of_header)       
        metadata = json.loads(header_bytes)                
        #header = json.loads(header_bytes.decode('utf-8'))
        #return header
        return metadata["__metadata__"]  if "__metadata__" in metadata else metadata
      
dict1 = parse_safetensors_metadata(MODEL_FULL_PATH)

with open(OUTPUT_JSON, "w") as out_file:
    json.dump(dict1, out_file, indent = 4) 
