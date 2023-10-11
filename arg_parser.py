EIC_CODE = '10YFI-1--------U'

class ArgParser:
    def __init__(self, args):
        self.args = args

    def parse(self):
        # read command line argument for Domain EIC Code
        if len(self.args) > 1:
            eic_code = self.args[1]
        else:
            eic_code = EIC_CODE

        # read command line argument for difference from UTC in hours
        if (len(self.args) > 2):
            utc_diff = int(self.args[2])
        else:
            utc_diff = 3

        # read vat percentage from command line argument
        if (len(self.args) > 3):
            vat_percentage = float(self.args[3])
        else:
            vat_percentage = 24

        # use local data for testing 
        if (len(self.args) > 4) and (self.args[4] == 'debug'):
            use_local_data = True
        else:
            use_local_data = False

        return eic_code, utc_diff, vat_percentage, use_local_data

