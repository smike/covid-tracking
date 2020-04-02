import argparse
import subprocess
import yaml
import os.path

parser = argparse.ArgumentParser(description='Evaluate all urlwatch filters.')
parser.add_argument('--output_dir', type=str, default=None,
                    help='''If set, the output for each filter will be written
                    to a separate file in this directory. If unset, it will be 
                    sent to STDOUT''')

args = parser.parse_args()
args.output_dir

with open('urls.yaml', 'r') as file:
  urls_list = yaml.load_all(file, Loader=yaml.FullLoader)

  for i, url in enumerate(urls_list):
    i += 1

    urlwatch_output = ''
    try:
      urlwatch_output = subprocess.check_output(
        ['urlwatch', '--urls', 'urls.yaml', '--test-filter', '{}'.format(i)], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
      urlwatch_output = e.output.decode()

    if args.output_dir:
      with open(os.path.join(args.output_dir, url['name']), 'w') as f:
        print(f"{url['name']}")
        f.write(str(urlwatch_output))
    else:
      print(f"{url['name']}:\n{urlwatch_output}\n")


