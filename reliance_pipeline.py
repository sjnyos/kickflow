
import kfp
import kfx

import kfp.components as components
import kfp.dsl as dsl
import kfx.dsl 

helper = kfx.dsl.ArtifactLocationHelper(
    scheme="minio", bucket="mlpipeline", key_prefix="artifacts/"
) 

@dsl.pipeline(
    name="Reliance Object Detection",
    description="saving the container data to the pvc"
)

def creating_pipeline_metadata( name,description, owner, uri, model_type):
    return  model = exec.log_output(
            metadata.Model(
            name=name,
            description=description,
            owner=owner,
            uri=uri,
            model_type=model_type,
            training_framework={
            "name": "tensorflow",
            "version": "v1.0"
            })

def reliance_object_detection():
    
    vop =  dsl.VolumeOp(
        name="objectdetection_pvc",
        resource_name="Template-detection-dev",
        size="8Gi",
        modes=dsl.VOLUME_MODE_RWO
    )
    _creating_pipeline_metadata = creating_pipeline_metadata("Reliance obj","test","test@test.com","gcs://my-bucket/mnist","neural_network")
    _pre_process = preprocess().add_pvolumes({"/obj": vop.volume}).set_display_name('Preprocessing data')._set_metadata(_creating_pipeline_metadata)
    _train= train().add_pvolumes({"/obj": vop.volume}).set_display_name('Traning data').after(_pre_process)
    _finetune= finetune().add_pvolumes({"/obj": vop.volume}).set_display_name('Finetuning data').after(_train)
    _evaluate= evaluate().add_pvolumes({"/obj": vop.volume}).set_display_name('Evaluatin data').after(_finetune)


def preprocess():

    return dsl.ContainerOp(
	      name="Preprocessing the Data",
          image="surajmachamasi/customprint:latest",
          command=["python","print.py"],
          #file_outputs={ }
		)

def  train():
 return dsl.ContainerOp(
            name="Training the Data",
            image="registry.gitlab.com/automation-jukshio/ml-ops/template-detection-demo/train:v1-slim",
            command=["python","train.py"],
        )
   
def  finetune():
  return dsl.ContainerOp(
            name="Finetuning with hydra",
            image="registry.gitlab.com/automation-jukshio/ml-ops/template-detection-demo/finetune:v1-slim",
            command=["python","finetune.py"]
        )
   
def  evaluate():
    return dsl.ContainerOp(
            name="evaluate with hydra",
            image="surajmachamasi/customprint:latest",
            command=["python","print.py"],
        )

    
pipeline_func = reliance_object_detection
run_name = pipeline_func.__name__ + " run"
experiment_name = "Object Detection Experiment"
arguments = {}


client = kfp.Client()
run_result = client.create_run_from_pipeline_func(
    reliance_object_detection,
    experiment_name=experiment_name,
    run_name=run_name,
    arguments=arguments,
    )

    

