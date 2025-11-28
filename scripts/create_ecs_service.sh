aws ecs create-service \
    --cluster another-bat-kx41n4 \
    --service-name devops-fargate-task-service-123 \
    --task-definition devops-fargate-task:51 \
    --desired-count 1 \
    --launch-type FARGATE \
    --deployment-controller type=CODE_DEPLOY \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-74021739,subnet-56460009,subnet-b443ca85,subnet-ff4d72f1,subnet-84aeeea5,subnet-b82762de],securityGroups=[sg-0415348404c8f42a4],assignPublicIp=ENABLED}" \
    --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:us-east-1:683745400026:targetgroup/Prod/09bd2da4e27553ad,containerName=devops-app,containerPort=5000"
