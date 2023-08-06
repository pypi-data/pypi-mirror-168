import json
import sys
import re

def do_cmd_clone_templates(ops, args):
    originals = []
    if args.name:
        originals = [args.name]
    elif args.infile:
        with open(args.infile, 'r') as f:
            for line in f:
                line = re.match('^[^#]*', line)[0]
                line = line.strip()
                if line != '':
                    originals.append(line)
    for original in originals:
        copyname = ""
        if args.copyname:
            copyname = args.copyname
        elif args.prefix:
            copyname = args.prefix + original
        do_cmd_clone_template(ops, original, copyname)

def do_cmd_clone_template(ops, name, copyname):
    matches = ops.get_templates(queryString=f'name:{name}')
    original = False
    for match in matches:
        if match['name'] == name:
            original = match
            break
    if not original:
        print(f'\nMonitoring template named {name} could not be found... skipping.\n')
    else:
        resp = ops.clone_template(original, copyname, original['description'])
        if 'templateId' not in resp:
            print(f'Clone of template {name} failed:\n{json.dumps(resp, indent=2, sort_keys=False)}')
        else:
            print(f'Successfully created new template {copyname} with uniqueId {resp["templateId"]}')