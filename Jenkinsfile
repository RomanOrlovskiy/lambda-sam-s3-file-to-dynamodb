pipeline {
    agent any

    environment {
        bucketName='rorlovskyi-lambda-sam-s3-file-to-dynamodb'
        stackName="s3-dynamodb"        
    }

    stages {

        //Retrieve cloudformation templates
        stage('Cloning Git repo') {
          steps {
              sshagent (credentials: ['464b0ae2-8c8a-4c41-9b8e-c34b1f5e76c5']) {
                        git branch: 'master', url: 'git@github.com:RomanOrlovskiy/lambda-sam-app-helloworld.git', credentialsId: '464b0ae2-8c8a-4c41-9b8e-c34b1f5e76c5'
                }
          }
        }

        stage ('Tests') {
            steps {
                script{
                  sh "sam local invoke FileToDynamoDB -e event.json"
              }
          }
        }


        stage ('Build') {
            steps {
                sh "sam build"
            }
        }



        stage ('Package') {
            steps {
                sh """
                sam package \
                    --output-template-file packaged.yaml \
                    --s3-bucket ${bucketName}
                """
            }
        }

        stage ('Deploy') {
            steps {
                sh """
                sam deploy \
                    --template-file packaged.yaml \
                    --stack-name ${stackName} \
                    --capabilities CAPABILITY_IAM
                """
            }
        }

    }
}