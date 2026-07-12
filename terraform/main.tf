provider "aws" {
  region = "us-east-1"
}

resource "aws_ecs_cluster" "ticketslayer_cluster" {
  name = "ticketslayer-ai-cluster"
}

resource "aws_ecs_task_definition" "ticketslayer_task" {
  family                   = "ticketslayer-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512

  container_definitions = jsonencode([{
    name      = "ticketslayer-ai"
    image     = "ticketslayer:latest"
    essential = true
    portMappings = [{
      containerPort = 8080
      hostPort      = 8080
    }]
  }])
}
