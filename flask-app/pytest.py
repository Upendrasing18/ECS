import subprocess

def push_image_to_ecr(region, repository, image_tag):
    # Get the ECR login password
    login_command = ['aws', 'ecr', 'get-login-password', '--region', region]
    password = subprocess.check_output(login_command).decode('utf-8').strip()

    # Login to ECR with the obtained password
    docker_login_command = ['docker', 'login', '--username', 'AWS', '--password-stdin', repository]
    subprocess.run(docker_login_command, input=password.encode('utf-8'))

    # Build the Docker image
    docker_build_command = ['docker', 'build', '-t', image_tag, '.']
    subprocess.run(docker_build_command)

    # Tag the Docker image
    docker_tag_command = ['docker', 'tag', image_tag, f'{repository}:{image_tag}']
    subprocess.run(docker_tag_command)

    # Push the Docker image to ECR
    docker_push_command = ['docker', 'push', f'{repository}:{image_tag}']
    subprocess.run(docker_push_command)

# Usage example
region = 'ap-south-1'
repository = '571928238279.dkr.ecr.ap-south-1.amazonaws.com/test2'
image_tag = '2.0'


push_image_to_ecr(region, repository, image_tag)
