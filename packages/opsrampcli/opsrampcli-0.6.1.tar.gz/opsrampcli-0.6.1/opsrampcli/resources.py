import json

def do_cmd_get_resources(ops,args):
    if args.search:
        result = ops.get_objects(obtype="resourcesNewSearch", searchQuery=args.search, countonly=args.count)
    else:
        result = ops.get_objects(obtype="resources", queryString=args.query, countonly=args.count)

    if args.delete:
        confirm_delete = 'NO'
        confirm_delete = input(f'This will result in the deletion of {len(result)} resources.  Enter YES (upper case) to confirm deletion or enter anything else to just print a list of the resources that would be deleted: ')
    
        if confirm_delete == 'YES':
            for (idx, resource) in enumerate(result):
                print(f'Deleting resource #{idx+1} - {resource["name"]} ({resource["resourceType"]}) with uniqueId {resource["id"]}')
                try:
                    print(ops.delete_resource(resource['id']))
                except Exception as e:
                    print(e)
        else:
            print(json.dumps(result, indent=2, sort_keys=False))

    elif args.manage:
        confirm_manage = 'NO'
        confirm_manage = input(f'This will result in managing {len(result)} resources.  Enter YES (upper case) to confirm or enter anything else to just print a list of the resources that would be managed: ')
    
        if confirm_manage == 'YES':
            for (idx, resource) in enumerate(result):
                print(f'Managing resource #{idx+1} - {resource["name"]}')
                try:
                    print(ops.do_resource_action("manage", resource['id']))
                except Exception as e:
                    print(e)

        else:
            print(json.dumps(result, indent=2, sort_keys=False))        


    else:
         print(json.dumps(result, indent=2, sort_keys=False))