import json
import pathlib

from app.models import *

#####################
#####################
# CONFIGURATION VARIABLES, CHANGE TO USE THIS SCRIPT

VALIDATION_ID_TO_DUMP = 1

####################
####################


def run():
    answer_objs = Answer.objects.filter(validation_id=VALIDATION_ID_TO_DUMP)
    final_obj = {
        "all_answers": [],
        "per_user": {},
        "per_item": {}
    }
    for answer in answer_objs:
        username = str(answer.user)
        final_obj["all_answers"].append({
            "user": username,
            "item_id": answer.item_id,
            "item_info": answer.item.payload,
            "data": answer.answer_data
        })
        if answer.item_id not in final_obj["per_item"]:
            final_obj["per_item"][answer.item_id] = []
        final_obj["per_item"][answer.item_id].append({
            "user": username,
            "item_info": answer.item.payload,
            "data": answer.answer_data
        })
        if username not in final_obj["per_user"]:
            final_obj["per_user"][username] = []
        final_obj["per_user"][username].append({
            "item_id": answer.item_id,
            "item_info": answer.item.payload,
            "data": answer.answer_data
        })

    output_path = pathlib.Path("answers.json")
    with open(output_path, "w") as jsonfile:
        json.dump(final_obj, jsonfile)