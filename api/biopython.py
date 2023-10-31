from flask import Blueprint, jsonify
from flask_restful import Api, Resource
import pandas as pd
import os
import requests
from flask import request
from Bio.Seq import Seq
from PIL import Image, ImageDraw
import json
import io
import base64

biopython_api = Blueprint('biopython_api', __name__, url_prefix='/api/biopython')
api = Api(biopython_api)

class BioPythonAPI:
    class _ConvertSequence(Resource):
        def post(self):
            data = request.get_json()
            dna_sequence = data.get('dna_sequence')

            def dna_to_rna(dna_sequence):
                dna_seq = Seq(dna_sequence)
                rna_seq = dna_seq.transcribe()
                return str(rna_seq)

            def rna_to_amino_acids(rna_sequence):
                rna_seq = Seq(rna_sequence)
                amino_acids = rna_seq.translate()
                return str(amino_acids)

            def create_images(dna_sequence, rna_sequence, amino_acids_sequence):
                dna_seq = Seq(dna_sequence)
                rna_seq = Seq(rna_sequence)
                amino_acids_seq = Seq(amino_acids_sequence)

                dna_image = Image.new('RGB', (300, 100), (255, 255, 255))
                dna_drawer = ImageDraw.Draw(dna_image)
                dna_drawer.text((10, 40), str(dna_seq), fill=(0, 0, 0))

                rna_image = Image.new('RGB', (300, 100), (255, 255, 255))
                rna_drawer = ImageDraw.Draw(rna_image)
                rna_drawer.text((10, 40), str(rna_seq), fill=(0, 0, 0))

                amino_acids_image = Image.new('RGB', (300, 100), (255, 255, 255))
                amino_acids_drawer = ImageDraw.Draw(amino_acids_image)
                amino_acids_drawer.text((10, 40), str(amino_acids_seq), fill=(0, 0, 0))

                return dna_image, rna_image, amino_acids_image

            # Convert DNA to RNA
            rna_sequence = dna_to_rna(dna_sequence)

            # Convert RNA to Amino Acids
            amino_acids_sequence = rna_to_amino_acids(rna_sequence)

            # Create DNA, RNA, and Amino Acid images
            dna_image, rna_image, amino_acids_image = create_images(dna_sequence, rna_sequence, amino_acids_sequence)

            dna_image_bytes = io.BytesIO()
            dna_image.save(dna_image_bytes, format='PNG')
            rna_image_bytes = io.BytesIO()
            rna_image.save(rna_image_bytes, format='PNG')
            amino_acids_image_bytes = io.BytesIO()
            amino_acids_image.save(amino_acids_image_bytes, format='PNG')

            dna_image_base64 = base64.b64encode(dna_image_bytes.getvalue()).decode('utf-8')
            rna_image_base64 = base64.b64encode(rna_image_bytes.getvalue()).decode('utf-8')
            amino_acids_image_base64 = base64.b64encode(amino_acids_image_bytes.getvalue()).decode('utf-8')

            image_data = {
                "dna_image_base64": dna_image_base64,
                "rna_image_base64": rna_image_base64,
                "amino_acids_image_base64": amino_acids_image_base64
            }

            return jsonify(image_data)

    api.add_resource(_ConvertSequence, '/convert_sequence')

if __name__ == "__main__":
    # Modify your test code as needed
    server = "http://127.0.0.1:8006"  # Replace with your server URL
    url = server + "/api/biopython"
    responses = []  # Responses list

    # Test code
    # Modify the following code according to your test scenario
    # responses.append(
    #     requests.get(url)  #read data
    # )
    responses.append(
        requests.post(url + "/convert_sequence")  # Create new data (if needed)
    )

    for response in responses:
        print(response)
        try:
            print(response.json())
        except:
            print("Unknown error")
