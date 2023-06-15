import boto3
import docker

# Set your AWS credentials and region
aws_access_key_id = 'AKIAYKKMULDDX72Q7XON'
aws_secret_access_key = 'LZ3Ih9BAQcmWnCCqk5qS9XjjvdIpaz//b9zi72yK'
region = 'ap-south-1'
aws_account_id = '571928238279'

# Set the Docker image details
image_name = 'flask'
tag = '2.0'
ecr_repository = 'test2'



def build_docker_image():
    client = docker.from_env()
    image_tag = f'{image_name}:{tag}'
    image, _ = client.images.build(path='.', dockerfile='Dockerfile', tag=image_tag)
    return image


def push_docker_image(image):
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )
    ecr_client = session.client('ecr')

    ecr_repository_uri = f'{aws_account_id}.dkr.ecr.{region}.amazonaws.com/{ecr_repository}'

    ecr_client.get_authorization_token()
    response = ecr_client.describe_repositories(repositoryNames=[ecr_repository])

    if 'repositories' in response and response['repositories']:
        registry_id = response['repositories'][0]['registryId']
    else:
        response = ecr_client.create_repository(repositoryName=ecr_repository)
        registry_id = response['repository']['registryId']

    ecr_repository_uri = f'{aws_account_id}.dkr.ecr.{region}.amazonaws.com/{ecr_repository}'
    login_info = ecr_client.get_authorization_token()['authorizationData'][0]
    token = login_info['authorizationToken']
    endpoint = login_info['proxyEndpoint']

    client = docker.from_env()
    client.login(username='AWS', password=token, registry=endpoint)
    client.images.push(f'{ecr_repository_uri}:{tag}')

    print(f'Docker image pushed to ECR repository: {ecr_repository_uri}:{tag}')

if __name__ == '__main__':
    docker_image = build_docker_image()
    push_docker_image(docker_image)
