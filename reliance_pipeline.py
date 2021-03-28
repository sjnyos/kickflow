
import kfp
import kfp.components as components
import kfp.dsl as dsl

@dsl.pipeline(
    name="Reliance Object Detection",
    description="saving the container data to the pvc"
)

def reliance_object_detection():
    vop = dsl.VolumeOp(
        name="objectdetection_pvc",
        resource_name="Template-detection-dev",
        size="20Gi",
        modes=dsl.VOLUME_MODE_RWO
    )

    preprocess = dsl.ContainerOp(
	  name="Preprocessing the Data",
          image="surajmachamasi/customprint:latest",
          command=["python","print.py"],
	  #arguments=["echo 1 | tee /mnt/file1"]
          pvolumes={"/obj": vop.volume}
		)
    train = dsl.ContainerOp(
            name="Training the Data",
            image="sagark24/train",
            command=["python","train.py"],
            #arguments=["echo 1 | tee /mnt/file1"],
            pvolumes={"/obj": vop.volume}
        ).after(preprocess)
   
    finetune = dsl.ContainerOp(
            name="Finetuning with hydra",
            image="sagark24/finetune",
            command=["python","finetune.py"],
            #arguments=["echo 1 | tee /mnt/file1"],
            pvolumes={"/obj": vop.volume}
        ).after(train)
   
    evaluate = dsl.ContainerOp(
            name="evaluate with hydra",
            image="surajmachamasi/customprint:latest",
            command=["python","print.py"],
            #arguments=["echo 1 | tee /mnt/file1"],
            pvolumes={"/obj": vop.volume}
        ).after(finetune)

    
pipeline_func = reliance_object_detection
run_name = pipeline_func.__name__ + " run"
experiment_name = "Object Detection Experiment"
arguments = {}


client = kfp.Client()
run_result = client.create_run_from_pipeline_func(
    pipeline_func,
    experiment_name=experiment_name,
    run_name=run_name,
    arguments=arguments,
    )

    

