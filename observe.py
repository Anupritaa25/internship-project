import argparse
import time
import os
from unittest.mock import patch
import requests
from PIL import Image
from transformers import AutoModelForCausalLM, AutoProcessor
from transformers.dynamic_module_utils import get_imports
from datetime import datetime
import sys 
import subprocess

def fixed_get_imports(filename):
    """Work around for https://huggingface.co/microsoft/phi-1_5/discussions/72."""
    if not str(filename).endswith("/modeling_florence2.py"):
        return get_imports(filename)
    imports = get_imports(filename)
    imports.remove("flash_attn")
    return imports


with patch("transformers.dynamic_module_utils.get_imports", fixed_get_imports):

    model = AutoModelForCausalLM.from_pretrained("microsoft/Florence-2-base-ft", trust_remote_code=True)
    processor = AutoProcessor.from_pretrained("microsoft/Florence-2-base-ft", trust_remote_code=True)

#url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg?download=true"
#image = Image.open(requests.get(url, stream=True).raw)

def run_example(prompt, image):

    inputs = processor(text=prompt, images=image, return_tensors="pt")
    generated_ids = model.generate(
    input_ids=inputs["input_ids"],
    pixel_values=inputs["pixel_values"],
    max_new_tokens=1024,
    num_beams=3,
    )
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]

    parsed_answer = processor.post_process_generation(generated_text, task=prompt, image_size=(image.width, image.height))


    return parsed_answer


def process_image(image):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    image = Image.open(image)
    prompt = "<MORE_DETAILED_CAPTION>"
    caption = run_example(prompt, image)
    caption = caption[prompt]
    line1 = timestamp + " " + caption

    return line1


def main():

    parser = argparse.ArgumentParser(prog= 'observe.py', description= 'send a text description of each captured photo to an output file')
    parser.add_argument('-t',type = int, help = 'takes a photo every few seconds', default = 30)
    parser.add_argument('-o','--output', type = str, help = 'output file to which descriptions are written')
    parser.add_argument('-i', '--input', type = str, help = 'image file used as the source instead of webcam')

    args = parser.parse_args()
    print(args)

    #sys.exit(0)

#If output file is given, then caption and timestamp will be written to the output file
    if args.input:
        if args.output:
            file1 = open(args.output, "a")
            file1.write(process_image(args.input) + '\n')
            file1.close()

    #If it is not given, then print timestamp and caption as standard ouput
        else:
            print(process_image(args.input))

    else:
        while True:
            subprocess.run(['imagesnap', '-w', '1', 'snapshot.jpg'])
            if args.output:
                file1 = open(args.output, "a")
                file1.write(process_image('snapshot.jpg') + '\n')
                file1.close()
            else:
                print(process_image('snapshot.jpg'))
            time.sleep(args.t)


main()

        
        
        

    
        



    
    










