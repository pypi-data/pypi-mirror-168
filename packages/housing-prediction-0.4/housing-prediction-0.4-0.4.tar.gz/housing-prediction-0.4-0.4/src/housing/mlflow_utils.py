import mlflow


def mlflow_start_run(f):
    def inner(*args, **kwrgs):
        with mlflow.start_run(nested=True):
            return f(*args, **kwrgs)

    return inner


def mlflow_conf(f):
    def inner(*args, **kwrgs):
        mlflow.set_tracking_uri("http://localhost:8889/")
        EXPERIMENT_NAME = "hosuing-production"
        exp_found = False
        for exp in mlflow.list_experiments():
            if exp.name == EXPERIMENT_NAME:
                exp_found = True
                break
        if not exp_found:
            print("Experiment not found, needs to create")
            mlflow.create_experiment(EXPERIMENT_NAME)
        print(f"Experiment {EXPERIMENT_NAME} set")
        mlflow.set_experiment("hosuing-production")
        return f(*args, **kwrgs)

    return inner
