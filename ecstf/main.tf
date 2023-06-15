# Define provider
provider "aws" {
  region = "ap-south-1"  # Replace with your desired region
}

# Create ECS cluster
resource "aws_ecs_cluster" "my_cluster" {
  name = "new1"  # Replace with your preferred cluster name
}



# Create ECR repository
resource "aws_ecr_repository" "my_repository" {
  name = "myrepo"  # Replace with your preferred repository name
}



# Create ECS task definition
resource "aws_ecs_task_definition" "my_task_definition" {
  family                = "my-task"
  network_mode          = "awsvpc"
  cpu                   = 512
  memory                = 1024
  requires_compatibilities = ["FARGATE"]
  

  container_definitions = <<DEFINITION
  [{
    "name": "my-container1",
    "image": "public.ecr.aws/g4k2b3i6/test1:1",
    "portMappings": [
      {
        "containerPort": 80,
        "hostPort": 80,
        "protocol": "tcp"
      },
      {
        "containerPort": 5000,
        "hostPort": 5000,
        "protocol": "tcp"
      }
    ],
    "cpu": 512,
    "memory": 1024,
    "networkMode": "awsvpc"
  }]
  DEFINITION

}

# Create ECS service
resource "aws_ecs_service" "my_service" {
  name            = "my-service1"
  cluster         = aws_ecs_cluster.my_cluster.id
  task_definition = aws_ecs_task_definition.my_task_definition.arn
  desired_count   = 1
  
  launch_type     = "FARGATE" 
  scheduling_strategy  = "REPLICA"
  force_new_deployment = true

  network_configuration {
    subnets         = ["subnet-049f8618bd8dca446", "subnet-041fec10a42e9b112"]  # Replace with your subnet IDs
    security_groups = ["sg-050c131a70a192bdf"]  # Replace with your security group IDs
    assign_public_ip = true
    #assign_public_ip = true
  }
}

