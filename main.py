"""
Execute the poem generator. 
"""


from src.image_analyzer import ImageObjectDetection
from src.poem import VillanellePoem
from src.lang_utility import LanguageUtility
from src.model import SemanticSearchModel
from utils.file_io import write_to_file, read_from_file, read_from_object

img_detection = ImageObjectDetection()
# smtic_model = SemanticSearchModel()
# lang_util = LanguageUtility("model/glove.6B.50d.txt")
image_out = img_detection.get_img_output_layers(
    "data/images/frank_ocean_bike.jpeg")
objs_detected = img_detection.get_label(image_out)
print(objs_detected)
# objs_detected = ["car", "candy", "love", "food"]
# complete_queries = lang_util.gen_quality_queries(objs_detected)
# poem = VillanellePoem(complete_queries, lang_util, smtic_model)

# poems_generated = 0
# while True:
#     ask_input = input("Enter command: ")
#     if ask_input == "gen":
#         poems_generated += 1
#         poem.gen_full_poem()
#         print(poem)
#         read_from_object(poem)
#     elif ask_input == "read":
#         file_path = input("Enter the file path: ")
#         read_from_file(file_path)
#     elif ask_input == "save":
#         write_to_file(poem, str(poems_generated))
