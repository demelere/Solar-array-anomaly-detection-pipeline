import sagemaker
from sagemaker.workflow.parameters import ParameterString
from sagemaker.estimator import Estimator
from sagemaker.inputs import TrainingInput
from sagemaker.workflow.steps import TrainingStep, CreateModelStep
from sagemaker.model import Model
from sagemaker.workflow.pipeline import Pipeline

sagemaker_session = sagemaker.Session()

solar_data_input = ParameterString( # pipeline parameters
    name="SolarDataInputUrl",
    default_value="" # TO DO: update with S3 url later
)
solar_model_output = ParameterString(
    name="SolarModelOutputUrl",
    default_value="" # TO DO: update with S3 output URL for storing the model artifacts
)

solar_estimator = Estimator(
    image_uri="", # TO DO: update with CatBoost Docker image URI in ECR, or feed in with .env file
    role="SageMakerRole", # same here, use env file for SageMaker execution role ARN
    instance_count=1,
    instance_type="ml.m5.xlarge",
    output_path=solar_model_output.resolve(),
    sagemaker_session=sagemaker_session,
)

solar_estimator.set_hyperparameters(
    depth=6,
    iterations=500,
    learning_rate=0.1,
)

solar_training_input = TrainingInput( # TrainingInput object pointing at the solar data in S3
    s3_data=solar_data_input.resolve(),
    content_type="csv"
)

solar_training_step = TrainingStep(
    name="SolarPowerModelTraining",
    estimator=solar_estimator,
    inputs={
        "train": solar_training_input
    }
)

solar_model = Model(
    image_uri="", # TO DO: use .env to store the CatBoost Docker image URI in ECR
    model_data=solar_training_step.properties.ModelArtifacts.S3ModelArtifacts,
    role="SageMakerRole", # TO DO: store SageMaker execution role ARN in .env
    sagemaker_session=sagemaker_session,
)

solar_model_step = CreateModelStep(
    name="CreateSolarPowerModel",
    model=solar_model,
    inputs=sagemaker.inputs.CreateModelInput(
        instance_type="ml.m5.xlarge"
    )
)

solar_pipeline = Pipeline(
    name="SolarTelemetryTrainingPipeline",
    parameters=[
        solar_data_input,
        solar_model_output
    ],
    steps=[solar_training_step, solar_model_step],
    sagemaker_session=sagemaker_session,
)

def main():
    solar_pipeline.upsert(role_arn="") # use env to store role ARN
    solar_pipeline_execution = solar_pipeline.start()
    print(f"Solar telemetry pipeline execution started with ARN: {solar_pipeline_execution.arn}")

if __name__ == "__main__":
    main()
