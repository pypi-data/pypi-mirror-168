import json
import csv
import pandas as pd
import xlsxwriter
import time
import re
import sys

CUSTOM_ATTR_FILE_RESOURCE_FIELDS = ['client.uniqueId', 'client.name','id','name','resourceType']

def do_cmd_get_custom_attributes(ops,args):
    result = ops.get_objects(obtype="customAttributes")
    print(json.dumps(result, indent=2, sort_keys=False))

def do_cmd_make_custom_attr_file(ops, args):
    customattrs = ops.get_objects(obtype="customAttributes")
    if 'code' in customattrs:
        print("Error encountered retrieving custom attributes: %s" % customattrs)
        raise
    resources = None
    if args.search:
        resources = ops.get_objects(obtype="resourcesNewSearch", searchQuery=args.search, countonly=False)
    else:
        resources = ops.get_objects(obtype="resources", queryString=args.query, countonly=False)
    resourcedf = pd.json_normalize(resources)[CUSTOM_ATTR_FILE_RESOURCE_FIELDS]
    for attr in customattrs:
        resourcedf[attr['name']] = ''
        assigned_entities = ops.get_objects(obtype="assignedAttributeEntities", attrId=attr['id'])
        for ent in assigned_entities:
            if 'taggable' not in ent:
                continue
            resourcedf.loc[resourcedf['id'] == ent['taggable']['id'], attr['name']] = ent['customAttributeValue']['value']

    filename = args.filename
    if not filename:
        filename = 'customattrfile_' + args.env + '_' + time.strftime("%Y-%m-%d_%H%M%S")

    if not re.match(".*\.xlsx$", filename):
        filename = filename + ".xlsx"

    print("Creating export file: %s" % (filename))

    writer = pd.ExcelWriter(filename, engine="xlsxwriter")
    resourcedf.to_excel(writer, index=False, sheet_name='Custom Attrs')
    workbook  = writer.book
    worksheet = writer.sheets['Custom Attrs']
    for i, col in enumerate(resourcedf.columns):
        column_len = max(resourcedf[col].astype(str).str.len().max(), len(col) + 2)
        worksheet.set_column(i, i, column_len)

    bold = workbook.add_format({'bold': True})
    valsheet = workbook.add_worksheet('values')
    for i, attr in enumerate(customattrs):
        maxwidth = len(attr['name'])
        valsheet.write(0,i,attr['name'], bold)
        for j, attrval in enumerate(attr['customAttributeValues']):
            valsheet.write(j+1,i,attrval['value'])
            maxwidth = max(maxwidth, len(attrval['value']))
        valsheet.set_column(i, i, maxwidth+2)



    writer.save()

    print("done")

def do_cmd_import_custom_attr_file(ops, args):
    filename = args.filename
    if not re.match(".*\.xlsx$", filename):
        filename = filename + ".xlsx"

    df =  pd.read_excel(io=filename, engine="openpyxl", dtype=str)

    customattrs = ops.get_objects(obtype="customAttributes")
    if 'code' in customattrs:
        print("Error encountered retrieving custom attributes: %s" % customattrs)
        raise    

    attrinfo = {}
    for attr in customattrs:
        attrname = attr['name']
        attrinfo[attrname] = {}
        attrinfo[attrname]['id'] = attr['id']
        attrinfo[attrname]['client_id'] = attr['organization']['uniqueId']
        attrinfo[attrname]['values'] = {}
        for value in attr['customAttributeValues']:
            attrinfo[attrname]['values'][value['value']] = value['id']

    resourcedict = {}
    resources = ops.get_objects(obtype="resources")
    for resource in resources:
        resourcedict[resource['id']] = resource


    errors = []

    for required_col in CUSTOM_ATTR_FILE_RESOURCE_FIELDS:
        if required_col not in set(df.columns):
            errors.append('Required column "' + required_col + '" is missing from the spreadsheet.')
            continue
        if (len(df[df[required_col] == '']) > 0) or (len(df[pd.isna(df[required_col])]) > 0):
            errors.append('Column "' + required_col + '" has blank values which is not permitted.')
        if required_col=='id' and df['id'].duplicated().any():
            errors.append('Column "id" has duplicate values which is not permitted.')

    if 'id' in set(df.columns):
        for idx,row in df.iterrows():
            if pd.isna(row['id']) or row['id'] == '' or pd.isnull(row['id']):
                pass
            elif row['id'] not in resourcedict:
                errors.append('Resource id "' + row['id'] + '" specified in spreadsheet does not exist for the specified client.')
            else:
                if row['name'] != resourcedict[row['id']]['name']:
                    errors.append('Resource "' + row['id'] + '" name "' + row['name'] + '" in spreadsheet is different from name "' + resourcedict[row['id']]['name'] + '" on platform.')
                if row['resourceType'] != resourcedict[row['id']]['resourceType']:
                    errors.append('Resource "' + row['id'] + '" resourceType "' + row['resourceType'] + '" in spreadsheet is different from resourceType "' + resourcedict[row['id']]['resourceType'] + '" on platform.')
                if row['client.uniqueId'] != resourcedict[row['id']]['client']['uniqueId']:
                    errors.append('Resource "' + row['id'] + '" client.uniqueId "' + row['client.uniqueId'] + '" in spreadsheet is different from client.uniqueId "' + resourcedict[row['id']]['client']['uniqueId'] + '" on platform.')
                if row['client.name'] != resourcedict[row['id']]['client']['name']:
                    errors.append('Resource "' + row['id'] + '" client.name "' + row['client.name'] + '" in spreadsheet is different from client.name "' + resourcedict[row['id']]['client']['name'] + '" on platform.')

    for column in df.columns:
        if column in set(CUSTOM_ATTR_FILE_RESOURCE_FIELDS):
            continue
        if column not in attrinfo:
            errors.append('Column header "' + column + '" is not a valid custom attribute name for specified client.' )
        else:
            for val in df[column].unique():
                if pd.notna(val) and val != "" and str(val) not in attrinfo[column]['values']:
                    errors.append('Value "' + str(val) + '" specified for custom attribute "' + column + '" is not a valid value.')
    if len(errors) > 0:
        print("\nErrors exist in the spreadsheet.  No updates to the platform have been made, please correct these errors before commiting:\n")
        for i,error in enumerate(errors):
            print("%s  %s" % (str(i+1).rjust(5),error))
        print(" \n")
        sys.exit(1)

    elif not args.commit:
        print("No errors were found in the spreadsheet.  To apply the changes to the platform, rerun the command with the --commit option added.")
        sys.exit(0)

    updateresults = {
        "updatesuccess": 0,
        "updatefail": 0,
        "updatenotneeded": 0,
        "clearskipped": 0,
        "clearsuccess": 0,
        "clearfail": 0,
        "rawresults": [],
        "errors": []
    }

    for idx,resource in df.iterrows():
        for column in df.columns:
            if column in set(CUSTOM_ATTR_FILE_RESOURCE_FIELDS):
                continue
            elif pd.isnull(resource[column]) or pd.isna(resource[column]) or resource[column]=='' :
                if args.writeblanks:
                    if "tags" in resourcedict[resource['id']] and any(attr['name']==column for attr in resourcedict[resource['id']]['tags']):
                        # There is a value and we need to remove it
                        pass
                    else:
                        # There is already no value so nothing to remove
                        updateresults['clearskipped'] +=1
                else:
                    updateresults['clearskipped'] +=1
                    continue
            elif "tags" in resourcedict[resource['id']] and any(attr['name']==column and attr['value']==resource[column] for attr in resourcedict[resource['id']]['tags']):
                # It already has the same value for this attr, no need to update
                updateresults['rawresults'].append({
                    "rownum": idx+1,
                    "resourceid": resource['id'],
                    "attr_name": column,
                    "attr_value": resource[column],
                    "attr_id": attrinfo[column]['id'],
                    "attr_value_id": attrinfo[column]['values'][resource[column]],
                    "action": "update not needed"
                })
                updateresults['updatenotneeded'] +=1
                continue
            else:
                # It has no value or a different value for this attr so we need to update
                result = ops.set_custom_attr_on_devices(attrinfo[column]['id'], attrinfo[column]['values'][str(resource[column])], resource['id'])
                updateresults['rawresults'].append({
                    "rownum": idx+1,
                    "resourceid": resource['id'],
                    "attr_name": column,
                    "attr_value": resource[column],
                    "attr_id": attrinfo[column]['id'],
                    "attr_value_id": attrinfo[column]['values'][str(resource[column])],
                    "action": "updated"
                })
                if result['successCount'] == 1:
                    updateresults['updatesuccess'] +=1
                else:
                    updateresults['updatefail'] +=1
                    updateresults['errors'].append({
                        "rownum": idx+1,
                        "resourceid": resource['id'],
                        "attr_name": column,
                        "attr_value": resource[column],
                        "attr_id": attrinfo[column]['id'],
                        "attr_value_id": attrinfo[column]['values'][str(resource[column])],
                        "action": "updatefail",
                        "response": result
                    })                    
    
    
    print("done") 