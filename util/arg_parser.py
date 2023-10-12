EIC_CODE = '10YFI-1--------U'

def parse_args(args):
    # read command line argument for Domain EIC Code
    if len(args) > 1:
        eic_code = args[1]
    else:
        eic_code = EIC_CODE

    # read command line argument for difference from UTC in hours
    if (len(args) > 2):
        utc_diff = int(args[2])
    else:
        utc_diff = 3

    # read vat percentage from command line argument
    if (len(args) > 3):
        vat_percentage = float(args[3])
    else:
        vat_percentage = 24

    # use local data for testing 
    if (len(args) > 4) and (args[4] == 'debug'):
        use_local_data = True
    else:
        use_local_data = False

    return eic_code, utc_diff, vat_percentage, use_local_data

