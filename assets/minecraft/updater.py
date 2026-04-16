import json, os
from pathlib import Path

p = Path("models/item/")
for x in p.rglob("*"):
    if f"{x}".endswith(".json"):
        name = f"{x}"[:-5]
        print(name)
        new_data = {
          "model": {
            "type": "range_dispatch",
            "property": "custom_model_data",
            "entries": [],
            "fallback": {
              "type": "model",
              "model": f"item/{os.path.basename(f"{x}")[:-5]}"
            }
          },
          "oversized_in_gui": True
        }
        data = {}
        with open(f"{x}", "r") as file:
            data = json.load(file)
            file.close()
        if not("overrides" in data.keys()):
            print(name, "i cant")
            continue
        overrides = data["overrides"]
        for predicate in overrides:
            if "custom_model_data" in predicate["predicate"].keys():
                if "shield" in name:
                    entry = {
                        "threshold": predicate["predicate"]["custom_model_data"],
                        "model": {
                            "type": "minecraft:condition",
                            "on_false": {
                                "type": "minecraft:range_dispatch",
                                "property": "minecraft:custom_model_data",
                                "entries": [
                                {
                                    "threshold": predicate["predicate"]["custom_model_data"],
                                    "model": {
                                        "type": "model",
                                        "model": predicate["model"],
                                        "tints": [
                                        {
                                          "type": "minecraft:dye",
                                          "default": [1, 1, 1]
                                        }
                                        ]
                                    }
                                }
                                ]
                            },
                            "on_true": {
                                "type": "minecraft:range_dispatch",
                                "property": "minecraft:custom_model_data",
                                "entries": [
                                {
                                    "threshold": predicate["predicate"]["custom_model_data"],
                                    "model": {
                                        "type": "model",
                                        "model": predicate["model"] + "_use",
                                        "tints": [
                                        {
                                          "type": "minecraft:dye",
                                          "default": [1, 1, 1]
                                        }
                                        ]
                                    }
                                }
                                ]
                            },
                            "property": "minecraft:using_item"
                        }
                    }
                    print("shield found")
                else:
                    entry = {
                        "threshold": predicate["predicate"]["custom_model_data"],
                        "model": {
                            "type": "model",
                            "model": predicate["model"],
                            "tints": [
                            {
                              "type": "minecraft:dye",
                              "default": [1, 1, 1]
                            }
                            ]
                        }
                    }
                new_data["model"]["entries"].append(entry)
        with open(f"items/{os.path.basename(f"{x}")}", "w") as file:
            json.dump(new_data, file, indent=2)
            file.close()
