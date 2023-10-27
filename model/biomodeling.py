import pymol
import base64
import json


# Function to create a PDB-like file from a nucleic acid sequence
def create_pdb_from_nucleic_acid_sequence(sequence, output_filename, is_rna=False):
    header = "HEADER    RNA SEQUENCE" if is_rna else "HEADER    DNA SEQUENCE"
    end_line = "END"


    # Create the PDB-like content
    pdb_content = [header]


    # Generate atom records for each base in the sequence
    for index, base in enumerate(sequence):
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


# Function to convert DNA to RNA
def dna_to_rna(dna_sequence):
    return dna_sequence.replace('T', 'U')


# Convert DNA to RNA
rna_sequence = dna_to_rna(dna_sequence)


# Output PDB files
dna_output_filename = "dna_structure.pdb"
rna_output_filename = "rna_structure.pdb"


# Create the PDB-like files for DNA and RNA
create_pdb_from_nucleic_acid_sequence(dna_sequence, dna_output_filename)
create_pdb_from_nucleic_acid_sequence(rna_sequence, rna_output_filename, is_rna=True)


# Save an image of the DNA visualization
dna_image_filename = "dna_structure.png"
pymol.cmd.png(dna_image_filename, width=800, height=600, dpi=300)  # Save the DNA visualization as a PNG image


# Load and display the RNA structure in PyMOL
pymol.cmd.load(rna_output_filename, "rna_structure")
pymol.cmd.show("sticks", "rna_structure")
pymol.cmd.zoom("rna_structure", buffer=10)


# Save an image of the RNA visualization
rna_image_filename = "rna_structure.png"
pymol.cmd.png(rna_image_filename, width=800, height=600, dpi=300)  # Save the RNA visualization as a PNG image


# Encode the DNA image to base64
with open(dna_image_filename, "rb") as dna_image_file:
    dna_image_base64 = base64.b64encode(dna_image_file.read()).decode("utf-8")


# Encode the RNA image to base64
with open(rna_image_filename, "rb") as rna_image_file:
    rna_image_base64 = base64.b64encode(rna_image_file.read()).decode("utf-8")


# Create a JSON structure to contain the base64-encoded images
image_data = {
    "dna_image_base64": dna_image_base64,
    "rna_image_base64": rna_image_base64,
}


# Convert the image data to a JSON string
image_data_json = json.dumps(image_data)


# Print or use image_data_json as needed



