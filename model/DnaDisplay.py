
import base64
import json
import pymol

# Function to create a PDB-like file from a DNA sequence
def create_pdb_from_dna_sequence(dna_sequence, output_filename):
    header = "HEADER    DNA SEQUENCE"
    end_line = "END"

    # Create the PDB-like content
    pdb_content = [header]

    # Generate atom records for each base in the DNA sequence
    for index, base in enumerate(dna_sequence):
        atom_record = f"ATOM  {index + 1:4d}  {base} SEQ  {index + 1:4d}      {base.upper()}"
        pdb_content.append(atom_record)

    pdb_content.append(end_line)

    # Write the PDB-like content to a file
    with open(output_filename, 'w') as pdb_file:
        pdb_file.write('\n'.join(pdb_content))

    print(f"PDB-like file '{output_filename}' created.")

# Initialize PyMOL
pymol.pymol_argv = ['pymol', '-qc']
pymol.finish_launching()

# DNA sequence
dna_sequence = "ATGCTTCAGAAAGGTCTTACG"

# Output PDB file
output_filename = "dna_sequence.pdb"

# Create the PDB-like file
create_pdb_from_dna_sequence(dna_sequence, output_filename)

# Load and display the DNA structure in PyMOL
pymol.cmd.load(output_filename, "my_dna")
pymol.cmd.show("sticks", "my_dna")

# Save an image
image_filename = "dna_structure.png"
pymol.cmd.png(image_filename, width=800, height=600, dpi=300)

# Encode the image to base64
with open(image_filename, "rb") as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

# Close PyMOL
pymol.cmd.quit()

# Create a JSON response
response = {
    "image_base64": image_base64,
    "message": "DNA structure displayed."
}

# Convert the response to a JSON string
json_response = json.dumps(response)