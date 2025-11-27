"""
Script to help upload model to cloud storage
You can use this to upload your model to various services
"""
import os
import boto3
from botocore.exceptions import ClientError

def upload_to_s3(file_path, bucket_name, object_name=None):
    """Upload model to AWS S3"""
    if object_name is None:
        object_name = os.path.basename(file_path)
    
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
        print(f"Model uploaded successfully to: {url}")
        return url
    except ClientError as e:
        print(f"Error uploading to S3: {e}")
        return None

def get_github_raw_url(repo_owner, repo_name, branch, file_path):
    """Generate GitHub raw URL for model file"""
    return f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/{file_path}"

if __name__ == "__main__":
    # Example: Upload to S3
    # upload_to_s3('gbr_pipeline.pkl', 'your-bucket-name', 'models/gbr_pipeline.pkl')
    
    # Example: GitHub raw URL (if model is in a public repo)
    # url = get_github_raw_url('WaelAhmad8822', 'CLSProject', 'main', 'gbr_pipeline.pkl')
    # print(f"GitHub URL: {url}")
    
    print("Please upload your model file to one of these services:")
    print("1. GitHub (as a release asset or in a public repo)")
    print("2. AWS S3 (make bucket public or use signed URLs)")
    print("3. Google Cloud Storage")
    print("4. Vercel Blob Storage (using @vercel/blob)")
    print("5. Any public file hosting service")
    print("\nThen set the MODEL_URL environment variable in Vercel to the model's URL")

