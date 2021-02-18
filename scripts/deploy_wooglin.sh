printf "First, we need to create our virtual environment and grab the necessary packages..."
cd ../
virtualenv deployment_env
source deployment_env/bin/activate
pip install -r requirements.txt
deactivate
cd deployment_env/lib/python3.8/site-packages/
zip -r ../../../../deployment_library.zip .

printf "Great. Now, let's zip up all our source code to be uploaded to S3..."
cd source
zip -r ../wooglin-source.zip .
cd ..

printf "Awesome, and now to combine the zips..."
zip -g wooglin-body.zip deployment_library.zip wooglin-source.zip

printf "Great, let's upload to S3..."
aws s3 cp wooglin-body.zip s3://wooglin-guts/