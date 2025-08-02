#!/usr/bin/env python3

import os
import json
import subprocess

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "default_rules.json")

def apply_rules():
    with open(CONFIG_PATH) as f:
        rules = json.load(f)
    
    for rule_file in rules["rule_files"]:
        print(f"Applying: {rule_file}")
        subprocess.run(["nft", "-f", rule_file], check=True)

if __name__ == "__main__":
    apply_rules()
