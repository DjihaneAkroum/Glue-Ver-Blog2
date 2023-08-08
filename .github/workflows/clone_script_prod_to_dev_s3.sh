#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <prod_script_name>"
  exit 1
fi

dev_script_path="s3://dev-bi-data-scripts-easygenerator/"
prod_script_name="$1"

dev_script_name="${prod_script_name/prod/dev}"

dev_script_name_py="$dev_script_name.py"
prod_script_name_py="$prod_script_name.py"

echo "dev_script_name_py = $dev_script_name_py"
echo "prod_script_name_py = $prod_script_name_py"

echo "dev_script_path = $dev_script_path"

mkdir to_clone
cd to_clone
touch "$dev_script_name_py"
cd ../

ls ../../$prod_script_name

echo "aws s3 sync to_clone/ $dev_script_path --profile bi_account"
aws s3 sync to_clone/ $dev_script_path --profile bi_account
rm -r to_clone

