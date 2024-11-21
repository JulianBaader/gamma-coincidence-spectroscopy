import yaml
import argparse
from mimocorb.buffer_control import run_mimoDAQ


# get information about the setup
parser = argparse.ArgumentParser()
"""
Input can be either tar or redpitaya
Output can be tar, spectrum, coincidence
Trigger can be IN1 or IN2
"""
parser.add_argument("-i", "--input", help="Input type", type=str)
parser.add_argument("-o", "--output", help="Output type", type=str)
parser.add_argument("-t", "--trigger", help="Trigger type", type=str)
parser.add_argument("-v", "--verbose", type=int, default=2, help="verbosity level (2)")
parser.add_argument("-d", "--debug", action="store_true", help="switch on debug mode (False)")

args = parser.parse_args()


input_type = args.input
output_type = args.output
trigger_type = args.trigger

while input_type not in ['tar', 'redpitaya']:
    input_type = input("Select an input (tar, redpitaya): ")
while output_type not in ['tar', 'spectrum', 'coincidence']:
    output_type = input("Select an output (tar, spectrum, coincidence): ")
while trigger_type not in ['IN1', 'IN2']:
    trigger_type = input("Select a trigger (IN1, IN2): ")


# create a setup
with open('setup_templates/' + output_type + '.yaml', 'r') as file:
    template = yaml.load(file, Loader=yaml.FullLoader)

# load RB_1 setup
with open('setup_templates/RB_1.yaml', 'r') as file:
    rb_1 = yaml.load(file, Loader=yaml.FullLoader)

setup = template


fkt_1 = setup['Functions'][1]['Fkt_1']

if input_type == 'redpitaya':
    fkt_1['file_name'] = "rpDAQ"
    fkt_1['fkt_name'] = "rp_mimocorb"
elif input_type == 'tar':
    fkt_1['file_name'] = "mimoCoRB/file_source"
    fkt_1['fkt_name'] = "tar_parquet_source"
else:
    raise ValueError(f"{input_type=} not correctly implemented")


setup['RingBuffer'][0]['RB_1'] = rb_1
rb_1_data_type = setup['RingBuffer'][0]['RB_1']['data_type']
if trigger_type == 'IN1':
    rb_1_data_type[1][0] = 'trigger_channel'
    rb_1_data_type[2][0] = 'coincidence_channel'
elif trigger_type == 'IN2':
    rb_1_data_type[1][0] = 'coincidence_channel'
    rb_1_data_type[2][0] = 'trigger_channel'
else:
    raise ValueError(f"{trigger_type=} not correctly implemented")

# save the setup
setup_filename = 'setup.yaml'
with open(setup_filename, 'w') as file:
    yaml.dump(setup, file)

daq = run_mimoDAQ(setup_filename, verbose=args.verbose, debug=args.debug)

daq.setup()

daq.run()
